import json
import re
from datetime import datetime
from pathlib import Path

import fitz
import pandas as pd

from shared_config import BASE_DIR, INPUT_DIR, load_config, resolve_si_workbook

OUTPUT_FILE = BASE_DIR / "static" / "audit_data.js"

SECTION_MAP = [
    ("Emission Unit 1", "equipment", "Emission Units"),
    ("Emission Units 2", "equipment", "Emission Units"),
    ("Stack Vent", "stack", "Stacks and Vents"),
    ("SI-SI Relationships", "relationship", "Relationships"),
    ("CEMS COMS", "monitor", "CEMS and COMS"),
    ("Parametric", "monitor", "Parametric Monitors"),
    ("Fugitive Sources", "fugitive", "Fugitive Sources"),
    ("Scrubbers", "control", "Control Equipment"),
    ("Wet Separators", "control", "Control Equipment"),
    ("Cyclones", "control", "Control Equipment"),
    ("ESPs", "control", "Control Equipment"),
    ("Injection", "control", "Control Equipment"),
    ("Fabric Filters", "control", "Control Equipment"),
    ("Other Control Equipment", "control", "Control Equipment"),
]

HEADER_HINTS = {
    "Subject Item Type Description",
    "Subject Item ID",
    "Subject Item Designation",
    "Subject Item Description",
    "SI Type Description",
    "SI ID",
    "SI Designation",
    "Description",
}

ROW_ID_PREFIXES = {"EQUI", "TREA", "FUGI", "STRU"}
PERMIT_ID_PREFIXES = ROW_ID_PREFIXES | {"COMG"}
PDF_SI_NAME_HINTS = (("subject", "item"), ("subject", "details"), ("si", "details"))
TITLE_V_NAME_HINTS = (("title", "v"), ("title", "permit"), ("air", "permit"))

DELTA_ID_PATTERN = re.compile(r"^(EU|CE|FS|SV|MR|CM|GP|DA)\s*\d+$", re.IGNORECASE)
PERMIT_ID_PATTERN = re.compile(r"^(COMG|EQUI|TREA|FUGI|STRU)\s*(\d+)$", re.IGNORECASE)
HEADING_BLOCK_PATTERN = re.compile(
    r"^(?P<prefix>COMG|EQUI|TREA|FUGI|STRU)\s*(?P<number>\d+)(?:\s*\|\s*(?P<title>.+))?$",
    re.IGNORECASE,
)
REQUIREMENT_BLOCK_PATTERN = re.compile(r"^(?P<number>[56]\.\d+\.\d+)\s*\|\s*(?P<body>.+)$", re.DOTALL)
SUBJECT_REFERENCE_PATTERN = re.compile(r"\b(COMG|EQUI|TREA|FUGI|STRU)\s*(\d+)\b", re.IGNORECASE)
APPENDIX_REFERENCE_PATTERN = re.compile(r"\bAppendix\s+([A-Z])\b", re.IGNORECASE)
PRINTED_PAGE_PATTERN = re.compile(r"Page\s+(\d+)\s+of\s+\d+", re.IGNORECASE)

DEFAULT_PRINTED_PAGES = {
    "summary": 7,
    "section5": 27,
    "section6": 169,
    "appendices": 203,
}

