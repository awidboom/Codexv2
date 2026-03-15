#!/usr/bin/env python3
"""
Compare two permit JSON files (Title V vs PTO JSON).
"""

from __future__ import annotations

import argparse
import json
import os
import re
from difflib import SequenceMatcher
from typing import Any, Dict, Iterable, List, Optional, Tuple


CONDITION_NUM_RE = re.compile(r"\b(\d{3,6})\b")


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


def extract_equipment_units(data: Dict[str, Any]) -> List[str]:
    units: List[str] = []
    equipment = find_section(data.get("sections", []), "EQUIPMENT")
    if not equipment:
        return units
    for item in equipment.get("content", []) or []:
        if item.get("type") != "table":
            continue
        for row in item.get("rows_as_objects", []) or []:
            unit_id = row.get("unit_id")
            if unit_id:
                units.append(str(unit_id))
                continue
            s_num = row.get("S-#")
            if s_num:
                units.append(f"S-{s_num}")
    seen = set()
    dedup: List[str] = []
    for u in units:
        if u not in seen:
            seen.add(u)
            dedup.append(u)
    return dedup


def build_condition_map(data: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
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
        items: Dict[str, str] = {}
        for item in sec.get("content", []) or []:
            if item.get("type") != "list_item":
                continue
            num = item.get("num")
            text = item.get("text", "")
            if num is None or not text:
                continue
            items[str(num)] = text
        out[number] = {
            "number": number,
            "items": items,
            "applicable_units": sec.get("applicable_units", []) or [],
        }

    return out


def compare_equipment_units(
    titlev_units: List[str], pto_units: List[str]
) -> List[Dict[str, Any]]:
    titlev_set = set(titlev_units)
    pto_set = set(pto_units)
    rows: List[Dict[str, Any]] = []

    for unit_id in sorted(pto_set):
        if unit_id in titlev_set:
            comparison = "present"
        else:
            comparison = "missing_in_title_v"
        rows.append({"unit_id": unit_id, "comparison": comparison})

    for unit_id in sorted(titlev_set - pto_set):
        rows.append({"unit_id": unit_id, "comparison": "missing_in_pto"})

    return rows


def compare_condition_items(
    titlev_map: Dict[str, Dict[str, Any]],
    pto_map: Dict[str, Dict[str, Any]],
    include_titlev_only: bool,
) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    seen = set()

    for number, pto_cond in pto_map.items():
        titlev_cond = titlev_map.get(number, {})
        titlev_items = titlev_cond.get("items", {}) if titlev_cond else {}
        titlev_units = ", ".join(titlev_cond.get("applicable_units", []) or [])
        pto_units = ", ".join(pto_cond.get("applicable_units", []) or [])

        for item_number, pto_text in pto_cond.get("items", {}).items():
            seen.add((number, item_number))
            titlev_text = titlev_items.get(item_number, "")
            similarity = text_similarity(pto_text, titlev_text)

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
                    "pto_units": pto_units,
                    "titlev_units": titlev_units,
                    "pto_text": pto_text,
                    "titlev_text": titlev_text,
                    "similarity": f"{similarity:.3f}",
                    "comparison": comparison,
                }
            )

    if include_titlev_only:
        for number, titlev_cond in titlev_map.items():
            for item_number, titlev_text in titlev_cond.get("items", {}).items():
                if (number, item_number) in seen:
                    continue
                rows.append(
                    {
                        "condition_number": number,
                        "item_number": item_number,
                        "pto_units": "",
                        "titlev_units": ", ".join(
                            titlev_cond.get("applicable_units", []) or []
                        ),
                        "pto_text": "",
                        "titlev_text": titlev_text,
                        "similarity": "0.000",
                        "comparison": "missing_in_pto",
                    }
                )

    return rows


def write_excel(
    path: str, equipment_rows: List[Dict[str, Any]], condition_rows: List[Dict[str, Any]]
) -> None:
    import openpyxl

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
    ap = argparse.ArgumentParser(description="Compare Title V JSON to PTO JSON.")
    ap.add_argument("titlev_json", help="Path to Title V JSON")
    ap.add_argument("pto_json", help="Path to PTO JSON")
    ap.add_argument(
        "--out",
        default=os.path.join("PTO", "permit_json_compare.xlsx"),
        help="Output .xlsx path",
    )
    ap.add_argument(
        "--include-titlev-only",
        action="store_true",
        help="Include Title V items not present in PTO",
    )
    args = ap.parse_args()

    if not os.path.exists(args.titlev_json):
        raise SystemExit(f"Title V JSON not found: {args.titlev_json}")
    if not os.path.exists(args.pto_json):
        raise SystemExit(f"PTO JSON not found: {args.pto_json}")

    with open(args.titlev_json, "r", encoding="utf-8") as f:
        titlev = json.load(f)
    with open(args.pto_json, "r", encoding="utf-8") as f:
        pto = json.load(f)

    titlev_units = extract_equipment_units(titlev)
    pto_units = extract_equipment_units(pto)
    equipment_rows = compare_equipment_units(titlev_units, pto_units)

    titlev_conditions = build_condition_map(titlev)
    pto_conditions = build_condition_map(pto)
    condition_rows = compare_condition_items(
        titlev_conditions, pto_conditions, args.include_titlev_only
    )

    write_excel(args.out, equipment_rows, condition_rows)
    print(args.out)


if __name__ == "__main__":
    main()
