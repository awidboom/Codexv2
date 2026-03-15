import argparse
import csv
import json
import re
import socket
import sys
import time
from io import BytesIO
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import build_opener, HTTPCookieProcessor, ProxyHandler, Request
from http.cookiejar import CookieJar
from pypdf import PdfReader
from pypdf.errors import DependencyError

FIELDNAMES = [
    "ApprovalOrderID",
    "AppliedOn",
    "IssuedOn",
    "PDFLink",
    "OwnerName",
    "SourceName",
    "PhysicalStreet",
    "PhysicalCity",
    "PhysicalState",
    "PhysicalZip",
    "SourceContactName",
    "SourceContactPhone",
    "SourceContactEmail",
    "UTM_Easting",
    "UTM_Northing",
    "UTM_Zone",
    "UTM_Datum",
    "SIC_Code",
    "GeneralDescription",
    "NSR_Classification",
    "Source_Classification",
    "Applicable_Federal_Standards",
    "Project_Description",
    "Project_CO2e_TPY",
    "Project_CO_TPY",
    "Project_NOx_TPY",
    "Project_PM10_TPY",
    "Project_PM25_TPY",
    "Project_SO2_TPY",
    "Project_VOC_TPY",
    "Project_Total_HAPs_TPY",
    "Source_CO2e_TPY",
    "Source_CO_TPY",
    "Source_NOx_TPY",
    "Source_PM10_TPY",
    "Source_PM25_TPY",
    "Source_SO2_TPY",
    "Source_VOC_TPY",
    "Source_Total_HAPs_TPY",
]

BASE = "https://daqpermitting.utah.gov"
LIST_URL = BASE + "/AOsIssuedAll"
AJAX_URL = BASE + "/ajax_report_data"
socket.setdefaulttimeout(60)
PER_PERMIT_TIMEOUT_SEC = None  # None to disable per-permit parse timeout
MAX_PERMITS = None  # default max; can be overridden via CLI
OUT_CSV = "permits_all.csv"

# Helpers

def clean_spaces(s):
    return re.sub(r"\s+", " ", s or "").strip()

def clean_phone(phone):
    p = clean_spaces(phone)
    p = p.replace(" -", "-").replace("- ", "-")
    return p

def clean_email(email):
    return email.replace(" ", "").replace("\u00a0", "").strip()

def find_between(text, start, end):
    # ensure the end alternatives are grouped to avoid regex precedence issues
    pattern = start + r"(.*?)" + r"(?:%s)" % end
    matches = re.findall(pattern, text, flags=re.S | re.I)
    for m in reversed(matches):
        s = m.strip()
        if s:
            return s
    return ""

def find_after(text, label):
    m = re.search(label + r"\s*([^\n]+)", text, flags=re.I)
    return clean_spaces(m.group(1)) if m else ""

def find_number(text, label):
    # capture the last numeric token after the label to avoid header matches
    pattern = label + r".*?([-]?[0-9][0-9.,]*)"
    matches = re.findall(pattern, text, flags=re.I | re.S)
    if matches:
        val = matches[-1]
        try:
            return float(val.replace(",", ""))
        except ValueError:
            return val
    return ""

def find_pollutant(text, label):
    # look line by line for the label, then grab last number on that line
    for line in text.splitlines():
        if re.search(label, line, flags=re.I):
            nums = re.findall(r"[-]?[0-9][0-9.,]*", line)
            if nums:
                try:
                    return float(nums[-1].replace(",", ""))
                except ValueError:
                    return nums[-1]
    return find_number(text, label)


def _to_float(s):
    try:
        return float(s.replace(",", ""))
    except Exception:
        return None


def _clean_nsr_value(nsr):
    nsr = clean_spaces(nsr)
    if not nsr:
        return ""

    # Strip common footer/header artifacts that get concatenated into the extracted value.
    nsr = re.sub(r"\bDAQE\s*[-â€“]\s*[A-Z0-9]+(?:[-â€“]\s*[0-9]+)?\s*Page\s*\d+\b", "", nsr, flags=re.I)
    nsr = re.sub(r"\bDAQE-[A-Z0-9]+-[0-9]+\b", "", nsr, flags=re.I)
    nsr = re.sub(r"\bPage\s*\d+\b", "", nsr, flags=re.I)
    nsr = clean_spaces(nsr)

    # Normalize common variants to canonical labels used in outputs.
    canonical = [
        "Administrative Amendment",
        "10-Year Review",
        "Experimental AO",
        "Major PSD Modification",
        "Major Modification at Minor Source",
        "Minor Modification at Major Source",
        "Minor Modification at Minor Source",
        "New Major Source",
        "New Minor Source",
        "Modification",
    ]
    lowered = nsr.lower()
    for label in canonical:
        if lowered.startswith(label.lower()):
            return label

    # Some documents include punctuation or extra words; match contains for the most common types.
    contains_map = {
        r"\badministrative\s+amendment\b": "Administrative Amendment",
        r"\b10\s*[- ]\s*year\s+review\b": "10-Year Review",
        r"\bexperimental\s+(?:ao|approval\s+order)\b": "Experimental AO",
        r"\bmajor\s+psd\s+modification\b": "Major PSD Modification",
        r"\bminor\s+modification\b.*\bminor\s+source\b": "Minor Modification at Minor Source",
        r"\bminor\s+modification\b.*\bmajor\s+source\b": "Minor Modification at Major Source",
        r"\bmajor\s+modification\b.*\bminor\s+source\b": "Major Modification at Minor Source",
        r"\bnew\s+major\s+(?:stationary\s+)?source\b": "New Major Source",
        r"\bnew\s+minor\s+source\b": "New Minor Source",
    }
    for rx, label in contains_map.items():
        if re.search(rx, nsr, flags=re.I | re.S):
            return label

    return nsr


