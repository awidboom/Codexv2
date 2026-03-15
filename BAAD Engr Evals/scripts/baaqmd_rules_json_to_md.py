#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


def _safe_filename(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "_", value).strip("_") or "untitled"


def _norm(value: Any) -> str:
    text = re.sub(r"\s+", " ", str(value or "")).strip()
    return (
        text.replace("â€“", "–")
        .replace("â€”", "—")
        .replace("â€™", "’")
        .replace("â€œ", "“")
        .replace("â€�", "”")
    )


def _emit_subsections(lines: list[str], subsections: list[dict[str, Any]], level: int) -> None:
    heading = "#" * min(level, 6)
    for item in subsections:
        label = _norm(item.get("label"))
        title = _norm(item.get("title"))
        header = " ".join(part for part in [label, title] if part).strip() or "Subsection"
        lines.append(f"{heading} {header}")
        lines.append("")
        for para in item.get("text") or []:
            para = _norm(para)
            if para:
                lines.append(para)
                lines.append("")
        _emit_subsections(lines, item.get("subsections") or [], level + 1)


def rule_json_to_md(obj: dict[str, Any], source_path: Path) -> str:
    lines: list[str] = []
    lines.append("---")
    for key in [
        "rule_number",
        "title",
        "source_url",
        "local_pdf",
        "rule_page_url",
        "version_status",
        "adopted",
        "amended",
    ]:
        value = obj.get(key)
        if value:
            lines.append(f"{key}: {_norm(value)}")
    lines.append(f"source_json: {source_path.as_posix()}")
    lines.append("---")
    lines.append("")

    title = _norm(obj.get("title") or obj.get("rule_number") or source_path.stem)
    lines.append(f"# {title}")
    lines.append("")

    desc = _norm(obj.get("description"))
    if desc:
        lines.append("## Description")
        lines.append("")
        lines.append(desc)
        lines.append("")

    contact = _norm(obj.get("contact"))
    if contact:
        lines.append("## Contact")
        lines.append("")
        lines.append(contact)
        lines.append("")

    lines.append("## Sections")
    lines.append("")
    for section in obj.get("sections") or []:
        section_id = _norm(section.get("section_id"))
        section_title = _norm(section.get("section_title"))
        header = " ".join(part for part in [section_id, section_title] if part).strip() or "Section"
        lines.append(f"### {header}")
        lines.append("")
        history = section.get("history") or []
        if history:
            lines.append("**History**")
            lines.append("")
            for item in history:
                item = _norm(item)
                if item:
                    lines.append(f"- {item}")
            lines.append("")
        for para in section.get("text") or []:
            para = _norm(para)
            if para:
                lines.append(para)
                lines.append("")
        _emit_subsections(lines, section.get("subsections") or [], 4)

    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Convert BAAQMD rule JSON files to Markdown for RAG.")
    parser.add_argument("--json-folder", default="baaqmd_rules/json")
    parser.add_argument("--out-folder", default="baaqmd_rules/rag_md")
    args = parser.parse_args()

    json_folder = Path(args.json_folder)
    out_folder = Path(args.out_folder)
    out_folder.mkdir(parents=True, exist_ok=True)

    written = 0
    for path in sorted(json_folder.glob("*.json")):
        obj = json.loads(path.read_text(encoding="utf-8"))
        stem = _safe_filename(path.stem)
        out_path = out_folder / f"{stem}.md"
        out_path.write_text(rule_json_to_md(obj, path), encoding="utf-8")
        written += 1

    print(f"Wrote {written} markdown files to {out_folder}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
