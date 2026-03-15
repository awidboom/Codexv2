import argparse
import csv
import hashlib
import re
from pathlib import Path

from pypdf import PdfReader

DEFAULT_DOWNLOAD_DIR = Path(__file__).resolve().parent / "downloads"
DEFAULT_MANIFEST_NAME = "cdphe_download_manifest.csv"
DEFAULT_OUTPUT_NAME = "cdphe_enforcement_summary.csv"
DOWNLOAD_DIR = DEFAULT_DOWNLOAD_DIR
MANIFEST_CSV = DOWNLOAD_DIR / DEFAULT_MANIFEST_NAME
OUTPUT_CSV = DOWNLOAD_DIR / DEFAULT_OUTPUT_NAME
CLEANUP_PDFS = False
MANIFEST_ONLY = False

FOOTER_PHRASES = [
    "4300 Cherry Creek Drive",
    "www.colorado.gov/cdphe",
    "Jared Polis",
    "Jill Hunsaker Ryan",
    "Executive Director",
]

STOP_PHRASES = [
    "the division encourages",
    "the division requests",
    "the division also requests",
    "if you have any questions",
    "it is important to resolve",
    "therefore,",
    "please be aware",
    "the option to install",
    "the regulation referenced",
]

STOP_PATTERNS = [
    r"\b\d+\s+The option",
    r"\b\d+\s+The regulation",
    r"\bTherefore\b",
]

CITATION_KEYWORDS = ["aqcc", "permit", "cfr", "c.r.s", "nsps"]


def normalize_text(text: str) -> str:
    cleaned = (text or "")
    cleaned = cleaned.replace("壯", "§").replace("\u0e07", "§")
    return re.sub(r"\s+", " ", cleaned).strip()


def drop_footer_lines(text: str) -> str:
    lines = []
    for line in (text or "").splitlines():
        if any(phrase in line for phrase in FOOTER_PHRASES):
            continue
        lines.append(line)
    return "\n".join(lines)


def trim_stop_phrases(text: str) -> str:
    lowered = text.lower()
    for phrase in STOP_PHRASES:
        idx = lowered.find(phrase)
        if idx > -1:
            return text[:idx].strip()
    for pat in STOP_PATTERNS:
        m = re.search(pat, text, flags=re.IGNORECASE)
        if m:
            return text[: m.start()].strip()
    return text.strip()


def shorten_violation(text: str) -> str:
    sentences = re.split(r"(?<=\.)\s+", text)
    for marker in ["failed", "violating"]:
        for sentence in sentences:
            if marker in sentence.lower():
                return sentence.strip()
    return text.strip()


def extract_text(pdf_path: Path) -> str:
    try:
        reader = PdfReader(str(pdf_path))
    except Exception as exc:
        print(f"PDF open failed {pdf_path}: {exc}")
        return ""

    parts = []
    for page in reader.pages:
        try:
            parts.append(page.extract_text() or "")
        except Exception:
            parts.append("")
    return "\n".join(parts)


def find_first(patterns, text: str) -> str:
    for pat in patterns:
        m = re.search(pat, text, flags=re.IGNORECASE)
        if m:
            return normalize_text(m.group(1))
    return ""


def detect_enforcement_type(text: str) -> str:
    rules = [
        ("Enforcement Discretion", [r"enforcement discretion"]),
        ("Early Settlement Agreement", [r"early settlement agreement", r"proposed early settlement agreement"]),
        (
            "Voluntary Self-Audit",
            [r"voluntary self[- ]audit", r"self[- ]audit review and determination", r"review and determination for"],
        ),
        ("Notice of Violation", [r"notice of violation", r"\bnov\b"]),
        ("Compliance Advisory", [r"compliance advisory"]),
        ("Administrative Order", [r"administrative order", r"order on consent", r"consent order", r"final order"]),
        ("Penalty Assessment", [r"penalty assessment", r"civil penalty", r"administrative penalty"]),
        ("Cease and Desist", [r"cease and desist"]),
        ("Settlement Agreement", [r"settlement agreement", r"settlement"]),
        ("Warning Letter", [r"warning letter"]),
        (
            "Correspondence",
            [
                r"\bFrom:\b[^\n]*@[^\n]+",
                r"\bTo:\b[^\n]*@[^\n]+",
                r"\bSubject:\b",
            ],
        ),
    ]
    for label, patterns in rules:
        if any(re.search(pat, text, flags=re.IGNORECASE) for pat in patterns):
            return label
    return ""