PDF_SCHEMA_COLUMNS = {
    "equipment": [
        ("SI Type", 30, 83),
        ("Subject Item ID", 83, 130),
        ("Delta Designation Description", 130, 271),
        ("Manufacturer", 271, 333),
        ("Model", 333, 386),
        ("Max Design Capacity", 386, 441),
        ("Max Design Capacity Units", 441, 503),
        ("Material", 503, 556),
        ("Construction Start Date", 556, 608),
        ("Operation Start Date", 608, 660),
        ("Modification Date", 660, 730),
    ],
    "monitor": [
        ("Subject Item ID", 30, 78),
        ("Delta Designation Description", 78, 208),
        ("Manufacturer", 208, 264),
        ("Model", 264, 307),
        ("Serial Number", 307, 356),
        ("Parameter Monitored", 356, 424),
        ("Primary or Backup", 424, 462),
        ("Bypass Capability", 462, 504),
        ("Install Date", 504, 551),
        ("Certification Date", 551, 594),
        ("Certification Basis", 594, 637),
        ("Span (ppm)", 637, 668),
        ("System Full Scale Value (ppm)", 668, 736),
    ],
    "stack": [
        ("Subject Item ID", 30, 86),
        ("Delta Designation Description", 86, 246),
        ("Stack Height (feet)", 246, 292),
        ("Stack Diameter (feet)", 292, 346),
        ("Stack Length (feet)", 346, 395),
        ("Stack Width (feet)", 395, 444),
        ("Stack Flow Rate (cubic ft/min)", 444, 532),
        ("Discharge Temperature (F)", 532, 588),
        ("Flow Rate/Temp Information Source", 588, 654),
        ("Discharge Direction", 654, 736),
    ],
    "control": [
        ("Subject Item Type", 35, 86),
        ("Subject Item ID", 86, 118),
        ("Delta Designation Description", 118, 218),
        ("Manufacturer (Model #)", 218, 265),
        ("Installation Start Date", 265, 305),
        ("Pollutants Controlled", 305, 350),
        ("Capture Efficiency (%)", 350, 384),
        ("Destruction Collect Efficiency (%)", 384, 432),
        ("Subject to CAM?", 432, 462),
        ("Large or Other PSEU?", 462, 492),
        ("Efficiency Basis", 492, 526),
        ("Other Basis Explanation", 526, 596),
    ],
    "fugitive": [
        ("Subject Item Type", 35, 86),
        ("Subject Item ID", 86, 118),
        ("Delta Designation Description", 118, 260),
        ("Install Year", 260, 330),
        ("Pollutants Emitted", 330, 736),
    ],
}


def normalize_text_key(value):
    return re.sub(r"[^a-z0-9]+", "", str(value or "").lower())


def normalize_code(value):
    return re.sub(r"\s+", "", str(value or "").upper())


def clean_pdf_text(text):
    return (
        str(text or "")
        .replace("\ufb01", "fi")
        .replace("\ufb02", "fl")
        .replace("\u2019", "'")
        .replace("\u2013", "-")
        .replace("\u2014", "-")
        .replace("\u2212", "-")
        .replace("\u2264", "<=")
        .replace("\u2265", ">=")
        .replace("\xa0", " ")
    )


def find_header_row(raw_df):
    best_idx = None
    best_score = 0
    for idx, row in raw_df.iterrows():
        values = {
            str(value).strip()
            for value in row.tolist()
            if isinstance(value, str) and str(value).strip() and str(value).strip().lower() != "nan"
        }
        if {"Subject Item ID", "Subject Item Designation"}.issubset(values):
            return idx
        if {"SI ID", "SI Designation"}.issubset(values):
            return idx
        score = len(values.intersection(HEADER_HINTS))
        if score > best_score:
            best_score = score
            best_idx = idx
    return best_idx if best_score >= 2 else None


def make_unique_headers(headers):
    counts = {}
    result = []
    for header in headers:
        name = header.strip() if header else "Notes"
        counts[name] = counts.get(name, 0) + 1
        result.append(name if counts[name] == 1 else f"{name} ({counts[name]})")
    return result


def normalize_value(value):
    if pd.isna(value):
        return None
    if isinstance(value, (pd.Timestamp, datetime)):
        return value.isoformat()
    if hasattr(value, "item"):
        try:
            return value.item()
        except ValueError:
            return value
    return value


