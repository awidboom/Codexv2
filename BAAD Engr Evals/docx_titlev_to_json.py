#!/usr/bin/env python3
"""
Convert a Title V permit DOCX into ordered JSON with section hierarchy and tables.
"""

from __future__ import annotations

import argparse
import json
import os
import re
from typing import Any, Dict, Iterable, List, Optional

from docx import Document
from docx.text.paragraph import Paragraph
from docx.table import Table
from docx.oxml.table import CT_Tbl
from docx.oxml.text.paragraph import CT_P


def iter_block_items(doc: Document) -> Iterable[object]:
    """Yield Paragraph and Table objects in document order."""
    for child in doc.element.body.iterchildren():
        if isinstance(child, CT_P):
            yield Paragraph(child, doc)
        elif isinstance(child, CT_Tbl):
            yield Table(child, doc)


def heading_level(style_name: str) -> Optional[int]:
    if not style_name:
        return None
    if style_name.lower().startswith("heading"):
        parts = style_name.split()
        for part in reversed(parts):
            if part.isdigit():
                return int(part)
    return None


def extract_source_ids(doc: Document) -> List[str]:
    ids = []
    for p in doc.paragraphs:
        for m in re.finditer(r"\bB\d{3,6}\b", p.text):
            ids.append(m.group(0))
    seen = set()
    dedup = []
    for i in ids:
        if i not in seen:
            dedup.append(i)
            seen.add(i)
    return dedup


def toc_level(style_name: str) -> Optional[int]:
    if not style_name:
        return None
    if style_name.lower().startswith("toc"):
        parts = style_name.split()
        for part in reversed(parts):
            if part.isdigit():
                return int(part)
    return None


def bullet_level(style_name: str) -> Optional[int]:
    if not style_name:
        return None
    if style_name.lower().startswith("bullets level"):
        parts = style_name.split()
        for part in reversed(parts):
            if part.isdigit():
                return int(part)
    return None


def table_to_matrix(tbl: Table) -> List[List[str]]:
    rows: List[List[str]] = []
    for row in tbl.rows:
        row_cells = []
        for cell in row.cells:
            row_cells.append(cell.text)
        rows.append(row_cells)
    return rows


def normalize_unit_id(value: str, default_prefix: Optional[str] = None) -> str:
    value = value.strip()
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


def extract_applicable_units(text: str) -> List[str]:
    units = []
    for m in re.finditer(r"\b([SA])\s*[- ]?\s*(\d{1,6})\b", text, re.IGNORECASE):
        units.append(f"{m.group(1).upper()}-{m.group(2)}")
    seen = set()
    dedup = []
    for u in units:
        if u not in seen:
            dedup.append(u)
            seen.add(u)
    return dedup


def extract_units_from_sources(text: str) -> List[str]:
    if not text:
        return []
    units: List[str] = []
    # Ranges like "S32120 through S32135" or "S32120-S32135"
    for m in re.finditer(
        r"\b([SA])\s*[- ]?\s*(\d{1,6})\s*(?:-|to|through)\s*([SA])?\s*[- ]?\s*(\d{1,6})\b",
        text,
        re.IGNORECASE,
    ):
        p1 = m.group(1).upper()
        start = int(m.group(2))
        p2 = (m.group(3) or p1).upper()
        end = int(m.group(4))
        if p1 != p2:
            continue
        if start <= end and (end - start) <= 5000:
            for n in range(start, end + 1):
                units.append(f"{p1}-{n}")
        elif start > end and (start - end) <= 5000:
            for n in range(start, end - 1, -1):
                units.append(f"{p1}-{n}")
    # Single IDs
    units.extend(extract_applicable_units(text))
    seen = set()
    dedup = []
    for u in units:
        if u not in seen:
            dedup.append(u)
            seen.add(u)
    return dedup