def extract_penalty(text: str) -> str:
    amounts = []
    for m in re.finditer(r"\$[\d,]+(?:\.\d{2})?", text):
        window = text[max(m.start() - 80, 0) : m.end() + 80].lower()
        if any(k in window for k in ["penalty", "civil", "fine", "settlement", "stipulated", "payment", "assessment"]):
            amounts.append(m.group(0))

    if not amounts:
        amounts = re.findall(r"\$[\d,]+(?:\.\d{2})?", text)

    if not amounts:
        return ""

    def to_num(value: str) -> float:
        return float(value.replace("$", "").replace(",", ""))

    try:
        return max(amounts, key=to_num)
    except Exception:
        return amounts[0]


def extract_company(text: str, fallback: str) -> str:
    patterns = [
        r"\bIn the Matter of\b\s*[:\-]?\s*([^\n]+)",
        r"\bReview and Determination for\b\s*([^\n]+)",
        r"\bVoluntary Self-Audit Review and Determination for\b\s*([^\n]+)",
        r"\bProposed Early Settlement Agreement\b.*?\bIn the Matter of\b\s*([^\n]+)",
        r"\bWarning Letter to\b\s+([^\n]+)",
        r"\bRE:\s*(?:Warning Letter to\s*)?([^\n]+?)\s+regarding\b",
        r"\bRE:\s*(?:Warning Letter to\s*)?([^\n]+)",
        r"Respondent\s*[:\-]\s*([^\n]+)",
        r"Company\s*[:\-]\s*([^\n]+)",
        r"Owner/Operator\s*[:\-]\s*([^\n]+)",
        r"Facility Name\s*[:\-]\s*([^\n]+)",
    ]
    company = find_first(patterns, text)
    if company:
        company = re.sub(r"^.*?\bfor\b\s+", "", company, flags=re.IGNORECASE).strip()
        company = re.sub(r"\s+regarding\b.*", "", company, flags=re.IGNORECASE).strip()
        company = re.split(r"\s{2,}|Case No\.|Case Number|Order No\.|File No\.|Document ID", company)[0].strip()
        return company
    facility_section = extract_facility_info_section(text)
    if facility_section:
        first_line = (facility_section.strip().splitlines() or [""])[0].strip()
        candidate = normalize_text(first_line)
        candidate = re.split(r"\s*\(|\s+owns and operates\b", candidate, maxsplit=1, flags=re.IGNORECASE)[0].strip(" ,")
        if candidate and len(candidate) >= 3:
            return candidate
    return fallback or ""


def extract_facility_name(text: str) -> str:
    facility_section = extract_facility_info_section(text) or ""
    facility_cleaned = normalize_text(facility_section)
    if facility_cleaned:
        m = re.search(r"owns and operates\s+([A-Za-z0-9\-/ ]+?)\s*\(Facility\)", facility_cleaned, flags=re.IGNORECASE)
        if m:
            return m.group(1).strip(" ,")
        m = re.search(
            r"known as\s+(?:the\s+)?(.+?)(?:\s+located|\s+in\s+[A-Za-z\s]+ County|,|\.|$)",
            facility_cleaned,
            flags=re.IGNORECASE,
        )
        if m:
            return m.group(1).strip(" ,")
        m = re.search(
            r"owns and operates\s+the\s+(.+?)\s+(?:oil and gas production facility|natural gas liquids fractionation, storage and distribution facility|produced water management facility|central production facility|gas processing facility|processing facility|fractionation facility|compressor station|production facility|facility)\b",
            facility_cleaned,
            flags=re.IGNORECASE,
        )
        if m:
            return m.group(1).strip(" ,")
        m = re.search(r"owns and operates\s+([^,]+)", facility_cleaned, flags=re.IGNORECASE)
        if m:
            return m.group(1).strip(" ,")
        m = re.search(r"\(([^)]+)\)\s*Facility", facility_cleaned, flags=re.IGNORECASE)
        if m:
            return m.group(1).strip(" ,")

    patterns = [
        r"Facility Name\s*[:\-]\s*([^\n]+)",
    ]
    name = find_first(patterns, text)
    if name:
        return name
    return ""


def parse_date_string(value: str) -> str:
    value = (value or "").strip()
    if not value:
        return ""
    m = re.match(r"(\d{1,2})/(\d{1,2})/(\d{2,4})", value)
    if m:
        mm, dd, yy = m.groups()
        yyyy = int(yy) if len(yy) == 4 else 2000 + int(yy)
        return f"{yyyy:04d}-{int(mm):02d}-{int(dd):02d}"
    m = re.match(r"([A-Za-z]+)\s+(\d{1,2}),\s*(\d{4})", value)
    if m:
        months = {
            "january": 1,
            "february": 2,
            "march": 3,
            "april": 4,
            "may": 5,
            "june": 6,
            "july": 7,
            "august": 8,
            "september": 9,
            "october": 10,
            "november": 11,
            "december": 12,
        }
        month = months.get(m.group(1).lower())
        if month:
            return f"{int(m.group(3)):04d}-{month:02d}-{int(m.group(2)):02d}"
    return value