def load_sheet(data_file, sheet_name):
    raw = pd.read_excel(data_file, sheet_name=sheet_name, header=None, engine="openpyxl")
    header_row = find_header_row(raw)
    if header_row is None:
        return None, None

    headers = raw.iloc[header_row].tolist()
    valid_cols = []
    normalized_headers = []
    for idx, header in enumerate(headers):
        header_text = str(header).strip() if isinstance(header, str) else ""
        has_data = raw.iloc[header_row + 1 :, idx].notna().any()
        if header_text and header_text.lower() != "nan":
            valid_cols.append(idx)
            normalized_headers.append(header_text)
        elif has_data:
            valid_cols.append(idx)
            normalized_headers.append("Notes")

    if not valid_cols:
        return None, None

    df = raw.iloc[header_row + 1 :, valid_cols].copy()
    df.columns = make_unique_headers(normalized_headers)
    df = df.dropna(how="all")
    for column in df.columns:
        if df[column].dtype == object:
            df[column] = df[column].map(lambda value: value.strip() if isinstance(value, str) else value)
    return df, df.columns.tolist()


def build_documents():
    documents = []
    if not INPUT_DIR.exists():
        return documents

    allowed_extensions = {".xlsx", ".xlsm", ".xls", ".pdf"}
    for path in sorted(INPUT_DIR.iterdir(), key=lambda item: item.name.lower()):
        if (
            not path.is_file()
            or path.suffix.lower() not in allowed_extensions
            or path.name.startswith("~$")
        ):
            continue
        documents.append(
            {
                "name": path.name,
                "path": f"../input/{path.name}",
                "extension": path.suffix.lower(),
            }
        )
    return documents


def derive_facility_name(_config):
    return "Facility SI Details Viewer"


def derive_title(_config):
    return "Facility SI Details Viewer"


def list_input_pdfs():
    if not INPUT_DIR.exists():
        return []
    return sorted(INPUT_DIR.glob("*.pdf"), key=lambda path: path.name.lower())


def _name_matches(path, keyword_groups):
    name = path.name.lower()
    return any(all(keyword in name for keyword in group) for group in keyword_groups)


def resolve_si_details_pdf():
    pdfs = list_input_pdfs()
    for pdf in pdfs:
        if _name_matches(pdf, PDF_SI_NAME_HINTS):
            return pdf
    non_permit = [pdf for pdf in pdfs if not _name_matches(pdf, TITLE_V_NAME_HINTS)]
    return non_permit[0] if len(non_permit) == 1 else (pdfs[0] if pdfs else None)


def resolve_title_v_permit_pdf():
    pdfs = list_input_pdfs()
    for pdf in pdfs:
        if _name_matches(pdf, TITLE_V_NAME_HINTS):
            return pdf
    if not pdfs:
        return None
    si_pdf = resolve_si_details_pdf()
    candidates = [pdf for pdf in pdfs if pdf != si_pdf]
    if candidates:
        return max(candidates, key=lambda path: path.stat().st_size)
    return max(pdfs, key=lambda path: path.stat().st_size)


def detect_pdf_kind(header_names):
    normalized = {normalize_text_key(name) for name in header_names}
    if any("stackheight" in name for name in normalized):
        return "stack"
    if any("parametermonitored" in name for name in normalized) or any("serialnumber" in name for name in normalized):
        return "monitor"
    if any("pollutantscontrolled" in name for name in normalized) or any("pollutantcontrolled" in name for name in normalized):
        return "control"
    if any("pollutantsemitted" in name for name in normalized):
        return "fugitive"
    if any("maxdesigncapacity" in name for name in normalized):
        return "equipment"
    return None


def split_designation_description(value):
    lines = [line.strip() for line in clean_pdf_text(value).splitlines() if line.strip()]
    if not lines:
        return None, None
    designation = None
    filtered = []
    for line in lines:
        normalized = normalize_code(line)
        if DELTA_ID_PATTERN.fullmatch(normalized):
            designation = normalized
            continue
        if normalize_text_key(line) == "null":
            continue
        filtered.append(line)
    description = " ".join(filtered).strip() or None
    return designation, description


def split_manufacturer_model(value):
    text = clean_pdf_text(value).strip()
    if not text:
        return None, None
    match = re.match(r"^(.*?)(?:\((.*?)\))?$", text)
    if not match:
        return text, None
    manufacturer = match.group(1).strip() or None
    model = match.group(2).strip() if match.group(2) else None
    if manufacturer and manufacturer.lower() == "null":
        manufacturer = None
    if model and model.lower() == "null":
        model = None
    return manufacturer, model