def normalize_table(matrix: List[List[str]]) -> Dict[str, Any]:
    if not matrix:
        return {"title": "", "headers": [], "rows_as_objects": [], "note_rows": []}

    title = ""
    headers: List[str] = []
    data_rows: List[List[str]] = []

    idx = 0
    first = matrix[0]
    if first:
        non_empty = [c for c in first if c.strip()]
        if non_empty and len(set(non_empty)) == 1:
            title = non_empty[0]
            idx = 1

    header_row_index = None
    for i, row in enumerate(matrix[:10]):
        if row and row[0].strip().upper() == "TYPE" and row[-1].strip() == "502":
            header_row_index = i
            break

    if header_row_index is not None:
        headers = matrix[header_row_index]
        idx = header_row_index + 1
    elif idx < len(matrix):
        headers = matrix[idx]
        idx += 1

    data_rows = matrix[idx:] if idx <= len(matrix) else []

    applicable_units = extract_applicable_units(title) if title else []

    unit_id_key = None
    unit_id_index = None
    unit_id_prefix = None
    for i, h in enumerate(headers):
        h_norm = re.sub(r"\s+", "", h.upper())
        if "S-#" in h_norm or h_norm == "S#" or "A-#" in h_norm or h_norm == "A#":
            unit_id_key = h
            unit_id_index = i
            unit_id_prefix = "S" if "S" in h_norm else "A"
            break

    special_vii_f3 = bool(headers) and headers[0].strip().upper() == "TYPE" and headers[-1].strip() == "502"

    def is_merged_row(row: List[str]) -> bool:
        non_empty = [c for c in row if c.strip()]
        return len(non_empty) > 1 and len(set(non_empty)) == 1

    rows_as_objects: List[Dict[str, str]] = []
    note_rows: List[List[str]] = []
    table_units: List[str] = []
    if headers:
        for row in data_rows:
            if special_vii_f3 and is_merged_row(row):
                note_rows.append(row)
                continue
            row_obj: Dict[str, str] = {}
            for i, h in enumerate(headers):
                if i < len(row):
                    row_obj[h] = row[i]
                else:
                    row_obj[h] = ""
            if unit_id_index is not None and unit_id_key is not None:
                row_obj["unit_id"] = normalize_unit_id(
                    row_obj.get(unit_id_key, ""),
                    default_prefix=unit_id_prefix,
                )
            if applicable_units:
                row_obj["applicable_units"] = list(applicable_units)
            elif unit_id_index is not None and unit_id_key is not None:
                unit_val = row_obj.get("unit_id", "")
                row_obj["applicable_units"] = [unit_val] if unit_val else []
                if unit_val:
                    table_units.append(unit_val)
            else:
                row_obj["applicable_units"] = []
            rows_as_objects.append(row_obj)

    is_table_iv_f2 = bool(title) and ("TABLE IV" in title.upper()) and ("F.2" in title)
    if is_table_iv_f2 and headers and "Sources" in headers and "Tank Group" in headers:
        group_ids = [r.get("Tank Group", "") for r in rows_as_objects if r.get("Tank Group", "")]
        group_set = set(group_ids)

        group_units: Dict[str, List[str]] = {}
        group_refs: Dict[str, List[str]] = {}

        for row in rows_as_objects:
            gid = row.get("Tank Group", "")
            sources = row.get("Sources", "")
            if not gid:
                continue
            units = [normalize_unit_id(u) for u in extract_units_from_sources(sources)]
            group_units[gid] = units

            refs: List[str] = []
            for g in group_set:
                if g == gid:
                    continue
                if re.search(rf"\b{re.escape(g)}\b", sources):
                    refs.append(g)
            group_refs[gid] = refs

        def resolve_group_units(gid: str, visiting: Optional[set] = None) -> List[str]:
            if visiting is None:
                visiting = set()
            if gid in visiting:
                return []
            visiting.add(gid)
            units = list(group_units.get(gid, []))
            for ref in group_refs.get(gid, []):
                units.extend(resolve_group_units(ref, visiting))
            visiting.remove(gid)
            seen = set()
            out = []
            for u in units:
                if u and u not in seen:
                    out.append(u)
                    seen.add(u)
            return out

        table_units = []
        for row in rows_as_objects:
            gid = row.get("Tank Group", "")
            if not gid:
                continue
            resolved = resolve_group_units(gid)
            row["applicable_units"] = resolved
            table_units.extend(resolved)

        applicable_units = sorted(set(table_units))

    return {
        "title": title,
        "applicable_units": applicable_units or sorted(set(table_units)),
        "headers": headers,
        "rows_as_objects": rows_as_objects,
        "note_rows": note_rows,
    }