def extract_inspection_date(text: str) -> str:
    if not text:
        return ""
    matches = []
    date_re = r"[A-Za-z]+\s+\d{1,2},\s*\d{4}|\d{1,2}/\d{1,2}/\d{2,4}"

    header_match = re.search(
        rf"Inspection Date[s]?\s*:\s*(?P<d1>{date_re})(?:\s*(?:and|,)?\s*(?P<d2>{date_re}))?",
        text,
        flags=re.IGNORECASE,
    )
    if header_match:
        for key in ("d1", "d2"):
            if header_match.group(key):
                matches.append(parse_date_string(header_match.group(key)))

    for m in re.finditer(r"inspected[^\.]{0,120}? on ([A-Za-z]+\s+\d{1,2},\s*\d{4})", text, flags=re.IGNORECASE):
        matches.append(parse_date_string(m.group(1)))
    for m in re.finditer(r"inspected[^\.]{0,120}? on (\d{1,2}/\d{1,2}/\d{2,4})", text, flags=re.IGNORECASE):
        matches.append(parse_date_string(m.group(1)))

    deduped = []
    for item in matches:
        if item and item not in deduped:
            deduped.append(item)

    normalized = [d for d in deduped if re.match(r"\d{4}-\d{2}-\d{2}$", d)]
    if not normalized:
        return ""
    return min(normalized)


def extract_violation_section(text: str) -> str:
    if not text:
        return ""
    patterns = [
        r"(?:^|\n)\s*III\.\s*Alleged Violations.*?(?:\n| )(.+?)(?:\n\s*IV\.\s|\n\s*Conclusion\b|\n\s*Requested Action\b|$)",
        r"(?:^|\n)\s*Alleged Violations.*?(?:\n| )(.+?)(?:\n\s*[IVX]+\.\s|\n\s*Conclusion\b|\n\s*Requested Action\b|$)",
        r"(?:^|\n)\s*Violations and Facts.*?(?:\n| )(.+?)(?:\n\s*[IVX]+\.\s|\n\s*Conclusion\b|\n\s*Requested Action\b|$)",
        r"(?:^|\n)\s*Findings of Fact.*?(?:\n| )(.+?)(?:\n\s*[IVX]+\.\s|\n\s*Conclusion\b|\n\s*Requested Action\b|$)",
        r"(?:^|\n)\s*Determination of Potential Violations.*?(?:\n| )(.+?)(?:\n\s*[IVX]+\.\s|\n\s*Conclusion\b|\n\s*Requested Action\b|$)",
    ]
    for pat in patterns:
        m = re.search(pat, text, flags=re.IGNORECASE | re.DOTALL)
        if m:
            return drop_footer_lines(m.group(1))
    return drop_footer_lines(text)


def split_violations(section_text: str) -> list:
    if not section_text:
        return []

    cleaned = section_text
    lettered = re.findall(r"\n\s*([A-Z])\.\s+(.+?)(?=\n\s*[A-Z]\.\s+|$)", cleaned, flags=re.DOTALL)
    if lettered:
        return [(letter, normalize_text(body)) for letter, body in lettered]

    numbered = re.findall(r"\n\s*(\d+)\.\s+(.+?)(?=\n\s*\d+\.\s+|$)", cleaned, flags=re.DOTALL)
    if numbered:
        return [(num, normalize_text(body)) for num, body in numbered]

    return [("", normalize_text(cleaned))]


def extract_facility_info_section(text: str) -> str:
    if not text:
        return ""
    patterns = [
        r"Facility Information\s*(.+?)(?:\n\s*III\.|\n\s*IV\.|\n\s*Alleged Violations|\n\s*Violations and Facts|$)",
    ]
    for pat in patterns:
        m = re.search(pat, text, flags=re.IGNORECASE | re.DOTALL)
        if m:
            return m.group(1)
    return ""