def format_column_text(words):
    rows = {}
    for word in sorted(words, key=lambda item: (round(item[1], 2), item[0])):
        key = (round(word[1], 2), word[5], word[6])
        rows.setdefault(key, []).append(clean_pdf_text(word[4]))
    lines = [" ".join(parts).strip() for _, parts in sorted(rows.items())]
    return "\n".join(line for line in lines if line).strip()


def build_pdf_item(page_num, kind, row_data):
    item_id = normalize_code(row_data.get("Subject Item ID"))
    if not any(item_id.startswith(prefix) for prefix in ROW_ID_PREFIXES):
        return None

    designation, description = split_designation_description(
        row_data.get("Delta Designation Description") or row_data.get("SI Designation and Description")
    )
    manufacturer = row_data.get("Manufacturer")
    model = row_data.get("Model")

    if not manufacturer and row_data.get("Manufacturer (Model #)"):
        manufacturer, model = split_manufacturer_model(row_data.get("Manufacturer (Model #)"))

    record = {
        "itemId": item_id,
        "designation": designation,
        "description": description,
        "kind": kind,
        "page": page_num,
        "rawValues": {key: value for key, value in row_data.items() if value},
    }

    common_fields = {
        "itemType": row_data.get("Subject Item Type") or row_data.get("SI Type"),
        "manufacturer": manufacturer,
        "model": model,
        "material": row_data.get("Material") or row_data.get("Material Injected"),
        "constructionStart": row_data.get("Construction Start Date"),
        "operationStart": row_data.get("Operation Start Date"),
        "modificationDate": row_data.get("Modification Date"),
        "installationStart": row_data.get("Installation Start Date"),
        "parameterMonitored": row_data.get("Parameter Monitored"),
        "pollutantsControlled": row_data.get("Pollutants Controlled") or row_data.get("Pollutant Controlled"),
        "pollutantsEmitted": row_data.get("Pollutants Emitted"),
    }
    record.update({key: value for key, value in common_fields.items() if value})
    return record


def merge_pdf_items(existing, incoming):
    if existing is None:
        return incoming

    merged = existing.copy()
    merged["page"] = min(existing.get("page", incoming["page"]), incoming.get("page", existing["page"]))
    merged_raw = dict(existing.get("rawValues", {}))
    for key, value in incoming.get("rawValues", {}).items():
        merged_raw.setdefault(key, value)
    merged["rawValues"] = merged_raw

    for key, value in incoming.items():
        if key in {"page", "rawValues"} or not value:
            continue
        current = merged.get(key)
        if not current:
            merged[key] = value
            continue
        if key == "designation":
            merged[key] = value
            continue
        if key == "description" and len(str(value)) > len(str(current)):
            merged[key] = value
    return merged