def add_content(target: Dict[str, Any], elem: Dict[str, Any]) -> None:
    target["content"].append(elem)


def build_json(doc: Document) -> Dict[str, Any]:
    root: Dict[str, Any] = {
        "source": {"type": "docx"},
        "front_matter": [],
        "sections": [],
    }

    section_stack: List[Dict[str, Any]] = []

    def current_container() -> Dict[str, Any]:
        return section_stack[-1] if section_stack else None

    for block in iter_block_items(doc):
        if isinstance(block, Paragraph):
            text = block.text
            style = block.style.name if block.style is not None else ""

            if not text:
                continue

            if style == "Contents" or text.strip().upper() == "TABLE OF CONTENTS":
                section = {
                    "title": text,
                    "level": 1,
                    "kind": "table_of_contents",
                    "content": [],
                    "sections": [],
                    "style": style,
                }
                root["sections"].append(section)
                section_stack = [section]
                continue

            h_level = heading_level(style)
            if h_level is not None:
                section = {
                    "title": text,
                    "level": h_level,
                    "content": [],
                    "sections": [],
                    "style": style,
                }
                while section_stack and section_stack[-1]["level"] >= h_level:
                    section_stack.pop()
                if section_stack:
                    section_stack[-1]["sections"].append(section)
                else:
                    root["sections"].append(section)
                section_stack.append(section)
                continue

            toc_lvl = toc_level(style)
            if toc_lvl is not None:
                elem = {
                    "type": "toc_entry",
                    "level": toc_lvl,
                    "text": text,
                    "style": style,
                }
            else:
                bullet_lvl = bullet_level(style)
                if bullet_lvl is not None:
                    elem = {
                        "type": "list_item",
                        "level": bullet_lvl,
                        "text": text,
                        "style": style,
                    }
                else:
                    elem = {
                        "type": "paragraph",
                        "text": text,
                        "style": style,
                    }

            if section_stack:
                add_content(section_stack[-1], elem)
            else:
                root["front_matter"].append(elem)

        elif isinstance(block, Table):
            elem = {
                "type": "table",
                "rows_raw": table_to_matrix(block),
            }
            elem.update(normalize_table(elem["rows_raw"]))
            if section_stack:
                add_content(section_stack[-1], elem)
            else:
                root["front_matter"].append(elem)

    apply_cross_table_rules(root)
    apply_permit_conditions_rules(root)
    return root


def iter_tables_in_sections(sections: List[Dict[str, Any]]) -> Iterable[Dict[str, Any]]:
    for sec in sections:
        for item in sec.get("content", []):
            if item.get("type") == "table":
                yield item
        for t in iter_tables_in_sections(sec.get("sections", [])):
            yield t