def build_equipment_table(text: str) -> dict:
    if not text:
        return {}
    table_match = re.search(
        r"(Table\s*\d+\s*[:\-]?\s*Equipment Description.*?)(?:\n\s*Table\s*\d+|\n\s*III\.|\n\s*Alleged Violations|\n\s*Violations and Facts|$)",
        text,
        flags=re.IGNORECASE | re.DOTALL,
    )
    chunk = ""
    if table_match:
        chunk = table_match.group(1)
    else:
        header_match = re.search(r"Equipment Description", text, flags=re.IGNORECASE)
        if header_match:
            start = max(header_match.start() - 200, 0)
            chunk = text[start : start + 2000]
        else:
            table1_match = re.search(r"(Table\s*1:.*?)(?:\n\s*Table\s*\d+|\n\s*III\.|\n\s*Alleged Violations|\n\s*Violations and Facts|$)", text, flags=re.IGNORECASE | re.DOTALL)
            if table1_match and "airs" in table1_match.group(1).lower():
                chunk = table1_match.group(1)

    if not chunk:
        return {}

    mapping = {}
    lines = [normalize_text(raw_line) for raw_line in chunk.splitlines()]

    def is_header(line: str) -> bool:
        lower = line.lower()
        if lower in {"airs", "point", "permit", "number", "description"}:
            return True
        return (
            "equipment description" in lower
            or "emissions control" in lower
            or "permit number" in lower
            or "airs point" in lower
        )

    def is_point_only(line: str) -> bool:
        return bool(re.match(r"^\d{2,3}$", line))

    def collect_desc(start_idx: int) -> tuple[list[str], int]:
        parts = []
        j = start_idx
        while j < len(lines):
            candidate = lines[j]
            if not candidate:
                if parts:
                    j += 1
                    continue
                j += 1
                continue
            lower = candidate.lower()
            if is_point_only(candidate):
                break
            if is_header(candidate):
                if parts:
                    break
                j += 1
                continue
            if "enclosed flare" in lower or "control device" in lower:
                if parts:
                    break
            if re.search(r"\b\d{2}[A-Z]{2,}\d{3,}\b", candidate) and ("permit" in lower or "flare" in lower):
                if parts:
                    break
            parts.append(candidate)
            j += 1
        return parts, j

    i = 0
    while i < len(lines):
        line = lines[i]
        if not line or is_header(line):
            i += 1
            continue

        point_id = None
        desc_parts = []

        m = re.search(
            r"AIRS\s*(?:Point|Pt\.?)\s*(?:ID)?\s*([0-9]{2,3})\b.*?Equipment Description\s*[:\-]?\s*(.+)",
            line,
            flags=re.IGNORECASE,
        )
        if m:
            try:
                point_id = int(m.group(1))
            except ValueError:
                point_id = None
            desc_parts = [m.group(2)]
            extra, j = collect_desc(i + 1)
            desc_parts.extend(extra)
            i = j
        else:
            m = re.search(r"AIRS\s*(?:Point|Pt\.?)\s*(?:ID)?\s*([0-9]{2,3})\b", line, flags=re.IGNORECASE)
            if m:
                try:
                    point_id = int(m.group(1))
                except ValueError:
                    point_id = None
                desc_line = re.sub(
                    r".*?AIRS\s*(?:Point|Pt\.?)\s*(?:ID)?\s*[0-9]{2,3}\s*[:\-]?\s*",
                    "",
                    line,
                    flags=re.IGNORECASE,
                )
                desc_parts = [desc_line] if desc_line else []
                extra, j = collect_desc(i + 1)
                desc_parts.extend(extra)
                i = j
            elif is_point_only(line):
                try:
                    point_id = int(line)
                except ValueError:
                    point_id = None
                extra, j = collect_desc(i + 1)
                desc_parts.extend(extra)
                i = j
            else:
                m = re.search(r"^([0-9]{2,3})\s+(.+)$", line)
                if m:
                    try:
                        point_id = int(m.group(1))
                    except ValueError:
                        point_id = None
                    desc_parts = [m.group(2)]
                    extra, j = collect_desc(i + 1)
                    desc_parts.extend(extra)
                    i = j
                else:
                    i += 1
                    continue

        if point_id is None:
            continue

        desc = normalize_text(" ".join(desc_parts))
        desc = re.sub(r"^Equipment Description\s*[:\-]?\s*", "", desc, flags=re.IGNORECASE)
        desc = re.split(r"\s+Permit|\s+Emissions\s+Control", desc, maxsplit=1, flags=re.IGNORECASE)[0]
        desc = normalize_text(desc)
        if not desc:
            continue
        mapping[point_id] = desc

    return mapping


def trim_citation(text: str) -> str:
    text = re.split(r"\s+(must|shall|are|is|owners|owner|operators|operator)\b", text, maxsplit=1)[0]
    text = re.sub(
        r",\s*(?!Condition|Section|Issuance|Part|Regulation|Permit|No\.|Number|AIRS)([A-Z][A-Za-z0-9 ,&/-]+)$",
        "",
        text,
    )
    return text.strip(" ,")


def extract_permit_conditions(text: str) -> str:
    if not text:
        return ""
    found = []
    snippet = text[:500]
    pattern = r"(Permit(?: Number| No\.)?\s*[A-Za-z0-9\-]+[^\n\.]{0,120}?Condition\s*[A-Za-z0-9\.\-]+)"
    for match in re.findall(pattern, snippet, flags=re.IGNORECASE):
        cleaned = normalize_text(match)
        if cleaned not in found:
            found.append(cleaned)
    return ";".join(found)