def extract_pdf_items(pdf_path):
    if not pdf_path or not pdf_path.exists():
        return []

    doc = fitz.open(pdf_path)
    items_by_id = {}

    for page_index in range(doc.page_count):
        page = doc.load_page(page_index)
        blocks = page.get_text("blocks")
        words = page.get_text("words")

        header_blocks = []
        for block in blocks:
            x0, y0, x1, y1, text, *_ = block
            cleaned = clean_pdf_text(text).strip()
            if not cleaned:
                continue
            if y0 < 100 or y0 > 160:
                continue
            if "AI ID" in cleaned or "Activity" in cleaned or cleaned == "Abc":
                continue
            header_blocks.append((x0, x1, cleaned))

        header_blocks.sort(key=lambda item: item[0])
        if len(header_blocks) < 4:
            continue

        header_names = [" ".join(block_text.split()) for _, _, block_text in header_blocks]
        kind = detect_pdf_kind(header_names)
        if not kind:
            continue

        schema_columns = PDF_SCHEMA_COLUMNS.get(kind)
        item_x_min = next(start for name, start, _ in schema_columns if name == "Subject Item ID")
        item_x_max = next(end for name, _, end in schema_columns if name == "Subject Item ID")
        header_y_max = 155 if kind == "equipment" else 132

        line_map = {}
        for word in words:
            x0, y0, x1, y1, text, block_no, line_no, _ = word
            if y0 <= header_y_max + 2:
                continue
            line_map.setdefault((block_no, line_no), []).append(word)

        row_starts = []
        for (_block_no, _line_no), line_words in line_map.items():
            ordered = sorted(line_words, key=lambda item: item[0])
            for idx, word in enumerate(ordered):
                x0, _y0, x1, _y1, text, *_ = word
                mid_x = (x0 + x1) / 2
                token = normalize_code(text)
                if token not in ROW_ID_PREFIXES:
                    continue
                if not (item_x_min - 8 <= mid_x <= item_x_max + 8):
                    continue
                item_tokens = [token]
                for next_word in ordered[idx + 1 :]:
                    next_mid = (next_word[0] + next_word[2]) / 2
                    if next_mid > item_x_max + 8:
                        break
                    next_token = clean_pdf_text(next_word[4]).strip()
                    if next_token:
                        item_tokens.append(next_token)
                full_id = normalize_code("".join(item_tokens[:2]))
                row_starts.append((word[1], full_id))
                break

        row_starts = sorted({(round(y, 2), item_id) for y, item_id in row_starts}, key=lambda item: item[0])
        if not row_starts:
            continue

        min_x = schema_columns[0][1] - 4
        max_x = schema_columns[-1][2] + 4
        for idx, (row_y, detected_id) in enumerate(row_starts):
            next_y = row_starts[idx + 1][0] - 1 if idx + 1 < len(row_starts) else 10_000
            region_words = [
                word
                for word in words
                if row_y - 12 <= word[1] < next_y and min_x <= (word[0] + word[2]) / 2 <= max_x
            ]
            column_words = {name: [] for name, _, _ in schema_columns}
            for word in region_words:
                mid_x = (word[0] + word[2]) / 2
                column_name = schema_columns[-1][0]
                for name, start, end in schema_columns:
                    if start <= mid_x < end:
                        column_name = name
                        break
                column_words[column_name].append(word)

            row_data = {name: format_column_text(column_words[name]) for name, _, _ in schema_columns}
            row_data["Subject Item ID"] = detected_id
            pdf_item = build_pdf_item(page_index + 1, kind, row_data)
            if not pdf_item:
                continue
            items_by_id[pdf_item["itemId"]] = merge_pdf_items(items_by_id.get(pdf_item["itemId"]), pdf_item)

    return sorted(items_by_id.values(), key=lambda item: item["itemId"])


def extract_printed_page_number(page_text):
    match = PRINTED_PAGE_PATTERN.search(clean_pdf_text(page_text))
    return int(match.group(1)) if match else None


def build_printed_page_map(doc):
    printed_to_index = {}
    index_to_printed = {}
    for page_index in range(doc.page_count):
        printed = extract_printed_page_number(doc.load_page(page_index).get_text("text"))
        if printed is None:
            continue
        printed_to_index.setdefault(printed, page_index)
        index_to_printed[page_index] = printed
    return printed_to_index, index_to_printed


def parse_toc_printed_pages(doc):
    probe_pages = min(12, doc.page_count)
    text = "\n".join(clean_pdf_text(doc.load_page(i).get_text("text")) for i in range(probe_pages))
    targets = {
        "summary": "4. Summary of subject items",
        "section5": "5. Limits and other requirements",
        "section6": "6. Submittal/action requirements",
        "appendices": "Appendix A. Insignificant activities and general applicable requirements",
    }
    results = {}
    for key, title in targets.items():
        pattern = re.compile(re.escape(title) + r"[\s.\n]*?(\d+)", re.IGNORECASE)
        match = pattern.search(text)
        if match:
            results[key] = int(match.group(1))
    return results