def extract_nsr_classification(text):
    # Primary: the structured block in the "General Information" section
    nsr = clean_spaces(find_between(text, r"NSR Classification", r"Source Classification"))
    if nsr:
        return _clean_nsr_value(nsr)

    # Common "Type of Action" style phrasing (varies by document)
    line = find_after(text, r"(?:Type of Action|Action Type|Permit Action)\s*:")
    if line:
        return _clean_nsr_value(line)

    # Heuristic fallback for documents where section headings don't extract cleanly.
    if re.search(r"\badministrative\s+amendment\b", text, flags=re.I):
        return "Administrative Amendment"
    if re.search(r"\b10\s*[- ]\s*year\s+review\b", text, flags=re.I):
        return "10-Year Review"
    if re.search(r"\bexperimental\s+(?:ao|approval\s+order)\b", text, flags=re.I):
        return "Experimental AO"
    # PSD: avoid false positives from acronym lists / regulatory references by requiring explicit phrasing.
    if re.search(r"\bmajor\s+psd\s+modification\b", text, flags=re.I) or re.search(r"\bpsd\s+major\s+modification\b", text, flags=re.I):
        return "Major PSD Modification"
    if re.search(r"\bmajor\s+modification\b", text, flags=re.I) and re.search(r"\bminor\s+source\b", text, flags=re.I):
        return "Major Modification at Minor Source"
    if re.search(r"\bminor\s+modification\b", text, flags=re.I) and re.search(r"\bmajor\s+source\b", text, flags=re.I):
        return "Minor Modification at Major Source"
    if re.search(r"\bminor\s+modification\b", text, flags=re.I) and re.search(r"\bminor\s+source\b", text, flags=re.I):
        return "Minor Modification at Minor Source"
    # New source: require a request/permit-action context to avoid false positives in applicability discussions.
    if re.search(r"\brequested\b.{0,120}\bnew\s+major\s+(?:stationary\s+)?source\b", text, flags=re.I | re.S) or re.search(r"\bapproval\s+order\b.{0,120}\bfor\b.{0,60}\bnew\s+major\s+(?:stationary\s+)?source\b", text, flags=re.I | re.S):
        return "New Major Source"
    if re.search(r"\brequested\b.{0,120}\bnew\s+minor\s+source\b", text, flags=re.I | re.S) or re.search(r"\bapproval\s+order\b.{0,120}\bfor\b.{0,60}\bnew\s+minor\s+source\b", text, flags=re.I | re.S):
        return "New Minor Source"

    # Your preference: if it doesn't state a classification, treat it as a modification.
    return "Modification"


def _project_change_values_from_emissions(emissions):
    if not emissions:
        return []
    vals = []
    for k, v in emissions.items():
        if not (k.startswith("Project_") and k.endswith("_TPY")):
            continue
        if v == "" or v is None:
            continue
        try:
            vals.append(float(v))
        except Exception:
            continue
    return vals


def infer_nsr_classification(text, emissions=None):
    """
    Combine direct extraction with conservative heuristics that use the Summary of Emissions table.
    """
    # Cover letter "Re:" line is often the clearest statement of what the AO is.
    m = re.search(r"Re\s*:\s*Approval\s+Order\s*:\s*([^\n]+)", text, flags=re.I)
    if m:
        re_line = clean_spaces(m.group(1))
        re_line_low = re_line.lower()
        if "administrative amendment" in re_line_low:
            return "Administrative Amendment"
        if "10-year review" in re_line_low or "10 year review" in re_line_low:
            return "10-Year Review"
        if "experimental" in re_line_low:
            return "Experimental AO"
        if "major psd modification" in re_line_low:
            return "Major PSD Modification"
        if "minor modification" in re_line_low and "minor source" in re_line_low:
            return "Minor Modification at Minor Source"
        if "minor modification" in re_line_low and "major source" in re_line_low:
            return "Minor Modification at Major Source"
        if "major modification" in re_line_low and "minor source" in re_line_low:
            return "Major Modification at Minor Source"
        if "new major source" in re_line_low:
            return "New Major Source"
        if "new minor source" in re_line_low:
            return "New Minor Source"
        if "modification" in re_line_low:
            return "Modification"

    nsr = _clean_nsr_value(extract_nsr_classification(text))
    if nsr and nsr != "Modification":
        return nsr

    # New minor source: many AOs describe the project as a new facility but don't cleanly expose
    # the NSR Classification field in extracted text. For reviewed examples, this correlates with
    # "Change (tpy)" values being 0 across pollutants.
    change_vals = _project_change_values_from_emissions(emissions)
    all_change_zero = len(change_vals) >= 2 and all(abs(v) < 1e-9 for v in change_vals)
    if all_change_zero:
        if re.search(r"\brequested\b.{0,60}\b(?:ao|approval\s+order)\b.{0,120}\bnew\b.{0,60}\b(?:facility|source|plant|site)\b", text, flags=re.I | re.S):
            return "New Minor Source"
        if re.search(r"\bthe\s+new\s+[A-Za-z0-9 ,.'-]{0,60}\bfacility\b", text, flags=re.I):
            return "New Minor Source"

    # Default to the extracted (likely "Modification") value.
    return nsr or "Modification"