def extract_rule_citations(text: str) -> str:
    if not text:
        return ""
    found = []
    snippet = text[:500]

    for pursuant in re.finditer(
        r"Pursuant\s+to?\s+(.+?)(?:\.|\s+must\b|\s+shall\b|\s+is\s+required\b)",
        snippet,
        flags=re.IGNORECASE,
    ):
        citation_block = trim_citation(normalize_text(pursuant.group(1)))
        if citation_block and any(k in citation_block.lower() for k in CITATION_KEYWORDS):
            if "permit" not in citation_block.lower() and citation_block not in found:
                found.append(citation_block)

    patterns = [
        r"AQCC Regulation[^\.;\n]+",
        r"\bRegulation[^\.;\n]+",
        r"NSPS[^\.;\n]+",
        r"40\s*CFR[^\.;\n]+",
        r"C\.R\.S\.[^\.;\n]+",
    ]
    for pat in patterns:
        for match in re.findall(pat, snippet, flags=re.IGNORECASE):
            cleaned = trim_citation(normalize_text(match))
            if not cleaned:
                continue
            lowered = cleaned.lower()
            if lowered.startswith("section"):
                continue
            if any(bad in lowered for bad in ["outdated", "restructured", "added", "option to install"]):
                continue
            if cleaned not in found:
                found.append(cleaned)
    return ";".join(found)


def extract_equipment_types_from_description(description: str) -> list:
    desc_l = (description or "").lower()
    rules = [
        ("engine", ["engine"]),
        ("dehydration unit", ["dehydration unit", "dehydrator"]),
        ("ECD", ["enclosed combustion device", "combustion device", "ecd"]),
        ("tank", ["storage tank", "tank battery", "tank"]),
        ("turbine", ["turbine"]),
        ("sweetening unit", ["sweetening unit", "sweetening", "amine unit", "amine system"]),
        ("pneumatic controller", ["pneumatic controller", "pneumatic control device"]),
        ("pigging operations", ["pigging operation", "pigging operations"]),
        ("catalyst", ["catalyst", "oxidation catalyst"]),
        ("fugitives", ["fugitive", "fugitives", "fugitive emissions"]),
        ("compressor", ["compressor", "compressor station"]),
        ("flare", ["flare", "flaring"]),
        ("separator", ["separator"]),
        ("pump", ["pump"]),
        ("heater", ["heater", "boiler"]),
    ]
    found = []
    for label, keywords in rules:
        if any(k in desc_l for k in keywords):
            found.append(label)
    return found


def extract_equipment_types(text: str, rule_citation: str, equipment_map: dict) -> str:
    raw_text = text or ""
    text_l = raw_text.lower()
    combined = f"{text_l} {(rule_citation or '').lower()}"
    found = extract_equipment_types_from_description(combined)

    if re.search(r"\bnsps\s*k[a-c]?\b", combined):
        found.append("tank")
    if re.search(r"\bnsps\s*(vv|vva|kkk)\b", combined):
        found.append("fugitives")

    if equipment_map:
        points = set()
        for m in re.finditer(
            r"AIRS\s*Point[s]?\s*([0-9]{2,3}(?:[^0-9]+[0-9]{2,3})*)",
            raw_text,
            flags=re.IGNORECASE,
        ):
            for num in re.findall(r"\d{2,3}", m.group(1)):
                points.add(num)
        for m in re.finditer(
            r"AIRS\s*(?:Point|Pt\.?)\s*(?:ID)?\s*([0-9]{2,3})",
            raw_text,
            flags=re.IGNORECASE,
        ):
            points.add(m.group(1))

        descs = []
        expanded_text = raw_text
        for point in sorted(points):
            try:
                point_id = int(point)
            except ValueError:
                continue
            desc = equipment_map.get(point_id)
            if desc:
                descs.append(desc)
                expanded_text = re.sub(
                    rf"(AIRS\s*(?:Point|Pt\.?)\s*(?:ID)?\s*0*{point_id}\b)",
                    rf"\\1 ({desc})",
                    expanded_text,
                    flags=re.IGNORECASE,
                )

        if descs:
            combined_with_table = f"{expanded_text.lower()} {combined} {' '.join(descs).lower()}"
            found.extend(extract_equipment_types_from_description(combined_with_table))

        if not found:
            unique_types = []
            for desc in equipment_map.values():
                unique_types.extend(extract_equipment_types_from_description(desc))
            unique_types = list(dict.fromkeys(unique_types))
            if len(unique_types) == 1:
                found.extend(unique_types)
    return ";".join(dict.fromkeys(found))


