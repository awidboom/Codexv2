#!/usr/bin/env python3
"""Download Bay Area (BAAQMD) current-rule PDFs and build one JSON per rule.

This script mirrors the NWCAA parser workflow, but targets BAAQMD's
"Current Rules" page:
https://www.baaqmd.gov/en/rules-and-compliance/current-rules

Outputs are written under:
  BAAD Engr Evals/baaqmd_rules/
    ├── pdfs/
    ├── json/
    └── manifest.json
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import html
import json
import os
import re
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen

from PyPDF2 import PdfReader

CURRENT_RULES_URL = "https://www.baaqmd.gov/en/rules-and-compliance/current-rules"
USER_AGENT = "Mozilla/5.0 (compatible; BAAD-RegParser/1.0; +https://www.baaqmd.gov)"


@dataclass(frozen=True)
class RulePdf:
    title: str
    url: str
    rule_no: str | None
    metadata: dict | None = None


def fetch_url_text(url: str, timeout_s: int) -> str:
    req = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(req, timeout=timeout_s) as resp:
        encoding = resp.headers.get_content_charset() or "utf-8"
        return resp.read().decode(encoding, errors="replace")


def fetch_url_bytes(url: str, timeout_s: int) -> bytes:
    req = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(req, timeout=timeout_s) as resp:
        return resp.read()


def fetch_url_json(url: str, timeout_s: int) -> dict | list:
    req = Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "application/json",
        },
    )
    with urlopen(req, timeout=timeout_s) as resp:
        encoding = resp.headers.get_content_charset() or "utf-8"
        return json.loads(resp.read().decode(encoding, errors="replace"))


def iter_pdf_links(page_html: str, base_url: str) -> Iterable[tuple[str, str]]:
    # Extract <a ... href="...pdf">text</a> links.
    anchor_re = re.compile(
        r"<a\b[^>]*?href\s*=\s*(['\"])(?P<href>[^'\"]+)\1[^>]*>(?P<text>.*?)</a>",
        flags=re.IGNORECASE | re.DOTALL,
    )
    tag_re = re.compile(r"<[^>]+>")

    for m in anchor_re.finditer(page_html):
        href = html.unescape(m.group("href")).strip()
        if ".pdf" not in href.lower():
            continue

        full_url = urljoin(base_url, href)
        parsed = urlparse(full_url)
        if not parsed.scheme.startswith("http"):
            continue

        link_text = tag_re.sub(" ", m.group("text"))
        link_text = re.sub(r"\s+", " ", html.unescape(link_text)).strip()
        yield link_text, full_url


def parse_rule_number(value: str) -> str | None:
    m = re.search(r"\b(?:rule\s*)?(\d+(?:\.\d+)?)\b", value, flags=re.IGNORECASE)
    return m.group(1) if m else None


def safe_slug(value: str) -> str:
    slug = value.lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug).strip("-")
    return slug or "untitled"


def build_rule_objects(page_html: str, source_url: str) -> list[RulePdf]:
    seen_urls: set[str] = set()
    rules: list[RulePdf] = []

    for text, full_url in iter_pdf_links(page_html, source_url):
        normalized = full_url.split("#", 1)[0]
        if normalized in seen_urls:
            continue
        seen_urls.add(normalized)

        file_name = Path(urlparse(normalized).path).name
        rule_no = parse_rule_number(text) or parse_rule_number(file_name)
        title = text or file_name

        rules.append(RulePdf(title=title, url=normalized, rule_no=rule_no))

    return rules


def strip_tags(value: str) -> str:
    value = re.sub(r"<[^>]+>", " ", value or "")
    value = html.unescape(value)
    return normalize_extracted_text(value)


def normalize_extracted_text(value: str) -> str:
    text = re.sub(r"\s+", " ", value or "").strip()
    if not text:
        return ""

    text = re.sub(r"(?<=\d)-\s+(?=\d)", "-", text)
    text = re.sub(r"\s+([,.;:)\]])", r"\1", text)
    text = re.sub(r"([(\[])\s+", r"\1", text)
    text = re.sub(r";(?=\S)", "; ", text)
    text = re.sub(r":(?=\S)", ": ", text)
    text = re.sub(r",(?=\S)", ", ", text)
    text = re.sub(r"\s{2,}", " ", text)

    replacements = [
        ("sec tion", "section"),
        ("Regul ation", "Regulation"),
        ("modifi cation", "modification"),
        ("exe mpt", "exempt"),
        ("a nd", "and"),
        ("f ollowing", "following"),
        ("compos ting", "composting"),
        ("Construct ion", "Construction"),
        ("Operat ion", "Operation"),
        ("Appli cation", "Application"),
        ("Envi ronmental", "Environmental"),
        ("P ermit", "Permit"),
        ("O perate", "Operate"),
        ("nonagricultural", "non-agricultural"),
        ("greenhouse gases ,", "greenhouse gases,"),
        ("th is", "this"),
        ("Renumbered and Amended", "Renumbered and Amended"),
    ]
    for old, new in replacements:
        text = text.replace(old, new)

    return text.strip()


def clean_join(parts: list[str]) -> str:
    out = ""
    for part in parts:
        piece = normalize_extracted_text(part)
        if not piece:
            continue
        if not out:
            out = piece
            continue
        if out.endswith("-"):
            out = out[:-1] + piece
        else:
            out = out + " " + piece
    return out.strip()


def normalize_rule_pdf_lines(text: str) -> list[str]:
    start_match = re.search(r"\(Adopted [^)]+\)", text)
    if start_match:
        text = text[start_match.start() :]
    lines: list[str] = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            lines.append("")
            continue
        if "Bay Area Air Quality Management Distri" in line:
            continue
        if line == "INDEX" or re.fullmatch(r"REGULATION \d+", line) or re.fullmatch(r"RULE \d+", line):
            continue
        line = re.sub(r"^\d+(?:-\d+)+\s+(?=\()", "", line)
        line = re.sub(r"^\d+(?:-\d+)+\s+(?=(?:\d+(?:-\d+)+-\d{3}|\d+\.\d+(?:\.\d+)*)\s)", "", line)
        if re.fullmatch(r"\d+(?:-\d+)+", line):
            continue
        lines.append(line)
    return lines


def add_text(target: dict, text: str) -> None:
    text = normalize_extracted_text(text)
    if not text:
        return
    target.setdefault("text", [])
    if target["text"]:
        if re.search(r"[.;:)]$", target["text"][-1]):
            target["text"].append(text)
        else:
            target["text"][-1] = clean_join([target["text"][-1], text])
    else:
        target["text"].append(text)


def subsection_level(label: str, section_id: str) -> int:
    if re.fullmatch(r"\d+\.\d+(?:\.\d+)*", label):
        if label.startswith(f"{section_id}."):
            return 1
        return label.count(".") + 1
    if re.fullmatch(r"\([ivxlcdm]+\)", label.lower()):
        return 4
    if re.fullmatch(r"\([a-z]+\)", label.lower()):
        return 3
    if re.fullmatch(r"[A-Z]\.", label):
        return 2
    if re.fullmatch(r"[a-z]\.", label):
        return 3
    return 1


def make_subsection(label: str, text: str) -> dict:
    subsection = {"label": label, "text": [], "subsections": []}
    add_text(subsection, text)
    return subsection


def extract_rule_sections_from_pdf(pdf_path: Path) -> list[dict]:
    reader = PdfReader(str(pdf_path))
    full_text = "\n".join((page.extract_text() or "") for page in reader.pages)
    lines = normalize_rule_pdf_lines(full_text)
    section_re = re.compile(r"^\d+(?:-\d+)+-(\d{3})\s+(.+)$")
    subsection_re = re.compile(
        r"^(?P<label>\d+\.\d+(?:\.\d+)*|\([ivxlcdm]+\)|\([a-z]+\)|[A-Z]\.|[a-z]\.)\s+(?P<text>.+)$",
        flags=re.IGNORECASE,
    )
    history_re = re.compile(r"^\((Adopted|Amended|Readopted|Repealed|Renumbered|Deleted).+\)$", flags=re.IGNORECASE)

    sections: list[dict] = []
    current_section: dict | None = None
    stack: list[tuple[int, dict]] = []

    def flush_stack(level: int) -> None:
        while stack and stack[-1][0] >= level:
            stack.pop()

    for line in lines:
        if not line:
            continue

        section_match = section_re.match(line)
        if section_match:
            section_id = section_match.group(1)
            remainder = section_match.group(2).strip()
            section_title = remainder
            inline_text = ""
            if ":" in remainder:
                section_title, inline_text = remainder.split(":", 1)
                section_title = section_title.strip()
                inline_text = inline_text.strip()
            current_section = {
                "section_id": section_id,
                "section_title": normalize_extracted_text(section_title),
                "history": [],
                "text": [],
                "subsections": [],
            }
            if inline_text:
                add_text(current_section, inline_text)
            sections.append(current_section)
            stack = []
            continue

        if current_section is None:
            continue

        if history_re.match(line):
            current_section["history"].append(normalize_extracted_text(line.strip()[1:-1].strip()))
            continue

        subsection_match = subsection_re.match(line)
        if subsection_match:
            label = subsection_match.group("label")
            text_value = subsection_match.group("text")
            level = subsection_level(label, current_section["section_id"])
            flush_stack(level)
            subsection = make_subsection(label, text_value)
            if stack:
                stack[-1][1]["subsections"].append(subsection)
            else:
                current_section["subsections"].append(subsection)
            stack.append((level, subsection))
            continue

        if stack:
            add_text(stack[-1][1], line)
        else:
            add_text(current_section, line)

    for section in sections:
        section["history"] = [item for item in section["history"] if item]
    return sections


def extract_first_pdf_link(fragment: str, base_url: str) -> tuple[str, str] | None:
    if not fragment:
        return None
    anchor_re = re.compile(
        r"<a\b[^>]*?href\s*=\s*(['\"])(?P<href>[^'\"]+\.pdf[^'\"]*)\1[^>]*>(?P<text>.*?)</a>",
        flags=re.IGNORECASE | re.DOTALL,
    )
    match = anchor_re.search(fragment)
    if not match:
        return None
    href = urljoin(base_url, html.unescape(match.group("href")).strip())
    text = strip_tags(match.group("text"))
    return text, href


def extract_table_block_params(page_html: str) -> tuple[str, str, str, str, str] | None:
    pattern = re.compile(
        r'new TableBlock\("(?P<page_id>[^"]+)",\s*"(?P<container_id>[^"]+)",\s*"(?P<data_source_id>[^"]+)",\s*(?P<rendering_hash>-?\d+),\s*renderingParams,\s*strings,\s*"(?P<lang>[^"]*)"\)',
        flags=re.IGNORECASE,
    )
    match = pattern.search(page_html)
    if not match:
        return None
    return (
        match.group("page_id"),
        match.group("container_id"),
        match.group("data_source_id"),
        match.group("rendering_hash"),
        match.group("lang") or "en",
    )


def build_rule_objects_from_table_api(page_html: str, source_url: str, timeout_s: int) -> list[RulePdf]:
    params = extract_table_block_params(page_html)
    if not params:
        return []

    page_id, _container_id, data_source_id, rendering_hash, lang = params
    base_url = f"https://www.baaqmd.gov/{lang}/api/admin/table"
    encoded_data_source = base64.b64encode(data_source_id.encode("utf-8")).decode("ascii")
    data_url = f"{base_url}/data/{page_id}/{encoded_data_source}/{rendering_hash}"
    payload = fetch_url_json(data_url, timeout_s=timeout_s)
    rows = payload.get("Data", []) if isinstance(payload, dict) else []

    rules: list[RulePdf] = []
    for row in rows:
        link = extract_first_pdf_link(row.get("AdoptedDocument", ""), source_url)
        title = strip_tags(row.get("Name", ""))
        rule_no = strip_tags(row.get("RuleNumber", "")) or None
        rule_url_match = re.search(r'href\s*=\s*["\'](?P<href>[^"\']+)["\']', row.get("Name", ""), flags=re.IGNORECASE)
        rule_page_url = urljoin(source_url, html.unescape(rule_url_match.group("href"))) if rule_url_match else None
        metadata = {
            "rule_page_url": rule_page_url,
            "version_status": strip_tags(row.get("VersionStatus", "")) or None,
            "adopted": row.get("Adopted"),
            "amended": row.get("Amended"),
            "description": strip_tags(row.get("Description", "")) or None,
            "contact": strip_tags(row.get("Contact", "")) or None,
        }
        if link:
            link_text, pdf_url = link
            rules.append(
                RulePdf(
                    title=link_text or title,
                    url=pdf_url,
                    rule_no=rule_no,
                    metadata=metadata,
                )
            )
        else:
            rules.append(
                RulePdf(
                    title=title,
                    url="",
                    rule_no=rule_no,
                    metadata={**metadata, "download_available": False},
                )
            )

    return rules


def download_rule_pdf(rule: RulePdf, pdf_dir: Path, timeout_s: int, delay_s: float) -> dict:
    if not rule.url:
        return {
            "rule_number": rule.rule_no,
            "title": rule.title,
            "source_url": None,
            "local_pdf": None,
            "sha256": None,
            "bytes": 0,
            **(rule.metadata or {}),
        }

    url_path_name = Path(urlparse(rule.url).path).name
    base_name = f"rule_{rule.rule_no}" if rule.rule_no else safe_slug(rule.title)
    ext = Path(url_path_name).suffix or ".pdf"
    pdf_name = safe_slug(base_name) + ext.lower()
    pdf_path = pdf_dir / pdf_name

    if not pdf_path.exists():
        payload = fetch_url_bytes(rule.url, timeout_s)
        pdf_path.write_bytes(payload)
        if delay_s > 0:
            time.sleep(delay_s)

    file_bytes = pdf_path.read_bytes()
    sections = extract_rule_sections_from_pdf(pdf_path)

    return {
        "rule_number": rule.rule_no,
        "title": rule.title,
        "source_url": rule.url,
        "local_pdf": str(pdf_path),
        "sha256": hashlib.sha256(file_bytes).hexdigest(),
        "bytes": len(file_bytes),
        "sections": sections,
        **(rule.metadata or {}),
    }


def write_json_records(records: list[dict], json_dir: Path) -> None:
    for record in records:
        rule_no = record.get("rule_number")
        stem = f"rule_{rule_no}" if rule_no else safe_slug(record["title"])
        out_path = json_dir / f"{safe_slug(stem)}.json"
        out_path.write_text(json.dumps(record, indent=2), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source-url",
        default=CURRENT_RULES_URL,
        help="BAAQMD source page containing links to rule PDFs.",
    )
    parser.add_argument(
        "--out-root",
        default="baaqmd_rules",
        help="Folder where PDFs/JSON/manifest are generated.",
    )
    parser.add_argument("--timeout", type=int, default=45, help="HTTP timeout in seconds.")
    parser.add_argument("--delay", type=float, default=0.15, help="Delay between PDF downloads.")
    parser.add_argument(
        "--max-rules",
        type=int,
        default=0,
        help="If >0, only process this many PDFs (useful for testing).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Discover rule PDFs and print summary without downloading files.",
    )
    args = parser.parse_args()

    out_root = Path(args.out_root)
    pdf_dir = out_root / "pdfs"
    json_dir = out_root / "json"
    out_root.mkdir(parents=True, exist_ok=True)
    pdf_dir.mkdir(parents=True, exist_ok=True)
    json_dir.mkdir(parents=True, exist_ok=True)

    try:
        page_html = fetch_url_text(args.source_url, timeout_s=args.timeout)
    except (HTTPError, URLError, TimeoutError) as exc:
        print(f"Failed to fetch source page: {exc}", file=sys.stderr)
        return 2

    rules = build_rule_objects_from_table_api(page_html, args.source_url, timeout_s=args.timeout)
    if not rules:
        rules = build_rule_objects(page_html, args.source_url)
    if args.max_rules > 0:
        rules = rules[: args.max_rules]

    print(f"Discovered {len(rules)} PDF links from {args.source_url}")
    if args.dry_run:
        for idx, rule in enumerate(rules, start=1):
            rn = f"Rule {rule.rule_no}" if rule.rule_no else "Rule ?"
            url = rule.url or "[no downloadable PDF]"
            print(f"{idx:03d}. {rn} :: {rule.title} :: {url}")
        return 0

    records: list[dict] = []
    for idx, rule in enumerate(rules, start=1):
        try:
            rec = download_rule_pdf(rule, pdf_dir=pdf_dir, timeout_s=args.timeout, delay_s=args.delay)
            records.append(rec)
            print(f"[{idx}/{len(rules)}] downloaded {rec['local_pdf']}")
        except (HTTPError, URLError, TimeoutError) as exc:
            print(f"[{idx}/{len(rules)}] skipped {rule.url}: {exc}", file=sys.stderr)

    write_json_records(records, json_dir)
    manifest_path = out_root / "manifest.json"
    manifest = {
        "source_url": args.source_url,
        "generated_at_epoch": int(time.time()),
        "total_links_found": len(rules),
        "records_written": len(records),
        "records": records,
    }
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"Wrote manifest: {manifest_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