def parse_summary_emissions(text):
    """
    Extract emissions from the Summary of Emissions table:
      - project_emissions: "Change (tpy)"
      - source_emissions: "Total (tpy)"

    Many AOs include three numeric columns (e.g., Existing, Change, Total). This parser
    takes the last two numeric tokens on a pollutant row as (change, total).
    """
    emissions_text = find_between(text, r"SUMMARY OF EMISSIONS", r"SECTION|SECTION I|SECTION  I|SECTION II")
    if not emissions_text:
        return {}

    lines = emissions_text.splitlines()

    def extract_change_total(label_rx):
        for i, line in enumerate(lines):
            if not re.search(label_rx, line, flags=re.I):
                continue
            window = line
            nums = re.findall(r"[-]?[0-9][0-9.,]*", window)
            if len(nums) < 2 and i + 1 < len(lines):
                window = window + " " + lines[i + 1]
                nums = re.findall(r"[-]?[0-9][0-9.,]*", window)
            if len(nums) < 2:
                continue
            change = _to_float(nums[-2])
            total = _to_float(nums[-1])
            return change, total
        return None, None

    mapping = {
        "CO2e": r"CO\s*2\s*Equivalent|CO2e",
        "CO": r"Carbon\s+Monoxide|\bCO\b",
        "NOx": r"Nitrogen\s+Oxides|\bNOx\b",
        "PM10": r"PM\s*10|PM10",
        "PM25": r"PM\s*2\.?5|PM2\.?5",
        "SO2": r"Sulfur\s+Dioxide|SO2",
        "VOC": r"Volatile\s+Organic\s+Compounds|\bVOC\b",
        "Total_HAPs": r"\bTotal\s+HAPs\b",
    }

    out = {}
    for key, rx in mapping.items():
        change, total = extract_change_total(rx)
        if change is not None:
            out[f"Project_{key}_TPY"] = change
        if total is not None:
            out[f"Source_{key}_TPY"] = total
    return out


def _looks_like_garbled_extraction(text):
    # Heuristic: some PDFs extract as lots of /i### tokens instead of readable text.
    return len(re.findall(r"/i\d{2,4}", text)) > 200


def _ocr_applied_on_from_pdf_bytes(pdf_bytes, date_pat):
    """
    Best-effort OCR of the first page to recover 'NOI received on <date>' style language
    when PDF text extraction is garbled.

    Requires: pytesseract + pdf2image + Tesseract + Poppler.
    """
    try:
        import pytesseract  # type: ignore
        from pdf2image import convert_from_bytes  # type: ignore
    except Exception:
        return ""

    # Prefer explicit Windows install locations if PATH isn't updated in this shell.
    tesseract_exe = Path(r"C:\Program Files\Tesseract-OCR\tesseract.exe")
    current = pytesseract.pytesseract.tesseract_cmd or ""
    if (not current) or (current and not Path(current).exists()):
        if tesseract_exe.exists():
            pytesseract.pytesseract.tesseract_cmd = str(tesseract_exe)

    poppler_path = None
    poppler_bin = Path.home() / "AppData" / "Local" / "Microsoft" / "WinGet" / "Packages"
    if poppler_bin.exists():
        matches = list(poppler_bin.glob("**/Library/bin/pdftoppm.exe"))
        if matches:
            matches.sort(key=lambda p: len(str(p)))
            poppler_path = str(matches[0].parent)

    try:
        images = convert_from_bytes(pdf_bytes, dpi=300, first_page=1, last_page=1, poppler_path=poppler_path)
        if not images:
            return ""
        ocr_text = pytesseract.image_to_string(images[0])
    except Exception:
        return ""

    for pat in [
        rf"(?:Notice of Intent\s*\(NOI\)|NOI)\s*(?:application\s*)?received\s*on\s*({date_pat})",
        rf"(?:Notice of Intent\s*\(NOI\)|NOI)\s*(?:application\s*)?was\s*received\s*on\s*({date_pat})",
        rf"Application\s*(?:was\s*)?received\s*on\s*({date_pat})",
        rf"Is\s+Derived\s+From\s+NOI\s+dated\s*({date_pat})",
        rf"Derived\s+From\s+NOI\s+dated\s*({date_pat})",
        rf"NOI\s+dated\s*({date_pat})",
    ]:
        m = re.search(pat, ocr_text, flags=re.I)
        if m:
            return clean_spaces(m.group(1))
    return ""

