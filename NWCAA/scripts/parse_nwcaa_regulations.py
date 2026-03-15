import argparse
import json
import os
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Optional


_SECTION_RE = re.compile(r"^\s*SECTION\s+(?P<section_id>\d{1,3})\s*-\s*(?P<title>.+?)\s*$")
_RULE_RE = re.compile(r"^\s*(?P<rule_id>\d{1,3}\.\d{1,3})\s+(?P<rest>.+?)\s*$")
_RULE_WITH_LETTER_RE = re.compile(
    r"^\s*(?P<rule_id>\d{1,3}\.\d{1,3})\((?P<label>[A-Z])\)\s*(?P<rest>.*)\s*$"
)
_SUBLABEL_RE = re.compile(r"^\s*\((?P<label>[A-Za-z]|\d+)\)\s+(?P<rest>.+?)\s*$")
_DEF_SPLIT_RE = re.compile(r"\s+[-–—]\s+")


def _normalize_text(raw: str) -> str:
    # Normalize a few common PDF-to-text artifacts.
    raw = raw.replace("\f", "\n")
    raw = raw.replace("\u00a0", " ")

    # Common mojibake for en dash/em dash when UTF-8 bytes are decoded as cp1252.
    raw = raw.replace("â€“", "-").replace("â€”", "-")
    raw = raw.replace("â€™", "'").replace("â€œ", '"').replace("â€", '"')
    raw = raw.replace("–", "-").replace("—", "-").replace("−", "-")

    # A frequent stray byte marker from PDF extraction.
    raw = raw.replace("Â", "")
    return raw


def _looks_like_page_number(line: str) -> bool:
    s = line.strip()
    if not s:
        return False
    if re.fullmatch(r"\d{1,4}-\d{1,4}", s):
        return True
    return False


def _drop_headers_footers(lines: list[str]) -> list[str]:
    out: list[str] = []
    for line in lines:
        if "REGULATION OF THE NORTHWEST CLEAN AIR AGENCY" in line.upper():
            continue
        if _looks_like_page_number(line):
            continue
        out.append(line.rstrip("\n"))
    return out


def _join_wrapped_lines(lines: list[str]) -> str:
    # Join lines into a single paragraph, attempting to undo hyphenation at line breaks.
    parts: list[str] = []
    for line in lines:
        s = line.strip()
        if not s:
            continue
        if not parts:
            parts.append(s)
            continue
        prev = parts[-1]
        if prev.endswith("-") and s and s[0].islower():
            parts[-1] = prev[:-1] + s
        else:
            parts[-1] = prev + " " + s
    return parts[-1] if parts else ""


def _label_level(label: str) -> int:
    if label.isdigit():
        return 2
    if len(label) == 1 and label.isalpha():
        return 1 if label.isupper() else 3
    return 9


def _infer_doc_date_from_path(path: str) -> Optional[str]:
    # Matches e.g. NWCAA-Regulations-2025_08_10.txt
    m = re.search(r"(\d{4})_(\d{2})_(\d{2})", os.path.basename(path))
    if not m:
        return None
    yyyy, mm, dd = m.group(1), m.group(2), m.group(3)
    return f"{yyyy}-{mm}-{dd}"


def _parse_definition_header(line: str) -> Optional[tuple[str, str]]:
    # In SECTION 200 (Definitions), terms are presented as:
    #   TERM - Definition...
    # where TERM is typically uppercase (sometimes contains small words like "or").
    parts = _DEF_SPLIT_RE.split(line.strip(), maxsplit=1)
    if len(parts) != 2:
        return None
    term, rest = parts[0].strip(), parts[1].strip()
    if not term or not rest:
        return None
    if term.upper().startswith("SECTION ") or term.upper().startswith("PASSED:") or term.upper().startswith("AMENDED:"):
        return None
    if term.endswith("."):
        return None

    alpha = [c for c in term if c.isalpha()]
    if len(alpha) < 3:
        return None
    uppercase = sum(1 for c in alpha if c.isupper())
    # Accept "AIR CONTAMINANT or AIR POLLUTANT" etc.
    if uppercase / len(alpha) < 0.6:
        return None
    return term, rest


@dataclass
class _Cursor:
    rule: Optional[dict[str, Any]] = None
    # Stack of subsection nodes currently open; the rule is the implicit root.
    subsection_stack: list[dict[str, Any]] = None
    pending_lines: list[str] = None

    def __post_init__(self) -> None:
        self.subsection_stack = []
        self.pending_lines = []

    def current_container(self) -> Optional[dict[str, Any]]:
        if self.subsection_stack:
            return self.subsection_stack[-1]
        return self.rule

    def flush_paragraph(self) -> None:
        if not self.pending_lines:
            return
        paragraph = _join_wrapped_lines(self.pending_lines)
        self.pending_lines = []
        if not paragraph:
            return
        container = self.current_container()
        if not container:
            return
        container["text"].append(paragraph)