def extract_source_type(text: str, facility_name: str) -> str:
    if not text:
        return ""
    cleaned = normalize_text(text)
    facility_l = (facility_name or "").lower()
    if "compressor station" in facility_l or "compressor station" in cleaned.lower():
        return "compressor station"
    facility_section = extract_facility_info_section(text) or ""
    facility_cleaned = normalize_text(facility_section) if facility_section else ""
    sentence = facility_cleaned or cleaned
    if facility_cleaned:
        m = re.search(r"(owns and operates.+?)(?:\.|$)", facility_cleaned, flags=re.IGNORECASE)
        if m:
            sentence = m.group(1)
        else:
            m = re.search(r"(operates.+?)(?:\.|$)", facility_cleaned, flags=re.IGNORECASE)
            if m:
                sentence = m.group(1)

    owns_match = re.search(r"owns and operates\s+(?:an?|the)\s+(.+)", sentence, flags=re.IGNORECASE)
    if owns_match:
        clause = owns_match.group(1)
        clause = re.split(r"\b(?:located|known as)\b", clause, maxsplit=1, flags=re.IGNORECASE)[0]
        clause = re.split(r"\s+located\s+at|\s+located\s+in|\s+at\s+", clause, maxsplit=1, flags=re.IGNORECASE)[0]
        clause = re.sub(r"[“”\"']", "", clause).strip(" ,")
        clause = re.sub(r"\(\s*Facility\s*\)", "", clause, flags=re.IGNORECASE).strip(" ,")
        clause = normalize_text(clause)

        comma_type = re.search(
            r",\s*(?:an?|a|the)\s+([^,]+?(?:facility|equipment|plant|station))\b",
            clause,
            flags=re.IGNORECASE,
        )
        phrase = (comma_type.group(1) if comma_type else clause).strip(" ,")
        phrase_l = phrase.lower()
        if phrase_l:
            if re.fullmatch(r"(?:the\s+)?facility", phrase, flags=re.IGNORECASE):
                return ""
            if re.search(r"\bColorado\b", phrase, flags=re.IGNORECASE) and re.search(r"\bFacility\b", phrase, flags=re.IGNORECASE):
                return ""
            if "well production facility" in phrase_l or phrase_l.endswith("production facility"):
                return "oil and gas production facility"
            if "oil and gas exploration and production operation" in phrase_l:
                return "oil and gas production facility"
            if re.search(r"\bexploration\s*(?:and|&)\s*production\b", phrase_l):
                return "oil and gas production facility"
            if re.search(r"\b(?:well|production|well/production)\s+pad\b", phrase_l):
                return "oil and gas production facility"
            if "aggregate" in phrase_l and "equipment" in phrase_l:
                return "portable aggregate processing equipment" if "portable" in phrase_l else "aggregate processing equipment"
            return phrase

    patterns = [
        r"owns and operates\s+the\s+((?:oil and gas production facility|natural gas liquids fractionation, storage and distribution facility|produced water management facility|central production facility|gas processing facility|processing facility|fractionation facility|compressor station|production facility|facility))\b",
        r"owns and operates\s+the\s+.+?\s+((?:oil and gas production|natural gas liquids fractionation, storage and distribution|produced water management|central production|gas processing|processing|fractionation|compressor station|production)[^,\.]*facility)",
        r"owns and operates\s+the\s+.+?\s+([^,\.]*facility)",
        r"owns and operates\s+(?:an?|the)\s+([^,\.]*aggregate[^,\.]*equipment)",
        r"owns and operates\s+(?:an?|the)\s+([^,\.]*facility)",
        r"operates\s+(?:an?|the)\s+([^,\.]*facility)",
        r"is (?:an?|a)\s+([^,\.]*facility)",
    ]
    for pat in patterns:
        m = re.search(pat, sentence, flags=re.IGNORECASE)
        if m:
            phrase = m.group(1).strip(" ,")
            phrase = re.split(r"\s+located\s+at|\s+located\s+in|\s+at\s+", phrase, flags=re.IGNORECASE)[0]
            phrase = re.sub(r"\bknown as\b.*", "", phrase, flags=re.IGNORECASE)
            phrase = re.sub(r"\s+in\s+[A-Za-z\s]+ County.*", "", phrase, flags=re.IGNORECASE)
            phrase = re.sub(r"\s+in\s+[A-Za-z\s]+,?\s*Colorado.*", "", phrase, flags=re.IGNORECASE)
            phrase = phrase.strip(" ,")
            phrase = re.sub(r"[“”\"']", "", phrase).strip()
            phrase = re.sub(r"\(\s*Facility\s*\)", "", phrase, flags=re.IGNORECASE).strip(" ,")
            if re.fullmatch(r"(?:the\s+)?facility", phrase, flags=re.IGNORECASE):
                return ""
            if re.search(r"\bColorado\b", phrase, flags=re.IGNORECASE) and re.search(r"\bFacility\b", phrase, flags=re.IGNORECASE):
                return ""
            if "well production facility" in phrase.lower():
                return "oil and gas production facility"
            if "aggregate" in phrase.lower() and "equipment" in phrase.lower():
                return "portable aggregate processing equipment" if "portable" in phrase.lower() else "aggregate processing equipment"
            if phrase == "production facility":
                return "oil and gas production facility"
            return phrase

    if "compressor station" in facility_l:
        return "compressor station"
    if "tank battery" in facility_l:
        return "tank battery"
    if "battery" in facility_l:
        return "battery"
    if "fractionation" in facility_l:
        return "fractionation facility"
    if "processing plant" in facility_l:
        return "processing plant"
    if "gas plant" in facility_l:
        return "gas plant"
    if "station" in facility_l:
        return "station"
    if "plant" in facility_l:
        return "plant"
    if "production facility" in facility_l:
        return "oil and gas production facility"
    return ""