def parse_pdf(pdf_bytes, page_limit=12):
    reader = PdfReader(BytesIO(pdf_bytes))
    pages = reader.pages[:page_limit]
    text = "\n".join((p.extract_text() or "") for p in pages)
    # Approval ID
    ao_id = ""
    m = re.search(r"DAQE\s*[-–]\s*([A-Z0-9]+)\s*[-–]\s*([0-9]+)", text)
    if m:
        ao_id = f"DAQE-{m.group(1)}-{m.group(2)}"
    # Issued On: prefer explicit label, else fallback
    issued_on = ""
    m = re.search(r"Issued On\s+([A-Za-z]+\s+\d{1,2},\s+20\d{2})", text)
    if m:
        issued_on = clean_spaces(m.group(1))
    if not issued_on:
        m = re.search(r"(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s+20\d{2}", text)
        if m:
            issued_on = clean_spaces(m.group(0))

    # Applied/NOI received date (often appears in the cover letter; sometimes appears near the end)
    applied_on = ""
    month_date = r"(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s*\s*20\d{2}"
    numeric_date = r"\d{1,2}/\d{1,2}/\d{2,4}"
    iso_date = r"20\d{2}-\d{2}-\d{2}"
    date_pat = rf"(?:{month_date}|{numeric_date}|{iso_date})"
    for pat in [
        rf"(?:Notice of Intent\s*\(NOI\)|NOI)\s*(?:application\s*)?received\s*on\s*({date_pat})",
        rf"(?:Notice of Intent\s*\(NOI\)|NOI)\s*(?:application\s*)?was\s*received\s*on\s*({date_pat})",
        rf"Application\s*(?:was\s*)?received\s*on\s*({date_pat})",
        rf"Is\s+Derived\s+From\s+NOI\s+dated\s*({date_pat})",
        rf"Derived\s+From\s+NOI\s+dated\s*({date_pat})",
        rf"NOI\s+dated\s*({date_pat})",
    ]:
        m = re.search(pat, text, flags=re.I)
        if m:
            applied_on = clean_spaces(m.group(1))
            break

    # If still blank, search the end of the PDF (some AOs place the NOI date in concluding text).
    if not applied_on and len(reader.pages) > 0:
        tail_pages = reader.pages[-5:] if len(reader.pages) >= 5 else reader.pages
        for page in tail_pages:
            t = page.extract_text() or ""
            if not t.strip():
                continue
            for pat in [
                rf"Is\s+Derived\s+From\s+NOI\s+dated\s*({date_pat})",
                rf"Derived\s+From\s+NOI\s+dated\s*({date_pat})",
                rf"(?:Notice of Intent\s*\(NOI\)|NOI)\s*(?:application\s*)?received\s*on\s*({date_pat})",
                rf"(?:Notice of Intent\s*\(NOI\)|NOI)\s*(?:application\s*)?was\s*received\s*on\s*({date_pat})",
                rf"Application\s*(?:was\s*)?received\s*on\s*({date_pat})",
                rf"NOI\s+dated\s*({date_pat})",
            ]:
                m = re.search(pat, t, flags=re.I)
                if m:
                    applied_on = clean_spaces(m.group(1))
                    break
            if applied_on:
                break

    # If extraction looks garbled and the date wasn't found, OCR the first page.
    if not applied_on and _looks_like_garbled_extraction(text):
        applied_on = _ocr_applied_on_from_pdf_bytes(pdf_bytes, date_pat) or ""

    # General info block
    sic_code = ""
    m = re.search(r"SIC code[: ]*\s*([0-9]{4})", text, flags=re.I)
    if m:
        sic_code = m.group(1)
    contact_name = ""
    contact_phone = ""
    contact_email = ""
    # Source Contact window
    m = re.search(r"Source Contact", text, flags=re.I)
    contact_window = ""
    if m:
        contact_window = text[m.start():m.start()+500]
    if contact_window:
        m_name = re.search(r"Name\s*:\s*([^\n]+)", contact_window, flags=re.I)
        if not m_name:
            m_name = re.search(r"Source Contact:?\s*([^\n]+)", contact_window, flags=re.I)
        if m_name:
            nm = clean_spaces(m_name.group(1))
            nm = re.sub(r"\s+[0-9].*", "", nm)
            contact_name = nm
        m_phone = re.search(r"\(?\d{3}\)?\s*\d{3}\s*[- ]?\s*\d{4}", contact_window)
        if m_phone:
            ph = clean_phone(m_phone.group(0))
            if ph:
                contact_phone = ph
        m_email = re.search(r"Email\s*:\s*([^\s]+@[^\s]+)", contact_window, flags=re.I)
        if m_email:
            em = clean_email(m_email.group(1))
            if em:
                contact_email = em
    # Fallbacks
    if not contact_name:
        m = re.search(r"Name\s*:\s*([A-Za-z .'-]+)", text, flags=re.I)
        if m:
            contact_name = clean_spaces(m.group(1))
    if not contact_phone:
        ph_line = find_after(text, r"Phone\s*:")
        if ph_line:
            m = re.search(r"\(?\d{3}\)?\s*\d{3}\s*[- ]?\s*\d{4}", ph_line)
            if not m:
                m = re.search(r"\d{3}[- ]?\d{3}[- ]?\d{4}", ph_line)
            if m:
                contact_phone = clean_phone(m.group(0))
    if not contact_email:
        m = re.search(r"Email\s*:\s*([^\s]+@[^\s]+)", text, flags=re.I)
        if m:
            contact_email = clean_email(m.group(1))
    utm_e = ""
    utm_n = ""
    utm_zone = ""
    utm_datum = ""
    m = re.search(r"([0-9][0-9,]+)\s*m Easting", text)
    if m:
        utm_e = m.group(1).replace(",", "")
    m = re.search(r"([0-9][0-9,]+)\s*m Northing", text)
    if m:
        utm_n = m.group(1).replace(",", "")
    m = re.search(r"UTM Zone\s*([0-9]+)", text, flags=re.I)
    if m:
        utm_zone = m.group(1)
    m = re.search(r"Datum\s*([A-Za-z0-9]+)", text, flags=re.I)
    if m:
        utm_datum = m.group(1)
    emissions = parse_summary_emissions(text)

    # Descriptions (prefer last occurrence to avoid table of contents)
    abstract = clean_spaces(find_between(text, r"Abstract", r"GENERAL INFORMATION|CONTACT/LOCATION INFORMATION|SUMMARY OF EMISSIONS|SECTION I|DAQE"))
    gen_desc = clean_spaces(find_between(text, r"General Description", r"NSR Classification"))
    nsr_class = infer_nsr_classification(text, emissions=emissions)
    source_class = clean_spaces(find_between(text, r"Source Classification", r"Applicable Federal Standards"))
    app_fed = clean_spaces(find_between(text, r"Applicable Federal Standards", r"Project Description"))
    proj_desc = clean_spaces(find_between(text, r"Project Description", r"SUMMARY OF EMISSIONS"))
    proj_desc = re.sub(r"DAQE\s*[-A-Z0-9 ]+Page\s*\d+", "", proj_desc, flags=re.I).strip()
    if abstract:
        if not gen_desc:
            gen_desc = abstract
        if not source_class:
            m = re.search(r"The plant is located in ([^.]+)", abstract, flags=re.I)
            if m:
                source_class = clean_spaces(m.group(1))
        pass
    return {
        "ApprovalOrderID": ao_id,
        "AppliedOnPdf": applied_on,
        "IssuedOnPdf": issued_on,
        "SIC_Code": sic_code,
        "SourceContactName": contact_name,
        "SourceContactPhone": contact_phone,
        "SourceContactEmail": contact_email,
        "UTM_Easting": utm_e,
        "UTM_Northing": utm_n,
        "UTM_Zone": utm_zone,
        "UTM_Datum": utm_datum,
        "GeneralDescription": gen_desc,
        "NSR_Classification": nsr_class,
        "Source_Classification": source_class,
        "Applicable_Federal_Standards": app_fed,
        "Project_Description": proj_desc,
        "Project_CO2e_TPY": emissions.get("Project_CO2e_TPY", ""),
        "Project_CO_TPY": emissions.get("Project_CO_TPY", ""),
        "Project_NOx_TPY": emissions.get("Project_NOx_TPY", ""),
        "Project_PM10_TPY": emissions.get("Project_PM10_TPY", ""),
        "Project_PM25_TPY": emissions.get("Project_PM25_TPY", ""),
        "Project_SO2_TPY": emissions.get("Project_SO2_TPY", ""),
        "Project_VOC_TPY": emissions.get("Project_VOC_TPY", ""),
        "Project_Total_HAPs_TPY": emissions.get("Project_Total_HAPs_TPY", ""),
        "Source_CO2e_TPY": emissions.get("Source_CO2e_TPY", ""),
        "Source_CO_TPY": emissions.get("Source_CO_TPY", ""),
        "Source_NOx_TPY": emissions.get("Source_NOx_TPY", ""),
        "Source_PM10_TPY": emissions.get("Source_PM10_TPY", ""),
        "Source_PM25_TPY": emissions.get("Source_PM25_TPY", ""),
        "Source_SO2_TPY": emissions.get("Source_SO2_TPY", ""),
        "Source_VOC_TPY": emissions.get("Source_VOC_TPY", ""),
        "Source_Total_HAPs_TPY": emissions.get("Source_Total_HAPs_TPY", ""),
    }