def apply_cross_table_rules(root: Dict[str, Any]) -> None:
    tables = list(iter_tables_in_sections(root.get("sections", [])))
    table_iv_f2 = None
    table_iv_f3 = None
    table_vii_f3 = None
    for t in tables:
        title = (t.get("title") or "").upper()
        if "TABLE IV" in title and "F.2" in title:
            table_iv_f2 = t
        if "TABLE IV" in title and "F.3" in title:
            table_iv_f3 = t
        if "TABLE VII" in title and "F.3" in title:
            table_vii_f3 = t

    if not table_iv_f2 or (not table_iv_f3 and not table_vii_f3):
        return

    group_units: Dict[str, List[str]] = {}
    for row in table_iv_f2.get("rows_as_objects", []):
        gid = row.get("Tank Group", "")
        units = row.get("applicable_units", []) or []
        if gid:
            group_units[gid] = units

    if not group_units:
        return

    def parse_group_header(h: str) -> tuple[str, str]:
        h = h.strip()
        m = re.match(r"^(\d+)\s*([A-D]+)?$", h)
        if not m:
            return ("", "")
        base = m.group(1)
        suffix = m.group(2) or ""
        return (base, suffix)

    def apply_group_units(table: Dict[str, Any]) -> None:
        headers = table.get("headers") or []
        rows = table.get("rows_as_objects", [])
        for row in rows:
            applicable: List[str] = []
            for h in headers:
                if h in ("Regulation", "Description", "FE Y/N", "Type", "Citation", "Future Effective Date", "Limit", "Monitoring", "Source #"):
                    continue
                base, suffix = parse_group_header(h)
                if not base:
                    continue
                cell = row.get(h, "").strip().upper()
                if not cell:
                    continue
                if cell == "X":
                    if suffix:
                        for letter in suffix:
                            applicable.extend(group_units.get(f"{base}{letter}", []))
                    else:
                        applicable.extend(group_units.get(base, []))
                    continue
                letters = re.findall(r"[A-D]", cell)
                if not letters:
                    continue
                for letter in letters:
                    applicable.extend(group_units.get(f"{base}{letter}", []))

            seen = set()
            dedup = []
            for u in applicable:
                if u and u not in seen:
                    dedup.append(u)
                    seen.add(u)
            row["applicable_units"] = dedup

    if table_iv_f3:
        apply_group_units(table_iv_f3)
    if table_vii_f3:
        apply_group_units(table_vii_f3)


def apply_permit_conditions_rules(root: Dict[str, Any]) -> None:
    permit = None
    for sec in root.get("sections", []):
        if sec.get("title") == "PERMIT CONDITIONS":
            permit = sec
            break
    if not permit:
        return

    basis_pat = re.compile(r"^\(?\s*basis\s*:", re.IGNORECASE)

    for cond in permit.get("sections", []):
        content = cond.get("content", [])
        if not content:
            continue

        first_li = None
        for i, item in enumerate(content):
            if item.get("type") == "list_item":
                first_li = i
                break

        pre_text = ""
        if first_li is not None and first_li > 0:
            pre_text = "\n".join(
                [i.get("text", "") for i in content[:first_li] if i.get("type") == "paragraph"]
            )
        cond_units = extract_applicable_units(pre_text)

        counters: Dict[int, int] = {}
        new_content = []
        last_li = None
        for item in content:
            if item.get("type") != "list_item":
                new_content.append(item)
                continue

            text = item.get("text", "")
            if basis_pat.match(text.strip()):
                if last_li is not None:
                    last_li["text"] = (last_li.get("text", "") + " " + text).strip()
                else:
                    level = int(item.get("level", 1))
                    counters[level] = counters.get(level, 0) + 1
                    item["num"] = counters[level]
                    new_content.append(item)
                    last_li = item
                continue

            level = int(item.get("level", 1))
            counters[level] = counters.get(level, 0) + 1
            item["num"] = counters[level]
            new_content.append(item)
            last_li = item

        cond["content"] = new_content
        cond["applicable_units"] = list(cond_units)


def main() -> None:
    ap = argparse.ArgumentParser(description="Convert a Title V permit DOCX into ordered JSON.")
    ap.add_argument("docx", help="Path to DOCX")
    ap.add_argument("--out", default=None, help="Output JSON path")
    args = ap.parse_args()

    if not os.path.exists(args.docx):
        raise SystemExit(f"Input DOCX not found: {args.docx}")

    doc = Document(args.docx)
    if not args.out:
        ids = extract_source_ids(doc)
        suffix = "_".join(sorted(ids)) if ids else "title_v_permit"
        args.out = os.path.join("JSON", f"title_v_permit_{suffix}.json")
    data = build_json(doc)
    data["source"]["path"] = os.path.abspath(args.docx)

    out_dir = os.path.dirname(args.out)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(args.out)


if __name__ == "__main__":
    main()