def categorize(text: str) -> str:
    text_l = (text or "").lower()
    categories = []

    rules = [
        ("APEN", ["apen"]),
        (
            "permitting",
            [
                "without a valid construction permit",
                "without a valid permit",
                "failed to obtain a valid construction permit",
                "failed to obtain a construction permit",
                "failed to obtain permit",
                "operating permit",
                "title v",
                "initial approval permit",
                "construction permit",
                "obtain a valid construction permit",
                "obtain a construction permit",
                "operate without a permit",
                "operated without a permit",
            ],
        ),
        ("enforcement discretion", ["enforcement discretion"]),
        ("tampering", ["tamper", "tampering", "tampered"]),
        ("testing", ["test", "stack test", "performance test", "sampling", "sample", "analyze", "analysis"]),
        (
            "monitoring",
            [
                "monitoring",
                "monitor",
                "cems",
                "flow meter",
                "pressure",
                "meter data",
                "predictive model",
                "method 9",
                "method 22",
                "opacity observation",
                "temperature",
                "avo inspection",
                "avo inspections",
                "aimm inspection",
                "aimm inspections",
            ],
        ),
        (
            "recordkeeping",
            [
                "recordkeeping",
                "record",
                "records",
                "reading",
                "readings",
                "log",
                "o&m plan",
                "o & m plan",
                "operation and maintenance plan",
                "demonstrate compliance",
                "mark the permit number",
                "mark permit number",
            ],
        ),
        (
            "reporting",
            [
                "reporting",
                "report",
                "semiannual",
                "annual",
                "deviation report",
                "self-certification",
                "self certification",
                "self- certification",
                "self-certify",
                "certify compliance",
                "demonstrate and certify compliance",
                "notice of start",
                "nos",
                "notice",
                "notices",
                "notification",
                "transfer of ownership",
                "forms",
                "submit an application",
                "information requested",
                "provide the following information",
            ],
        ),
        ("emissions", ["emission", "emit", "emitted", "vent", "venting", "exceed", "excess emissions", "opacity", "fugitive", "limit", "neshap"]),
        (
            "controls",
            [
                "control device",
                "control",
                "ecd",
                "catalyst",
                "flare",
                "combustion device",
                "dp to within",
                "vapor tight",
                "vapor recovery",
                "stage 1",
                "stage i",
                "work practices",
                "corrective action",
                "filter",
                "filters",
                "carbon filter",
                "biospark",
            ],
        ),
        ("throughput", ["throughput", "commingled liquids", "rolling 12", "bbl", "barrel"]),
    ]

    for label, keywords in rules:
        if any(k in text_l for k in keywords):
            categories.append(label)

    if not categories:
        categories = ["uncategorized"]
    return ";".join(dict.fromkeys(categories))


def parse_filename_metadata(filename: str) -> dict:
    stem = Path(filename).stem
    parts = stem.split("__")
    if len(parts) >= 3:
        return {
            "document_date": parts[0],
            "company": parts[1].replace("_", " ").strip(),
            "case_number": parts[2].replace("_", " ").strip(),
        }
    return {"document_date": "", "company": "", "case_number": ""}


def load_manifest() -> tuple[dict, list]:
    if not MANIFEST_CSV.exists():
        raise FileNotFoundError(
            f"Manifest not found: {MANIFEST_CSV}. Run cdphe_downloader.py to generate pdf_url metadata."
        )

    def clean_manifest_value(value: str) -> str:
        return (value or "").replace("\xa0", " ").strip()

    mapping = {}
    order = []
    with MANIFEST_CSV.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = clean_manifest_value(row.get("file_name", ""))
            if not name:
                continue
            cleaned = {k: clean_manifest_value(v) for k, v in row.items()}
            mapping[name] = cleaned
            order.append(name)
    return mapping, order