# Improved parser to handle cover-page contacts, abstract, and robust emissions
def parse_pdf_v2(pdf_bytes, page_limit=25):
    reader = PdfReader(BytesIO(pdf_bytes))
    pages = reader.pages[:page_limit]
    text = "\n".join((p.extract_text() or "") for p in pages)
    ao_id = ""
    m = re.search(r"DAQE\s*[-–]\s*([A-Z0-9]+)\s*[-–]\s*([0-9]+)", text)
    if m:
        ao_id = f"DAQE-{m.group(1)}-{m.group(2)}"
    issued_on = ""
    m = re.search(r"Issued On\s+([A-Za-z]+\s+\d{1,2},\s+20\d{2})", text)
    if m:
        issued_on = clean_spaces(m.group(1))
    if not issued_on:
        m = re.search(r"(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s+20\d{2}", text)
        if m:
            issued_on = clean_spaces(m.group(0))

    # Applied/NOI received date (often appears in the cover letter; sometimes appears near the end)
    applied_on = ""
    month_date = r"(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s*\s*20\d{2}"
    numeric_date = r"\d{1,2}/\d{1,2}/\d{2,4}"
    iso_date = r"20\d{2}-\d{2}-\d{2}"
    date_pat = rf"(?:{month_date}|{numeric_date}|{iso_date})"
    for pat in [
        rf"(?:Notice of Intent\s*\(NOI\)|NOI)\s*(?:application\s*)?received\s*on\s*({date_pat})",
        rf"(?:Notice of Intent\s*\(NOI\)|NOI)\s*(?:application\s*)?was\s*received\s*on\s*({date_pat})",
        rf"Application\s*(?:was\s*)?received\s*on\s*({date_pat})",
        rf"Is\s+Derived\s+From\s+NOI\s+dated\s*({date_pat})",
        rf"Derived\s+From\s+NOI\s+dated\s*({date_pat})",
        rf"NOI\s+dated\s*({date_pat})",
    ]:
        m = re.search(pat, text, flags=re.I)
        if m:
            applied_on = clean_spaces(m.group(1))
            break

    # If still blank, search the end of the PDF (some AOs place the NOI date in concluding text).
    if not applied_on and len(reader.pages) > 0:
        tail_pages = reader.pages[-5:] if len(reader.pages) >= 5 else reader.pages
        for page in tail_pages:
            t = page.extract_text() or ""
            if not t.strip():
                continue
            for pat in [
                rf"Is\s+Derived\s+From\s+NOI\s+dated\s*({date_pat})",
                rf"Derived\s+From\s+NOI\s+dated\s*({date_pat})",
                rf"(?:Notice of Intent\s*\(NOI\)|NOI)\s*(?:application\s*)?received\s*on\s*({date_pat})",
                rf"(?:Notice of Intent\s*\(NOI\)|NOI)\s*(?:application\s*)?was\s*received\s*on\s*({date_pat})",
                rf"Application\s*(?:was\s*)?received\s*on\s*({date_pat})",
                rf"NOI\s+dated\s*({date_pat})",
            ]:
                m = re.search(pat, t, flags=re.I)
                if m:
                    applied_on = clean_spaces(m.group(1))
                    break
            if applied_on:
                break

    # If extraction looks garbled and the date wasn't found, OCR the first page.
    if not applied_on and _looks_like_garbled_extraction(text):
        applied_on = _ocr_applied_on_from_pdf_bytes(pdf_bytes, date_pat) or ""
    sic_code = ""
    m = re.search(r"SIC code[: ]*\s*([0-9]{4})", text, flags=re.I)
    if m:
        sic_code = m.group(1)
    contact_name = ""
    contact_phone = ""
    contact_email = ""
    m = re.search(r"Source Contact", text, flags=re.I)
    contact_window = ""
    if m:
        contact_window = text[m.start():m.start()+500]
    if contact_window:
        m_name = re.search(r"Name\s*:\s*([^\n]+)", contact_window, flags=re.I)
        if m_name:
            nm = clean_spaces(m_name.group(1))
            nm = re.sub(r"\s+[0-9].*", "", nm)
            contact_name = nm
        m_phone = re.search(r"\(?\d{3}\)?\s*\d{3}\s*[- ]?\s*\d{4}", contact_window)
        if m_phone:
            ph = clean_phone(m_phone.group(0))
            if ph:
                contact_phone = ph
        m_email = re.search(r"Email\s*:\s*([^\s]+)", contact_window, flags=re.I)
        if m_email:
            contact_email = clean_email(m_email.group(1))
    if not contact_name:
        m = re.search(r"Name\s*:\s*([A-Za-z .'-]+)", text, flags=re.I)
        if m:
            contact_name = clean_spaces(m.group(1))
    if not contact_phone:
        ph_line = find_after(text, r"Phone\s*:")
        if ph_line:
            m = re.search(r"\(?\d{3}\)?\s*\d{3}\s*[- ]?\s*\d{4}", ph_line)
            if not m:
                m = re.search(r"\d{3}[- ]?\d{3}[- ]?\d{4}", ph_line)
            if m:
                contact_phone = clean_phone(m.group(0))
    if not contact_email:
        m = re.search(r"Email\s*:\s*([^\s]+)", text, flags=re.I)
        if m:
            contact_email = clean_email(m.group(1))
    utm_e = utm_n = utm_zone = utm_datum = ""
    m = re.search(r"([0-9][0-9,]+)\s*m Easting", text)
    if m:
        utm_e = m.group(1).replace(",", "")
    m = re.search(r"([0-9][0-9,]+)\s*m Northing", text)
    if m:
        utm_n = m.group(1).replace(",", "")
    m = re.search(r"UTM Zone\s*([0-9]+)", text, flags=re.I)
    if m:
        utm_zone = m.group(1)
    m = re.search(r"Datum\s*([A-Za-z0-9]+)", text, flags=re.I)
    if m:
        utm_datum = m.group(1)
    emissions = parse_summary_emissions(text)
    abstract = clean_spaces(find_between(text, r"Abstract", r"GENERAL INFORMATION|CONTACT/LOCATION INFORMATION|SUMMARY OF EMISSIONS|SECTION I|DAQE"))
    gen_desc = clean_spaces(find_between(text, r"General Description", r"NSR Classification"))
    nsr_class = infer_nsr_classification(text, emissions=emissions)
    source_class = clean_spaces(find_between(text, r"Source Classification", r"Applicable Federal Standards"))
    app_fed = clean_spaces(find_between(text, r"Applicable Federal Standards", r"Project Description"))
    proj_desc = clean_spaces(find_between(text, r"Project Description", r"SUMMARY OF EMISSIONS"))
    proj_desc = re.sub(r"DAQE\s*[-A-Z0-9 ]+Page\s*\d+", "", proj_desc, flags=re.I).strip()
    if abstract:
        if not gen_desc:
            gen_desc = abstract
        if not source_class:
            m = re.search(r"The plant is located in ([^.]+)", abstract, flags=re.I)
            if m:
                source_class = clean_spaces(m.group(1))
        pass
    return {
        "ApprovalOrderID": ao_id,
        "AppliedOnPdf": applied_on,
        "IssuedOnPdf": issued_on,
        "SIC_Code": sic_code,
        "SourceContactName": contact_name,
        "SourceContactPhone": contact_phone,
        "SourceContactEmail": contact_email,
        "UTM_Easting": utm_e,
        "UTM_Northing": utm_n,
        "UTM_Zone": utm_zone,
        "UTM_Datum": utm_datum,
        "GeneralDescription": gen_desc,
        "NSR_Classification": nsr_class,
        "Source_Classification": source_class,
        "Applicable_Federal_Standards": app_fed,
        "Project_Description": proj_desc,
        "Project_CO2e_TPY": emissions.get("Project_CO2e_TPY", ""),
        "Project_CO_TPY": emissions.get("Project_CO_TPY", ""),
        "Project_NOx_TPY": emissions.get("Project_NOx_TPY", ""),
        "Project_PM10_TPY": emissions.get("Project_PM10_TPY", ""),
        "Project_PM25_TPY": emissions.get("Project_PM25_TPY", ""),
        "Project_SO2_TPY": emissions.get("Project_SO2_TPY", ""),
        "Project_VOC_TPY": emissions.get("Project_VOC_TPY", ""),
        "Project_Total_HAPs_TPY": emissions.get("Project_Total_HAPs_TPY", ""),
        "Source_CO2e_TPY": emissions.get("Source_CO2e_TPY", ""),
        "Source_CO_TPY": emissions.get("Source_CO_TPY", ""),
        "Source_NOx_TPY": emissions.get("Source_NOx_TPY", ""),
        "Source_PM10_TPY": emissions.get("Source_PM10_TPY", ""),
        "Source_PM25_TPY": emissions.get("Source_PM25_TPY", ""),
        "Source_SO2_TPY": emissions.get("Source_SO2_TPY", ""),
        "Source_VOC_TPY": emissions.get("Source_VOC_TPY", ""),
        "Source_Total_HAPs_TPY": emissions.get("Source_Total_HAPs_TPY", ""),
    }