def resolve_permit_ranges(doc):
    printed_to_index, index_to_printed = build_printed_page_map(doc)
    printed_pages = DEFAULT_PRINTED_PAGES.copy()
    printed_pages.update(parse_toc_printed_pages(doc))

    resolved = {}
    for key, printed in printed_pages.items():
        if printed in printed_to_index:
            resolved[key] = printed_to_index[printed]

    if "summary" not in resolved:
        resolved["summary"] = 6
    if "section5" not in resolved:
        resolved["section5"] = 26
    if "section6" not in resolved:
        resolved["section6"] = 168
    if "appendices" not in resolved:
        resolved["appendices"] = 202

    return resolved, printed_to_index, index_to_printed


def extract_block_entries(page):
    entries = []
    for block in page.get_text("dict").get("blocks", []):
        if "lines" not in block:
            continue
        lines = []
        for line in block["lines"]:
            spans = [clean_pdf_text(span["text"]).strip() for span in line["spans"] if clean_pdf_text(span["text"]).strip()]
            if spans:
                lines.append(" ".join(spans))
        if not lines:
            continue
        entries.append(
            {
                "y0": block["bbox"][1],
                "text": "\n".join(lines).strip(),
                "flat": " | ".join(lines).strip(),
            }
        )
    entries.sort(key=lambda entry: entry["y0"])
    return entries


def is_noise_block(entry):
    flat = entry["flat"]
    if not flat:
        return True
    if flat.startswith("Permit Issued:") or flat.startswith("Permit issued:"):
        return True
    if flat == "Requirement number Requirement and citation":
        return True
    return False


def parse_heading_entry(entry):
    match = HEADING_BLOCK_PATTERN.match(entry["flat"])
    if not match:
        return None
    item_id = normalize_code(f"{match.group('prefix')}{match.group('number')}")
    title = clean_pdf_text(match.group("title") or "").strip() or None
    return {"itemId": item_id, "title": title}


def parse_requirement_entry(entry):
    match = REQUIREMENT_BLOCK_PATTERN.match(entry["flat"])
    if not match:
        return None
    return {
        "number": match.group("number"),
        "body": entry["text"].split("\n", 1)[1].strip() if "\n" in entry["text"] else match.group("body").strip(),
    }


def finalize_condition(condition):
    if not condition:
        return None

    raw_text = "\n".join(part.strip() for part in condition.pop("parts") if part and part.strip()).strip()
    raw_text = re.sub(r"\n{3,}", "\n\n", clean_pdf_text(raw_text))
    citation_match = re.search(r"(\[[^\[\]]+\])\s*$", raw_text, re.DOTALL)
    citation = citation_match.group(1).strip() if citation_match else None
    body_text = raw_text[: citation_match.start()].strip() if citation_match else raw_text

    references = []
    if re.search(r"See Subject Item", body_text, re.IGNORECASE):
        references = sorted(
            {
                normalize_code(f"{match.group(1)}{match.group(2)}")
                for match in SUBJECT_REFERENCE_PATTERN.finditer(body_text)
            }
        )

    appendix_refs = sorted({match.group(1).upper() for match in APPENDIX_REFERENCE_PATTERN.finditer(raw_text)})

    return {
        **condition,
        "text": body_text,
        "citation": citation,
        "referencedIds": references,
        "appendixRefs": appendix_refs,
    }


