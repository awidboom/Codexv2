import csv
import json
import re
import socket
import time
from io import BytesIO
from urllib.parse import urlencode
from urllib.request import build_opener, HTTPCookieProcessor, Request, urlopen
from http.cookiejar import CookieJar
from PyPDF2 import PdfReader

FIELDNAMES = [
    "ApprovalOrderID",
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
    "CO2e_TPY",
    "CO_TPY",
    "NOx_TPY",
    "PM10_TPY",
    "PM25_TPY",
    "SO2_TPY",
    "VOC_TPY",
    "Total_HAPs_TPY",
]

BASE = "https://daqpermitting.utah.gov"
LIST_URL = BASE + "/AOsIssuedAll"
AJAX_URL = BASE + "/ajax_report_data"
socket.setdefaulttimeout(60)
PER_PERMIT_TIMEOUT_SEC = None  # None to disable per-permit parse timeout
MAX_PERMITS = 10  # set to an int for quick smoke test; None means full run

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
    # General info block
    sic_code = ""
    m = re.search(r"SIC code\s*([0-9]{4})", text)
    if m:
        sic_code = m.group(1)
    contact_name = ""
    contact_phone = ""
    contact_email = ""
    # Source Contact window
    m = re.search(r"Source Contact", text, flags=re.I)
    contact_window = ""
    if m:
        contact_window = text[m.start():m.start()+400]
    if contact_window:
        m_name = re.search(r"Name\s*:\s*([^\n]+)", contact_window, flags=re.I)
        if m_name:
            contact_name = clean_spaces(m_name.group(1))
        m_phone = re.search(r"Phone\s*:\s*([0-9(). +\\-]+)", contact_window, flags=re.I)
        if m_phone:
            ph = clean_phone(m_phone.group(1))
            if ph:
                contact_phone = ph
        m_email = re.search(r"Email\s*:\s*([^\s]+)", contact_window, flags=re.I)
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
        m = re.search(r"Email\s*:\s*([^\s]+)", text, flags=re.I)
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
    # Initialize emission placeholders
    co2e = co = nox = pm10 = pm25 = so2 = voc = total_haps = ""

    # Descriptions (prefer last occurrence to avoid table of contents)
    abstract = clean_spaces(find_between(text, r"Abstract", r"GENERAL INFORMATION|CONTACT/LOCATION INFORMATION|SUMMARY OF EMISSIONS|SECTION I|DAQE"))
    gen_desc = clean_spaces(find_between(text, r"General Description", r"NSR Classification"))
    nsr_class = clean_spaces(find_between(text, r"NSR Classification", r"Source Classification"))
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
        # Emissions from abstract "The new PTE ..."
        for label, key in [
            ("CO2e", "CO2e_TPY"),
            ("CO", "CO_TPY"),
            ("NOx", "NOx_TPY"),
            ("PM10", "PM10_TPY"),
            ("PM2.5", "PM25_TPY"),
            ("SO2", "SO2_TPY"),
            ("VOC", "VOC_TPY"),
            ("Total HAPs", "Total_HAPs_TPY"),
        ]:
            val = find_number(abstract, label)
            if val != "":
                if key == "PM25_TPY":
                    pm25 = val
                elif key == "PM10_TPY":
                    pm10 = val
                elif key == "CO2e_TPY":
                    co2e = val
                elif key == "CO_TPY":
                    co = val
                elif key == "NOx_TPY":
                    nox = val
                elif key == "SO2_TPY":
                    so2 = val
                elif key == "VOC_TPY":
                    voc = val
                elif key == "Total_HAPs_TPY":
                    total_haps = val
    # Emissions
    # Limit emissions search to the summary section if present
    emissions_text = find_between(text, r"SUMMARY OF EMISSIONS", r"SECTION|SECTION I|SECTION  I|SECTION II")
    search_area = emissions_text if emissions_text else text
    if co2e == "":
        co2e = find_number(search_area, r"CO\s*2\s*Equivalent")
    if co == "":
        co = find_number(search_area, r"Carbon Monoxide")
    if nox == "":
        nox = find_number(search_area, r"Nitrogen Oxides")
    if pm10 == "":
        pm10 = find_number(search_area, r"PM\s*10")
    if pm25 == "":
        pm25 = find_number(search_area, r"PM\s*2\.5")
    if so2 == "":
        so2 = find_number(search_area, r"Sulfur Dioxide")
    if voc == "":
        voc = find_number(search_area, r"Volatile Organic Compounds")
    if total_haps == "":
        total_haps = find_number(search_area, r"Total HAPs")
    return {
        "ApprovalOrderID": ao_id,
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
        "CO2e_TPY": co2e,
        "CO_TPY": co,
        "NOx_TPY": nox,
        "PM10_TPY": pm10,
        "PM25_TPY": pm25,
        "SO2_TPY": so2,
        "VOC_TPY": voc,
        "Total_HAPs_TPY": total_haps,
    }


def fetch_listing():
    cj = CookieJar()
    opener = build_opener(HTTPCookieProcessor(cj))
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


def main():
    opener, items = fetch_listing()
    rows = []
    total = len(items)

    def default_parsed():
        return {k: "" for k in [
            "ApprovalOrderID","IssuedOnPdf","SIC_Code","SourceContactName","SourceContactPhone","SourceContactEmail","UTM_Easting","UTM_Northing","UTM_Zone","UTM_Datum","GeneralDescription","NSR_Classification","Source_Classification","Applicable_Federal_Standards","Project_Description","CO2e_TPY","CO_TPY","NOx_TPY","PM10_TPY","PM25_TPY","SO2_TPY","VOC_TPY","Total_HAPs_TPY"
        ]}

    def process_item(idx_item):
        idx, item = idx_item
        intDocID = item.get("intDocID")
        if not intDocID:
            return None
        pdf_url = f"{BASE}/DocViewer?IntDocID={intDocID}&contentType=application/pdf"
        start = time.time()
        parsed = default_parsed()
        try:
            pdf_bytes = urlopen(pdf_url, timeout=20).read()
            if PER_PERMIT_TIMEOUT_SEC is None or (time.time() - start) < PER_PERMIT_TIMEOUT_SEC:
                parsed = parse_pdf(pdf_bytes)
        except Exception:
            pass
        ao_id_final = parsed.get("ApprovalOrderID") or ""
        issued_on = (item.get("aoIssuedDate") or "") or parsed.get("IssuedOnPdf")
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
            "CO2e_TPY": parsed.get("CO2e_TPY",""),
            "CO_TPY": parsed.get("CO_TPY",""),
            "NOx_TPY": parsed.get("NOx_TPY",""),
            "PM10_TPY": parsed.get("PM10_TPY",""),
            "PM25_TPY": parsed.get("PM25_TPY",""),
            "SO2_TPY": parsed.get("SO2_TPY",""),
            "VOC_TPY": parsed.get("VOC_TPY",""),
            "Total_HAPs_TPY": parsed.get("Total_HAPs_TPY",""),
        }
        return idx, intDocID, row

    # Prepare output file with header
    with open("permits_all.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()

    buffer = []
    buffer_flush_size = 50
    completed_count = 0

    def flush_buffer():
        nonlocal buffer
        if not buffer:
            return
        with open("permits_all.csv", "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writerows(buffer)
        buffer = []

    # Sequential processing to avoid rare hangs from worker threads
    iter_items = enumerate(items, 1)
    if MAX_PERMITS:
        iter_items = enumerate(items[:MAX_PERMITS], 1)

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
    print(f"Wrote {len(rows)} rows to permits_all.csv")

if __name__ == "__main__":
    main()