def fetch_listing():
    cj = CookieJar()
    # Ignore proxy env vars by default (this environment sets a dead proxy at 127.0.0.1:9).
    opener = build_opener(ProxyHandler({}), HTTPCookieProcessor(cj))
    page = opener.open(LIST_URL).read().decode("utf-8", errors="ignore")
    m = re.search(r'name="_csrf" value="([^"]+)"', page)
    token = m.group(1) if m else ""
    body = urlencode({
        "reportType": "aosissued",
        "startDate": '"07/01/1900"',
        "endDate": "",
        "_csrf": token,
    }).encode("utf-8")
    req = Request(AJAX_URL, data=body, headers={"Content-Type": "application/x-www-form-urlencoded"})
    data = opener.open(req).read().decode("utf-8")
    payload = json.loads(data)
    return opener, payload.get("data", [])


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default=OUT_CSV, help="Output CSV path")
    parser.add_argument("--max-permits", type=int, default=MAX_PERMITS, help="Limit number of permits processed (for testing)")
    args = parser.parse_args(argv)

    opener, items = fetch_listing()
    rows = []
    total = len(items)
    warned_dependency = False

    def default_parsed():
        return {k: "" for k in [
            "ApprovalOrderID","AppliedOnPdf","IssuedOnPdf","SIC_Code","SourceContactName","SourceContactPhone","SourceContactEmail","UTM_Easting","UTM_Northing","UTM_Zone","UTM_Datum","GeneralDescription","NSR_Classification","Source_Classification","Applicable_Federal_Standards","Project_Description","Project_CO2e_TPY","Project_CO_TPY","Project_NOx_TPY","Project_PM10_TPY","Project_PM25_TPY","Project_SO2_TPY","Project_VOC_TPY","Project_Total_HAPs_TPY","Source_CO2e_TPY","Source_CO_TPY","Source_NOx_TPY","Source_PM10_TPY","Source_PM25_TPY","Source_SO2_TPY","Source_VOC_TPY","Source_Total_HAPs_TPY"
        ]}

    def process_item(idx_item):
        nonlocal warned_dependency
        idx, item = idx_item
        intDocID = item.get("intDocID")
        if not intDocID:
            return None
        pdf_url = f"{BASE}/DocViewer?IntDocID={intDocID}&contentType=application/pdf"
        start = time.time()
        parsed = default_parsed()
        try:
            pdf_bytes = opener.open(pdf_url, timeout=20).read()
            if PER_PERMIT_TIMEOUT_SEC is None or (time.time() - start) < PER_PERMIT_TIMEOUT_SEC:
                parsed = parse_pdf_v2(pdf_bytes)
        except DependencyError:
            if not warned_dependency:
                warned_dependency = True
                print(
                    "Encountered an AES-encrypted PDF that requires `cryptography>=3.1` for pypdf. "
                    "Install with `pip install cryptography` to reduce blank/unknown PDF-derived fields.",
                    file=sys.stderr,
                    flush=True,
                )
        except Exception:
            pass
        ao_id_final = parsed.get("ApprovalOrderID") or ""
        issued_on = (item.get("aoIssuedDate") or "") or parsed.get("IssuedOnPdf")
        applied_on = parsed.get("AppliedOnPdf", "")
        street = clean_spaces(" ".join(filter(None, [item.get("physicalAddressLine1",""), item.get("physicalAddressLine2",""), item.get("physicalAddressLine3","")])))
        city_state_zip = clean_spaces(" ".join([item.get("physicalAddressMunicipality",""), item.get("physicalAddressStateCode",""), item.get("physicalAddressZip","")]))
        city = state = zipc = ""
        m = re.match(r"(.+?),\s*([A-Z]{2})\s*(\d{5})?", city_state_zip)
        if m:
            city = m.group(1)
            state = m.group(2)
            zipc = m.group(3) or ""
        row = {
            "ApprovalOrderID": ao_id_final,
            "AppliedOn": applied_on,
            "IssuedOn": issued_on,
            "PDFLink": pdf_url,
            "OwnerName": item.get("masterOrgName",""),
            "SourceName": item.get("masterAiName",""),
            "PhysicalStreet": street,
            "PhysicalCity": city,
            "PhysicalState": state,
            "PhysicalZip": zipc,
            "SourceContactName": parsed.get("SourceContactName",""),
            "SourceContactPhone": parsed.get("SourceContactPhone",""),
            "SourceContactEmail": parsed.get("SourceContactEmail",""),
            "UTM_Easting": parsed.get("UTM_Easting",""),
            "UTM_Northing": parsed.get("UTM_Northing",""),
            "UTM_Zone": parsed.get("UTM_Zone",""),
            "UTM_Datum": parsed.get("UTM_Datum",""),
            "SIC_Code": parsed.get("SIC_Code",""),
            "GeneralDescription": parsed.get("GeneralDescription",""),
            "NSR_Classification": parsed.get("NSR_Classification",""),
            "Source_Classification": parsed.get("Source_Classification",""),
            "Applicable_Federal_Standards": parsed.get("Applicable_Federal_Standards",""),
            "Project_Description": parsed.get("Project_Description",""),
            "Project_CO2e_TPY": parsed.get("Project_CO2e_TPY",""),
            "Project_CO_TPY": parsed.get("Project_CO_TPY",""),
            "Project_NOx_TPY": parsed.get("Project_NOx_TPY",""),
            "Project_PM10_TPY": parsed.get("Project_PM10_TPY",""),
            "Project_PM25_TPY": parsed.get("Project_PM25_TPY",""),
            "Project_SO2_TPY": parsed.get("Project_SO2_TPY",""),
            "Project_VOC_TPY": parsed.get("Project_VOC_TPY",""),
            "Project_Total_HAPs_TPY": parsed.get("Project_Total_HAPs_TPY",""),
            "Source_CO2e_TPY": parsed.get("Source_CO2e_TPY",""),
            "Source_CO_TPY": parsed.get("Source_CO_TPY",""),
            "Source_NOx_TPY": parsed.get("Source_NOx_TPY",""),
            "Source_PM10_TPY": parsed.get("Source_PM10_TPY",""),
            "Source_PM25_TPY": parsed.get("Source_PM25_TPY",""),
            "Source_SO2_TPY": parsed.get("Source_SO2_TPY",""),
            "Source_VOC_TPY": parsed.get("Source_VOC_TPY",""),
            "Source_Total_HAPs_TPY": parsed.get("Source_Total_HAPs_TPY",""),
        }
        return idx, intDocID, row

    # Prepare output file with header
    with open(args.out, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()

    buffer = []
    buffer_flush_size = 50
    completed_count = 0

    def flush_buffer():
        nonlocal buffer
        if not buffer:
            return
        with open(args.out, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writerows(buffer)
        buffer = []

    # Sequential processing to avoid rare hangs from worker threads
    iter_items = enumerate(items, 1)
    if args.max_permits:
        iter_items = enumerate(items[: args.max_permits], 1)

    for idx, item in iter_items:
        res = process_item((idx, item))
        if res:
            _, intDocID, row = res
            rows.append(row)
            buffer.append(row)
            completed_count += 1
            if completed_count % buffer_flush_size == 0:
                flush_buffer()
        if completed_count % 25 == 0:
            print(f"Progress checkpoint: {completed_count} permits", flush=True)

    flush_buffer()
    print(f"Wrote {len(rows)} rows to {args.out}")

if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