def analyze_pdf(pdf_path: Path, meta: dict, seen_hashes: set[str]) -> list:
    text = extract_text(pdf_path)
    raw_no_footer = drop_footer_lines(text)
    fingerprint = normalize_text(raw_no_footer).lower()
    if fingerprint:
        digest = hashlib.md5(fingerprint.encode("utf-8")).hexdigest()
        if digest in seen_hashes:
            print(f"Skipping duplicate content for {pdf_path.name}")
            return []
        seen_hashes.add(digest)
    cleaned = normalize_text(raw_no_footer)
    inspection_date = extract_inspection_date(cleaned)
    section = extract_violation_section(text)
    violations = split_violations(section)
    facility_name = extract_facility_name(raw_no_footer)
    source_type = extract_source_type(raw_no_footer, facility_name)
    equipment_map = build_equipment_table(raw_no_footer)

    records = []
    for violation_id, violation_text in violations:
        violation_text = normalize_text(drop_footer_lines(violation_text))
        violation_text = trim_stop_phrases(violation_text)
        short_text = shorten_violation(violation_text)
        rule_citation = extract_rule_citations(violation_text)
        permit_condition = extract_permit_conditions(violation_text)
        if not (
            re.search(r"\b(fail(?:ed|ure)?|violat(?:e|ed|ion)|noncompliance|must|shall|exceed(?:ed)?|emit(?:ted)?|vent(?:ing)?)\b", violation_text, flags=re.IGNORECASE)
            or rule_citation
            or permit_condition
        ):
            continue
        records.append(
            {
                "file_name": pdf_path.name,
                "pdf_url": meta.get("pdf_url", ""),
                "document_date": meta.get("document_date", ""),
                "inspection_date": inspection_date,
                "company": extract_company(text, meta.get("company", "")),
                "case_number": meta.get("case_number", ""),
                "enforcement_type": detect_enforcement_type(cleaned),
                "monetary_penalty": extract_penalty(cleaned),
                "violation_id": violation_id,
                "permit_condition": permit_condition,
                "rule_citation": rule_citation,
                "violation_description": short_text,
                "category": categorize(violation_text or short_text or cleaned),
                "equipment_type": extract_equipment_types(violation_text, rule_citation, equipment_map),
                "source_type": source_type,
                "facility_name": facility_name,
            }
        )

    return records


def delete_pdfs(pdf_paths: list[Path]) -> None:
    deleted = 0
    for path in pdf_paths:
        try:
            path.unlink(missing_ok=True)
            deleted += 1
        except Exception as exc:
            print(f"Warning: could not delete {path.name}: {exc}")
    print(f"Deleted {deleted} PDF(s).")


def main() -> None:
    try:
        manifest, order = load_manifest()
    except FileNotFoundError as exc:
        print(exc)
        return

    ordered_paths = []
    seen = set()
    for name in order:
        path = DOWNLOAD_DIR / name
        if path.exists():
            ordered_paths.append(path)
            seen.add(name)

    if not MANIFEST_ONLY:
        for path in sorted(DOWNLOAD_DIR.glob("*.pdf")):
            if path.name not in seen:
                ordered_paths.append(path)

    records = []
    seen_hashes: set[str] = set()
    for pdf_path in ordered_paths:
        meta = manifest.get(pdf_path.name, {})
        if not meta:
            meta = parse_filename_metadata(pdf_path.name)
        records.extend(analyze_pdf(pdf_path, meta, seen_hashes))
        print(f"Parsed {pdf_path.name}")

    if records:
        with OUTPUT_CSV.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(records[0].keys()))
            writer.writeheader()
            writer.writerows(records)
        print(f"Wrote summary {OUTPUT_CSV}")
        if CLEANUP_PDFS:
            manifest_paths = [DOWNLOAD_DIR / name for name in order if (DOWNLOAD_DIR / name).exists()]
            delete_pdfs(manifest_paths or ordered_paths)
    else:
        print("No PDF records found.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse downloaded CDPHE PDFs into a per-violation CSV summary.")
    parser.add_argument(
        "--download-dir",
        type=Path,
        default=DEFAULT_DOWNLOAD_DIR,
        help="Directory containing PDFs and the manifest (default: ./downloads).",
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        default=None,
        help="Manifest CSV path (default: <download-dir>/cdphe_download_manifest.csv).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Output CSV path (default: <download-dir>/cdphe_enforcement_summary.csv).",
    )
    parser.add_argument(
        "--cleanup-pdfs",
        action="store_true",
        help="Delete the PDFs listed in the manifest after successfully writing the summary CSV.",
    )
    parser.add_argument(
        "--manifest-only",
        action="store_true",
        help="Only parse PDFs listed in the manifest (ignore other PDFs in the download directory).",
    )
    args = parser.parse_args()

    DOWNLOAD_DIR = args.download_dir
    MANIFEST_CSV = args.manifest or (DOWNLOAD_DIR / DEFAULT_MANIFEST_NAME)
    OUTPUT_CSV = args.output or (DOWNLOAD_DIR / DEFAULT_OUTPUT_NAME)
    CLEANUP_PDFS = bool(args.cleanup_pdfs)
    MANIFEST_ONLY = bool(args.manifest_only)

    main()
