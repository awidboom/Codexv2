#!/usr/bin/env python3
"""
Convert a Permit to Operate (PTO) PDF into a Title V-like JSON structure.
"""

from __future__ import annotations

import argparse
import json
import os
import re
from typing import Any, Dict, List, Optional, Tuple

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


def parse_pto_equipment(lines: List[str]) -> Dict[str, Any]:
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

    headers = ["S-#", "Description", "Status"]
    rows_as_objects: List[Dict[str, str]] = []
    rows_raw: List[List[str]] = [headers]

    for entry in entries:
        unit_id = normalize_unit_id(entry.get("unit_id_raw", ""))
        unit_digits = ""
        m = re.search(r"\d{1,6}", unit_id)
        if m:
            unit_digits = m.group(0)

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

        description = " ".join(lines).strip()

        row_obj = {
            "S-#": unit_digits,
            "Description": description,
            "Status": status,
            "unit_id": unit_id,
            "applicable_units": [unit_id] if unit_id else [],
        }
        rows_as_objects.append(row_obj)
        rows_raw.append([unit_digits, description, status])

    return {
        "type": "table",
        "rows_raw": rows_raw,
        "title": "PTO Equipment",
        "applicable_units": [],
        "headers": headers,
        "rows_as_objects": rows_as_objects,
        "note_rows": [],
    }


def parse_item_start(line: str) -> Optional[Tuple[str, str]]:
    line = line.strip()
    m = re.match(r"^([A-Za-z])\s*(\d+)\s*\.\s*(.*)$", line)
    if m:
        return (f"{m.group(1).upper()}{m.group(2)}", m.group(3).strip())
    m = re.match(r"^(\d+)\s*([A-Za-z])\s*\.\s*(.*)$", line)
    if m:
        return (f"{m.group(1)}{m.group(2).lower()}", m.group(3).strip())
    m = re.match(r"^(\d+)\s*\.\s*(.*)$", line)
    if m:
        return (m.group(1), m.group(2).strip())
    return None


def is_condition_start(line: str) -> Tuple[bool, Optional[str]]:
    if "Subject to Condition #:" in line:
        return (False, None)
    m = re.match(r"^Condition\s*#:\s*(\d{3,6})?\s*$", line.strip())
    if not m:
        return (False, None)
    return (True, m.group(1))


def normalize_unit_text_for_header(value: str) -> str:
    unit_id = normalize_unit_id(value)
    return unit_id.replace("-", "") if unit_id else value


def build_header_paragraph(header_lines: List[str], condition_number: str) -> str:
    parts: List[str] = []
    pending_unit: Optional[str] = None

    for line in header_lines:
        if not line or line == condition_number:
            continue
        if UNIT_LINE_RE.match(line):
            pending_unit = normalize_unit_text_for_header(line)
            continue

        if pending_unit:
            parts.append(f"{pending_unit} {line}".strip())
            pending_unit = None
        else:
            parts.append(line)

    return " ".join(parts).strip()


def parse_pto_conditions(lines: List[str]) -> List[Dict[str, Any]]:
    conditions: List[Dict[str, Any]] = []
    current: Optional[Dict[str, Any]] = None

    for idx, line in enumerate(lines):
        is_start, inline_number = is_condition_start(line)
        if is_start:
            if current:
                conditions.append(current)
            number = inline_number
            if not number:
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
    for cond in conditions:
        raw_lines = merge_split_lines(cond.get("lines", []))
        clean_lines = filter_noise_lines(raw_lines)

        header_lines: List[str] = []
        items: List[Dict[str, Any]] = []
        current_item: Optional[Dict[str, Any]] = None
        seen_item = False

        for line in clean_lines:
            parsed_item = parse_item_start(line)
            if parsed_item:
                item_number, text = parsed_item
                seen_item = True
                if current_item:
                    items.append(current_item)
                current_item = {"num": item_number, "text": text}
                continue

            if not seen_item:
                header_lines.append(line)
                continue

            if current_item:
                current_item["text"] = f"{current_item['text']} {line}".strip()

        if current_item:
            items.append(current_item)

        header_text = build_header_paragraph(header_lines, cond.get("number", ""))
        units = extract_units_from_text(" ".join(clean_lines))

        content: List[Dict[str, Any]] = []
        if header_text:
            content.append({"type": "paragraph", "text": header_text, "style": ""})
        for item in items:
            content.append(
                {
                    "type": "list_item",
                    "level": 1,
                    "num": item.get("num"),
                    "text": item.get("text", ""),
                    "style": "",
                }
            )

        parsed.append(
            {
                "title": f"Condition {cond.get('number', '').strip()}",
                "level": 2,
                "content": content,
                "sections": [],
                "style": "",
                "applicable_units": units,
            }
        )

    return parsed


def build_json(pdf_path: str) -> Dict[str, Any]:
    raw_lines = extract_pdf_lines(pdf_path)
    merged_lines = merge_split_lines(raw_lines)

    equipment_table = parse_pto_equipment(merged_lines)
    conditions = parse_pto_conditions(merged_lines)

    return {
        "source": {"type": "pdf", "path": os.path.abspath(pdf_path)},
        "front_matter": [],
        "sections": [
            {
                "title": "EQUIPMENT",
                "level": 1,
                "content": [equipment_table],
                "sections": [],
                "style": "",
            },
            {
                "title": "PERMIT CONDITIONS",
                "level": 1,
                "content": [],
                "sections": conditions,
                "style": "",
            },
        ],
    }


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Convert a Permit to Operate PDF into Title V-like JSON."
    )
    ap.add_argument("pto_pdf", help="Path to PermitToOperate.pdf")
    ap.add_argument(
        "--out",
        default=os.path.join("JSON", "permit_to_operate.json"),
        help="Output JSON path",
    )
    args = ap.parse_args()

    if not os.path.exists(args.pto_pdf):
        raise SystemExit(f"PTO PDF not found: {args.pto_pdf}")

    data = build_json(args.pto_pdf)

    out_dir = os.path.dirname(args.out)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(args.out)


if __name__ == "__main__":
    main()