def parse_nwcaa_regulations_text(text: str, input_path: str) -> dict[str, Any]:
    normalized = _normalize_text(text)
    lines = normalized.splitlines()
    lines = _drop_headers_footers(lines)

    sections: list[dict[str, Any]] = []
    current_section: Optional[dict[str, Any]] = None
    seen_first_section = False
    cursor = _Cursor()

    def start_section(section_id: str, title: str) -> None:
        nonlocal current_section, cursor, seen_first_section
        if cursor.rule:
            cursor.flush_paragraph()
            cursor.rule = None
            cursor.subsection_stack = []
        if current_section:
            sections.append(current_section)
        current_section = {
            "section_id": section_id,
            "section_title": title.strip(),
            "history": [],
            "rules": [],
        }
        seen_first_section = True

    def start_rule(rule_id: str, rule_title: Optional[str]) -> None:
        nonlocal cursor, current_section
        if not current_section:
            # Ignore table-of-contents / preamble fragments before the first SECTION header.
            return
        if cursor.rule:
            cursor.flush_paragraph()
            cursor.rule = None
            cursor.subsection_stack = []
        rule: dict[str, Any] = {
            "rule_id": rule_id,
            "text": [],
            "subsections": [],
        }
        if rule_title:
            rule["rule_title"] = rule_title
        current_section["rules"].append(rule)
        cursor.rule = rule

    for raw_line in lines:
        line = raw_line.rstrip()
        if not line.strip():
            cursor.flush_paragraph()
            continue

        # Section boundaries.
        m_sec = _SECTION_RE.match(line)
        if m_sec:
            start_section(m_sec.group("section_id"), m_sec.group("title"))
            continue

        # History lines in the consolidated regulations PDF.
        if line.strip().upper().startswith("PASSED:") or line.strip().upper().startswith("AMENDED:"):
            if not current_section:
                continue
            current_section["history"].append(_join_wrapped_lines([line]))
            continue

        # SECTION 200 (Definitions): treat each definition term as an unnumbered "rule".
        if current_section and current_section["section_id"] == "200":
            def_hdr = _parse_definition_header(line)
            if def_hdr:
                term, rest = def_hdr
                if cursor.rule:
                    cursor.flush_paragraph()
                    cursor.rule = None
                    cursor.subsection_stack = []
                start_rule(term, None)
                if cursor.rule:
                    cursor.pending_lines.append(rest)
                continue

        # Rule boundaries.
        m_rule_letter = _RULE_WITH_LETTER_RE.match(line)
        if m_rule_letter:
            if raw_line[:1].isspace() and cursor.rule:
                # A wrapped reference like "300.9(C)" can land at column 0 in a PDF extract.
                # If it is indented and we're already inside a rule, treat it as body text.
                cursor.pending_lines.append(line)
                continue
            rule_id = m_rule_letter.group("rule_id")
            label = m_rule_letter.group("label")
            rest = m_rule_letter.group("rest").strip()
            if not cursor.rule or cursor.rule.get("rule_id") != rule_id:
                start_rule(rule_id, None)
            if not cursor.rule:
                continue
            # Treat as a subsection line on first encounter.
            cursor.flush_paragraph()
            node = {"label": label, "text": [], "subsections": []}
            cursor.rule["subsections"].append(node)
            cursor.subsection_stack = [node]
            if rest:
                cursor.pending_lines.append(rest)
            continue

        m_rule = _RULE_RE.match(line)
        if m_rule:
            rule_id = m_rule.group("rule_id")
            rest = m_rule.group("rest").strip()

            if rest and rest[0].islower() and cursor.rule:
                # Common PDF wrapping can put references like "300.9 and ..." at column 0.
                # Treat these as normal content lines, not new rule starts.
                cursor.pending_lines.append(line)
                continue

            # Heuristic: treat short, punctuation-free fragments as titles (not body text).
            rule_title: Optional[str] = None
            if (
                rest
                and rest[0].isupper()
                and ("," not in rest)
                and ("." not in rest)
                and (len(rest) <= 120)
            ):
                rule_title = rest
                start_rule(rule_id, rule_title)
            else:
                start_rule(rule_id, None)
                if not cursor.rule:
                    continue
                cursor.pending_lines.append(rest)
            continue

        # Subsection labels.
        m_sub = _SUBLABEL_RE.match(line)
        if m_sub and cursor.rule:
            label = m_sub.group("label")
            rest = m_sub.group("rest").strip()
            cursor.flush_paragraph()

            level = _label_level(label)
            while cursor.subsection_stack and _label_level(cursor.subsection_stack[-1]["label"]) >= level:
                cursor.subsection_stack.pop()

            node = {"label": label, "text": [], "subsections": []}
            parent = cursor.subsection_stack[-1] if cursor.subsection_stack else cursor.rule
            parent["subsections"].append(node)
            cursor.subsection_stack.append(node)
            cursor.pending_lines.append(rest)
            continue

        # Default: content line.
        if cursor.rule:
            cursor.pending_lines.append(line)
        else:
            # Ignore preamble text outside any parsed section/rule.
            continue

    # Finalize.
    cursor.flush_paragraph()
    if current_section:
        sections.append(current_section)

    # Remove empty history arrays for compactness.
    for s in sections:
        if not s["history"]:
            s.pop("history", None)

    generated_at = datetime.now(timezone.utc).isoformat()
    result: dict[str, Any] = {
        "source": {
            "input_path": input_path,
            "generated_at": generated_at,
            "document_name": os.path.basename(input_path),
        },
        "sections": sections,
    }
    doc_date = _infer_doc_date_from_path(input_path)
    if doc_date:
        result["source"]["document_date"] = doc_date
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Parse NWCAA consolidated regulations text into JSON.")
    parser.add_argument("--input", required=True, help="Path to NWCAA-Regulations-*.txt")
    parser.add_argument("--output", required=True, help="Path to write JSON output")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON (indent=2)")
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8", errors="replace") as f:
        text = f.read()

    parsed = parse_nwcaa_regulations_text(text=text, input_path=args.input)

    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(parsed, f, indent=2 if args.pretty else None, ensure_ascii=False)
        f.write("\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
