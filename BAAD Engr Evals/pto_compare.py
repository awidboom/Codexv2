#!/usr/bin/env python3
"""
Compare a Permit to Operate (PTO) PDF to a Title V permit JSON.

Outputs CSV files (Excel-friendly). If openpyxl is installed and --out ends
with .xlsx, writes a multi-sheet workbook. Default output is .xlsx.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
from difflib import SequenceMatcher
from typing import Any, Dict, Iterable, List, Optional, Tuple

from PyPDF2 import PdfReader


DATE_ONLY_RE = re.compile(
    r"^(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s+\d{4}$",
    re.IGNORECASE,
)
UNIT_LINE_RE = re.compile(r"^[SA]\s*-?\s*\d{1,6}$", re.IGNORECASE)
UNIT_IN_TEXT_RE = re.compile(r"\b([SA])\s*-?\s*(\d{1,6})\b", re.IGNORECASE)
CONDITION_NUM_RE = re.compile(r"\b(\d{3,6})\b")


def normalize_unit_id(value: str, default_prefix: Optional[str] = None) -> str:
    value = (value or "").strip()
    m = re.search(r"\b([SA])\s*[- ]?\s*(\d{1,6})\b", value, re.IGNORECASE)
    if m:
        return f"{m.group(1).upper()}-{m.group(2)}"
    if default_prefix and re.search(r"^\d{1,6}$", value):
        return f"{default_prefix.upper()}-{value}"
    if default_prefix and re.search(r"^[A-Za-z]*\d{1,6}$", value):
        digits = re.search(r"\d{1,6}", value)
        if digits:
            return f"{default_prefix.upper()}-{digits.group(0)}"
    return value


def norm_text(value: str) -> str:
    value = (value or "").lower()
    value = re.sub(r"[^a-z0-9]+", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def text_similarity(a: str, b: str) -> float:
    na = norm_text(a)
    nb = norm_text(b)
    if not na or not nb:
        return 0.0
    return SequenceMatcher(None, na, nb).ratio()


def find_section(sections: List[Dict[str, Any]], title: str) -> Optional[Dict[str, Any]]:
    title_up = title.strip().upper()
    for sec in sections:
        if (sec.get("title") or "").strip().upper() == title_up:
            return sec
        found = find_section(sec.get("sections", []), title)
        if found:
            return found
    return None


def extract_pdf_lines(pdf_path: str) -> List[str]:
    reader = PdfReader(pdf_path)
    lines: List[str] = []
    for page in reader.pages:
        text = page.extract_text() or ""
        for raw in text.splitlines():
            line = re.sub(r"\s+", " ", raw).strip()
            if line:
                lines.append(line)
    return lines


def merge_split_lines(lines: List[str]) -> List[str]:
    merged: List[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        nxt = lines[i + 1] if i + 1 < len(lines) else ""

        if line.endswith("-") and nxt and re.match(r"^\d{1,6}$", nxt):
            merged.append(line + nxt)
            i += 2
            continue

        if line in {"S", "A"} and re.match(r"^\d{1,6}$", nxt):
            merged.append(f"{line}-{nxt}")
            i += 2
            continue

        if re.match(r"^[SA]-$", line) and re.match(r"^\d{1,6}$", nxt):
            merged.append(f"{line}{nxt}")
            i += 2
            continue

        merged.append(line)
        i += 1

    return merged


def parse_pto_equipment(lines: List[str]) -> List[Dict[str, str]]:
    in_equipment = False
    entries: List[Dict[str, Any]] = []
    current: Optional[Dict[str, Any]] = None

    for line in lines:
        if "This document serves as your Permit to Operate the following:" in line:
            in_equipment = True
            continue
        if in_equipment and "Condition #:" in line:
            break
        if not in_equipment:
            continue

        if UNIT_LINE_RE.match(line):
            if current:
                entries.append(current)
            current = {"unit_id_raw": line, "lines": []}
            continue

        if current:
            current["lines"].append(line)

    if current:
        entries.append(current)

    parsed: List[Dict[str, str]] = []
    for entry in entries:
        unit_id = normalize_unit_id(entry.get("unit_id_raw", ""))
        lines = list(entry.get("lines", []))
        merged_lines: List[str] = []
        for line in lines:
            if merged_lines and line.startswith("("):
                merged_lines[-1] = f"{merged_lines[-1]} {line}"
            else:
                merged_lines.append(line)
        lines = merged_lines

        status = ""
        if lines and lines[-1].strip().lower() in {"permitted", "exempt"}:
            status = lines.pop(-1).strip()
        elif any(l.strip().lower() in {"permitted", "exempt"} for l in lines):
            for idx in range(len(lines) - 1, -1, -1):
                if lines[idx].strip().lower() in {"permitted", "exempt"}:
                    status = lines.pop(idx).strip()
                    break

        text = " ".join(lines).strip()
        parsed.append(
            {
                "unit_id": unit_id,
                "pto_status": status,
                "pto_text": text,
            }
        )

    return parsed


def filter_noise_lines(lines: List[str]) -> List[str]:
    cleaned: List[str] = []
    skip_fid_number = False
    skip_page_tail = 0

    for line in lines:
        if not line:
            continue
        if line == "FID":
            skip_fid_number = True
            continue
        if skip_fid_number:
            if re.match(r"^\d+$", line):
                skip_fid_number = False
                continue
            skip_fid_number = False
        if line == "Page":
            skip_page_tail = 3
            continue
        if skip_page_tail > 0:
            skip_page_tail -= 1
            continue
        if line.lower().startswith("375 beale street"):
            continue
        if "www.baaqmd.gov" in line.lower():
            continue
        if DATE_ONLY_RE.match(line):
            continue
        cleaned.append(line)

    return cleaned


def parse_pto_conditions(lines: List[str]) -> List[Dict[str, Any]]:
    conditions: List[Dict[str, Any]] = []
    current: Optional[Dict[str, Any]] = None

    for idx, line in enumerate(lines):
        if "Condition #:" in line:
            if current:
                conditions.append(current)
            number = None
            m = CONDITION_NUM_RE.search(line)
            if m:
                number = m.group(1)
            else:
                for look_ahead in range(idx + 1, min(idx + 4, len(lines))):
                    m2 = CONDITION_NUM_RE.search(lines[look_ahead])
                    if m2:
                        number = m2.group(1)
                        break
            current = {"number": number or "", "lines": []}
            continue
        if current:
            current["lines"].append(line)

    if current:
        conditions.append(current)

    parsed: List[Dict[str, Any]] = []
    item_re = re.compile(r"^([A-Z])?\s*(\d+)\.\s*(.*)")
    for cond in conditions:
        raw_lines = merge_split_lines(cond.get("lines", []))
        clean_lines = filter_noise_lines(raw_lines)

        items: List[Dict[str, str]] = []
        current_item: Optional[Dict[str, str]] = None
        for line in clean_lines:
            m = item_re.match(line)
            if m:
                prefix = (m.group(1) or "").strip()
                num = m.group(2)
                text = m.group(3).strip()
                item_number = f"{prefix}{num}" if prefix else num
                if current_item:
                    items.append(current_item)
                current_item = {"item_number": item_number, "text": text}
            else:
                if current_item:
                    current_item["text"] = f"{current_item['text']} {line}".strip()

        if current_item:
            items.append(current_item)

        text = " ".join(clean_lines).strip()
        units = extract_units_from_text(text)
        parsed.append(
            {
                "number": cond.get("number", ""),
                "pto_text": text,
                "pto_units": ", ".join(units),
                "items": items,
            }
        )

    return parsed


def extract_units_from_text(text: str) -> List[str]:
    units: List[str] = []
    for m in UNIT_IN_TEXT_RE.finditer(text or ""):
        units.append(f"{m.group(1).upper()}-{m.group(2)}")
    seen = set()
    dedup: List[str] = []
    for u in units:
        if u not in seen:
            seen.add(u)
            dedup.append(u)
    return dedup


def build_titlev_equipment_map(data: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    equipment = find_section(data.get("sections", []), "EQUIPMENT")
    rows_by_unit: Dict[str, Dict[str, Any]] = {}
    if not equipment:
        return rows_by_unit

    tables = [item for item in equipment.get("content", []) if item.get("type") == "table"]
    for table in tables:
        headers = table.get("headers", []) or []
        for row in table.get("rows_as_objects", []) or []:
            unit_id = row.get("unit_id") or normalize_unit_id(row.get("S-#", ""))
            if not unit_id:
                continue
            parts = [str(row.get(h, "")).strip() for h in headers if str(row.get(h, "")).strip()]
            row_text = " | ".join(parts)
            entry = rows_by_unit.setdefault(
                unit_id,
                {
                    "unit_id": unit_id,
                    "titlev_rows": [],
                },
            )
            entry["titlev_rows"].append(
                {
                    "table_title": (table.get("title") or "").strip(),
                    "row_text": row_text,
                }
            )

    return rows_by_unit


def build_titlev_conditions_map(data: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    permit = find_section(data.get("sections", []), "PERMIT CONDITIONS")
    out: Dict[str, Dict[str, Any]] = {}
    if not permit:
        return out

    for sec in permit.get("sections", []) or []:
        title = sec.get("title", "")
        m = CONDITION_NUM_RE.search(title)
        if not m:
            continue
        number = m.group(1)
        text = titlev_condition_text(sec)
        items = titlev_condition_items(sec)
        out[number] = {
            "number": number,
            "titlev_text": text,
            "titlev_units": ", ".join(sec.get("applicable_units", []) or []),
            "items": items,
        }

    return out


def titlev_condition_text(sec: Dict[str, Any]) -> str:
    parts: List[str] = []
    for item in sec.get("content", []) or []:
        if item.get("type") == "paragraph":
            text = item.get("text", "")
            if text:
                parts.append(text)
        elif item.get("type") == "list_item":
            text = item.get("text", "")
            num = item.get("num")
            if text:
                if num is not None:
                    parts.append(f"{num}. {text}")
                else:
                    parts.append(text)
    return " ".join(parts).strip()


def titlev_condition_items(sec: Dict[str, Any]) -> List[Dict[str, str]]:
    items: List[Dict[str, str]] = []
    for item in sec.get("content", []) or []:
        if item.get("type") != "list_item":
            continue
        num = item.get("num")
        text = item.get("text", "")
        if num is None or not text:
            continue
        items.append({"item_number": str(num), "text": text})
    return items


def compare_equipment(
    pto_equipment: List[Dict[str, str]],
    titlev_equipment: Dict[str, Dict[str, Any]],
    include_titlev_only: bool,
) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    seen_units = set()

    for item in pto_equipment:
        unit_id = item.get("unit_id", "")
        seen_units.add(unit_id)
        titlev_entry = titlev_equipment.get(unit_id)
        titlev_text = ""
        if titlev_entry:
            titlev_text = " || ".join(
                [
                    (r.get("row_text") or "").strip()
                    for r in titlev_entry.get("titlev_rows", [])
                ]
            )
        if not titlev_text:
            comparison = "missing_in_title_v"
        else:
            comparison = "present"

        rows.append(
            {
                "unit_id": unit_id,
                "pto_status": item.get("pto_status", ""),
                "pto_text": item.get("pto_text", ""),
                "titlev_text": titlev_text,
                "similarity": "",
                "comparison": comparison,
            }
        )

    if include_titlev_only:
        for unit_id, entry in titlev_equipment.items():
            if unit_id in seen_units:
                continue
            titlev_text = " || ".join(
                [
                    (r.get("row_text") or "").strip()
                    for r in entry.get("titlev_rows", [])
                ]
            )
            rows.append(
                {
                    "unit_id": unit_id,
                    "pto_status": "",
                    "pto_text": "",
                    "titlev_text": titlev_text,
                    "similarity": "",
                    "comparison": "missing_in_pto",
                }
            )

    return rows


def compare_conditions(
    pto_conditions: List[Dict[str, Any]],
    titlev_conditions: Dict[str, Dict[str, Any]],
    include_titlev_only: bool,
) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    seen = set()

    for cond in pto_conditions:
        number = cond.get("number", "")
        titlev_entry = titlev_conditions.get(number)
        titlev_units = titlev_entry.get("titlev_units", "") if titlev_entry else ""
        titlev_items = {i["item_number"]: i["text"] for i in (titlev_entry or {}).get("items", [])}

        for item in cond.get("items", []):
            item_number = item.get("item_number", "")
            seen.add((number, item_number))
            titlev_text = titlev_items.get(item_number, "")
            similarity = text_similarity(item.get("text", ""), titlev_text)

            if not titlev_text:
                comparison = "missing_in_title_v"
            elif similarity >= 0.92:
                comparison = "match"
            elif similarity >= 0.75:
                comparison = "partial"
            else:
                comparison = "changed"

            rows.append(
                {
                    "condition_number": number,
                    "item_number": item_number,
                    "pto_units": cond.get("pto_units", ""),
                    "titlev_units": titlev_units,
                    "pto_text": item.get("text", ""),
                    "titlev_text": titlev_text,
                    "similarity": f"{similarity:.3f}",
                    "comparison": comparison,
                }
            )

    if include_titlev_only:
        for number, entry in titlev_conditions.items():
            for item in entry.get("items", []):
                item_number = item.get("item_number", "")
                if (number, item_number) in seen:
                    continue
                rows.append(
                    {
                        "condition_number": number,
                        "item_number": item_number,
                        "pto_units": "",
                        "titlev_units": entry.get("titlev_units", ""),
                        "pto_text": "",
                        "titlev_text": item.get("text", ""),
                        "similarity": "0.000",
                        "comparison": "missing_in_pto",
                    }
                )

    return rows


def write_csv(path: str, rows: List[Dict[str, Any]], headers: List[str]) -> None:
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def write_excel(path: str, equipment_rows: List[Dict[str, Any]], condition_rows: List[Dict[str, Any]]) -> None:
    try:
        import openpyxl
    except Exception:
        raise RuntimeError("openpyxl is required for .xlsx output")

    wb = openpyxl.Workbook()
    ws1 = wb.active
    ws1.title = "equipment"
    if equipment_rows:
        ws1.append(list(equipment_rows[0].keys()))
        for row in equipment_rows:
            ws1.append([row.get(k, "") for k in equipment_rows[0].keys()])

    ws2 = wb.create_sheet("conditions")
    if condition_rows:
        ws2.append(list(condition_rows[0].keys()))
        for row in condition_rows:
            ws2.append([row.get(k, "") for k in condition_rows[0].keys()])

    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    wb.save(path)


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Compare a Permit to Operate PDF to a Title V permit JSON."
    )
    ap.add_argument("pto_pdf", help="Path to PermitToOperate.pdf")
    ap.add_argument(
        "--titlev-json",
        default=os.path.join("JSON", "title_v_permit_B2758_B2759.json"),
        help="Path to Title V JSON",
    )
    ap.add_argument(
        "--out",
        default=os.path.join("PTO", "pto_titlev_compare.xlsx"),
        help="Output path (.xlsx) or base path for CSV",
    )
    ap.add_argument(
        "--include-titlev-only",
        action="store_true",
        help="Include Title V items not present in PTO",
    )
    args = ap.parse_args()

    if not os.path.exists(args.pto_pdf):
        raise SystemExit(f"PTO PDF not found: {args.pto_pdf}")
    if not os.path.exists(args.titlev_json):
        raise SystemExit(f"Title V JSON not found: {args.titlev_json}")

    with open(args.titlev_json, "r", encoding="utf-8") as f:
        data = json.load(f)

    raw_lines = extract_pdf_lines(args.pto_pdf)
    merged_lines = merge_split_lines(raw_lines)

    pto_equipment = parse_pto_equipment(merged_lines)
    pto_conditions = parse_pto_conditions(merged_lines)

    titlev_equipment = build_titlev_equipment_map(data)
    titlev_conditions = build_titlev_conditions_map(data)

    equipment_rows = compare_equipment(
        pto_equipment, titlev_equipment, args.include_titlev_only
    )
    condition_rows = compare_conditions(
        pto_conditions, titlev_conditions, args.include_titlev_only
    )

    out_path = args.out
    if out_path.lower().endswith(".xlsx"):
        try:
            write_excel(out_path, equipment_rows, condition_rows)
            print(out_path)
            return
        except RuntimeError as exc:
            print(f"{exc}. Falling back to CSV output.")
            out_path = out_path[: -len(".xlsx")]

    equipment_csv = f"{out_path}_equipment.csv"
    conditions_csv = f"{out_path}_conditions.csv"

    write_csv(
        equipment_csv,
        equipment_rows,
        ["unit_id", "pto_status", "pto_text", "titlev_text", "similarity", "comparison"],
    )
    write_csv(
        conditions_csv,
        condition_rows,
        [
            "condition_number",
            "item_number",
            "pto_units",
            "titlev_units",
            "pto_text",
            "titlev_text",
            "similarity",
            "comparison",
        ],
    )

    print(equipment_csv)
    print(conditions_csv)


if __name__ == "__main__":
    main()