def parse_permit_sections(doc, ranges, index_to_printed):
    permit_items = {}
    conditions = []

    def register_item(item_id, title, printed_page, section):
        existing = permit_items.get(item_id)
        record = {
            "itemId": item_id,
            "title": title,
            "page": printed_page,
            "section": section,
        }
        if not existing:
            permit_items[item_id] = record
            return
        if printed_page is not None and (existing.get("page") is None or printed_page < existing["page"]):
            existing["page"] = printed_page
        if title and (not existing.get("title") or len(title) > len(existing["title"])):
            existing["title"] = title

    ordered_sections = [
        ("5", ranges["section5"], ranges["section6"]),
        ("6", ranges["section6"], ranges["appendices"]),
    ]

    for section_label, start_index, end_index in ordered_sections:
        current_heading = None
        current_condition = None

        for page_index in range(start_index, min(end_index, doc.page_count)):
            printed_page = index_to_printed.get(page_index)
            page = doc.load_page(page_index)
            for entry in extract_block_entries(page):
                if is_noise_block(entry):
                    continue

                heading = parse_heading_entry(entry)
                if heading:
                    finalized = finalize_condition(current_condition)
                    if finalized:
                        conditions.append(finalized)
                    current_condition = None
                    current_heading = heading
                    register_item(heading["itemId"], heading.get("title"), printed_page, section_label)
                    continue

                requirement = parse_requirement_entry(entry)
                if requirement:
                    finalized = finalize_condition(current_condition)
                    if finalized:
                        conditions.append(finalized)
                    if not current_heading:
                        current_condition = None
                        continue
                    current_condition = {
                        "subjectItemId": current_heading["itemId"],
                        "subjectItemTitle": current_heading.get("title"),
                        "section": section_label,
                        "requirementNumber": requirement["number"],
                        "page": printed_page,
                        "parts": [requirement["body"]],
                    }
                    continue

                if current_condition:
                    current_condition["parts"].append(entry["text"])

        finalized = finalize_condition(current_condition)
        if finalized:
            conditions.append(finalized)

    return {
        "items": sorted(permit_items.values(), key=lambda item: item["itemId"]),
        "conditions": conditions,
    }


def parse_summary_comg_memberships(doc, ranges, index_to_printed):
    summary_start = ranges["summary"]
    summary_end = ranges["section5"]
    if summary_end <= summary_start:
        return {"groups": {}, "members": {}}

    page_texts = []
    page_lookup = {}
    for page_index in range(summary_start, min(summary_end, doc.page_count)):
        text = " ".join(clean_pdf_text(doc.load_page(page_index).get_text("text")).split())
        if not text:
            continue
        page_texts.append(text)
        for match in re.finditer(r"\bCOMG\s+\d+\b", text, re.IGNORECASE):
            comg_id = normalize_code(match.group(0))
            page_lookup.setdefault(comg_id, index_to_printed.get(page_index))

    combined = " ".join(page_texts)
    pattern = re.compile(
        r"(COMG\s+\d+)\s*:\s*(.*?)\s+has members\s+(.+?)(?=\s+(?:COMG|EQUI|TREA|FUGI|STRU)\s+\d+\s*:|\s*$)",
        re.IGNORECASE,
    )

    groups = {}
    reverse = {}
    for match in pattern.finditer(combined):
        group_id = normalize_code(match.group(1))
        title = re.sub(r"\s+", " ", clean_pdf_text(match.group(2))).strip()
        member_text = match.group(3)
        members = [
            normalize_code(f"{ref.group(1)}{ref.group(2)}")
            for ref in SUBJECT_REFERENCE_PATTERN.finditer(member_text)
            if ref.group(1).upper() != "COMG"
        ]
        members = sorted(dict.fromkeys(members))
        groups[group_id] = {
            "itemId": group_id,
            "title": title,
            "members": members,
            "page": page_lookup.get(group_id),
        }
        for member_id in members:
            reverse.setdefault(member_id, []).append(group_id)

    reverse = {member_id: sorted(group_ids) for member_id, group_ids in reverse.items()}
    return {"groups": groups, "members": reverse}


def extract_appendix_starts(doc, appendices_start_index):
    starts = {}
    for page_index in range(appendices_start_index, doc.page_count):
        lines = [
            " ".join(line.split())
            for line in clean_pdf_text(doc.load_page(page_index).get_text("text")).splitlines()
            if " ".join(line.split())
        ]
        probe = " | ".join(lines[:12])
        match = re.search(r"\bAppendix\s+([A-Z])\.", probe, re.IGNORECASE)
        if match:
            starts.setdefault(match.group(1).upper(), page_index)
    return starts


def build_appendix_excerpts(doc, ranges, index_to_printed, cited_letters):
    if not cited_letters:
        return []

    starts = extract_appendix_starts(doc, ranges["appendices"])
    ordered = sorted((letter, page_index) for letter, page_index in starts.items() if letter in cited_letters)
    if not ordered:
        return []

    excerpts = []
    for idx, (letter, start_index) in enumerate(ordered):
        next_index = ordered[idx + 1][1] if idx + 1 < len(ordered) else doc.page_count
        excerpt_pages = range(start_index, min(start_index + 2, next_index))
        excerpt_parts = []
        title = None
        for page_index in excerpt_pages:
            lines = [
                " ".join(line.split())
                for line in clean_pdf_text(doc.load_page(page_index).get_text("text")).splitlines()
                if " ".join(line.split())
            ]
            if not lines:
                continue
            if title is None:
                for line in lines[:8]:
                    if re.search(rf"\bAppendix\s+{letter}\.", line, re.IGNORECASE):
                        title = line
                        break
            excerpt_parts.append("\n".join(lines[:20]))

        excerpt_text = "\n\n".join(part for part in excerpt_parts if part).strip()
        if not excerpt_text:
            continue

        excerpts.append(
            {
                "appendixId": letter,
                "title": title or f"Appendix {letter}",
                "page": index_to_printed.get(start_index),
                "excerpt": excerpt_text[:2800].strip(),
            }
        )

    return excerpts


def extract_permit_data(permit_pdf):
    if not permit_pdf or not permit_pdf.exists():
        return {
            "sourceFile": None,
            "items": [],
            "conditions": [],
            "comgMemberships": {"groups": {}, "members": {}},
            "appendixExcerpts": [],
        }

    doc = fitz.open(permit_pdf)
    ranges, _printed_to_index, index_to_printed = resolve_permit_ranges(doc)
    section_data = parse_permit_sections(doc, ranges, index_to_printed)
    comg_memberships = parse_summary_comg_memberships(doc, ranges, index_to_printed)
    cited_appendices = {
        letter
        for condition in section_data["conditions"]
        for letter in condition.get("appendixRefs", [])
    }
    appendix_excerpts = build_appendix_excerpts(doc, ranges, index_to_printed, cited_appendices)

    return {
        "sourceFile": permit_pdf.name,
        "items": section_data["items"],
        "conditions": section_data["conditions"],
        "comgMemberships": comg_memberships,
        "appendixExcerpts": appendix_excerpts,
    }


def build_payload():
    config = load_config()
    data_file = resolve_si_workbook(config)
    si_pdf_file = resolve_si_details_pdf()
    permit_pdf_file = resolve_title_v_permit_pdf()
    sections = []

    for sheet_name, kind, label in SECTION_MAP:
        try:
            df, columns = load_sheet(data_file, sheet_name)
        except ValueError:
            continue
        if df is None or df.empty:
            continue
        rows = [{column: normalize_value(row[column]) for column in columns} for _, row in df.iterrows()]
        sections.append(
            {
                "sheet": sheet_name,
                "kind": kind,
                "label": label,
                "columns": columns,
                "rows": rows,
            }
        )

    permit = extract_permit_data(permit_pdf_file)
    return {
        "generatedAt": datetime.now().isoformat(timespec="seconds"),
        "facilityName": derive_facility_name(config),
        "title": derive_title(config),
        "sourceFile": data_file.name,
        "pdfSourceFile": si_pdf_file.name if si_pdf_file else None,
        "permitSourceFile": permit_pdf_file.name if permit_pdf_file else None,
        "documents": build_documents(),
        "sections": sections,
        "pdfItems": extract_pdf_items(si_pdf_file),
        "permit": permit,
    }


def main():
    payload = build_payload()
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as handle:
        handle.write("window.AUDIT_DATA = ")
        json.dump(payload, handle, ensure_ascii=True, indent=2)
        handle.write(";\n")
    print(f"Wrote {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
