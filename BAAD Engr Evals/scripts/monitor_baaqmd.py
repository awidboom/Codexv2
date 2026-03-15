#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import html
import hashlib
import io
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from html.parser import HTMLParser
from typing import Any, Iterable, Optional


RE_URL = re.compile(r"https?://[^\s)>\"]+")
RE_GUID = re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", re.I)
RE_TABLEBLOCK = re.compile(
    r'new\s+TableBlock\(\s*"(?P<page_id>[0-9a-f-]{36})"\s*,\s*"(?P<container_id>[^"]+)"\s*,\s*"(?P<data_source>[^"]+)"\s*,\s*(?P<render_hash>-?\d+)',
    re.I,
)


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_text(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write_text(path: str, content: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)


def read_json(path: str) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path: str, obj: dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, sort_keys=True)
        f.write("\n")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_text(text: str) -> str:
    return sha256_bytes(text.encode("utf-8", errors="replace"))


def normalize_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def sanitize_filename(name: str) -> str:
    name = normalize_whitespace(name)
    name = re.sub(r"[<>:\"/\\\\|?*]+", "_", name)
    name = name.strip(" ._")
    return name[:180] if len(name) > 180 else name


def is_probably_pdf_url(url: str) -> bool:
    parsed = urllib.parse.urlparse(url)
    return parsed.path.lower().endswith(".pdf")


def is_probably_csv_url(url: str) -> bool:
    parsed = urllib.parse.urlparse(url)
    return parsed.path.lower().endswith(".csv") or "CsvExportUnfiltered" in parsed.path


def is_relevant_link_for_page(page_url: str, link_url: str) -> bool:
    if is_probably_pdf_url(link_url):
        return True
    page = urllib.parse.urlparse(page_url)
    link = urllib.parse.urlparse(link_url)
    if not link.scheme or not link.netloc:
        return False
    if link.netloc != page.netloc:
        return False
    if link.path.startswith("/~/media/"):
        return True
    page_path = page.path or "/"
    page_base = page_path if page_path.endswith("/") else page_path + "/"
    return link.path.startswith(page_base)


class MinimalHTMLExtractor(HTMLParser):
    def __init__(self, page_url: str):
        super().__init__(convert_charrefs=True)
        self._page_url = page_url
        self._ignore_depth = 0
        self._capture_title = False
        self._title_parts: list[str] = []
        self._text_parts: list[str] = []

        self._in_a = False
        self._a_href: Optional[str] = None
        self._a_text_parts: list[str] = []
        self.links: list[dict[str, str]] = []

    @property
    def title(self) -> str:
        return normalize_whitespace(" ".join(self._title_parts))

    @property
    def visible_text(self) -> str:
        return normalize_whitespace(" ".join(self._text_parts))

    def handle_starttag(self, tag: str, attrs: list[tuple[str, Optional[str]]]) -> None:
        tag_l = tag.lower()
        if tag_l in ("script", "style", "noscript"):
            self._ignore_depth += 1
            return
        if self._ignore_depth > 0:
            return

        if tag_l == "title":
            self._capture_title = True
            return

        if tag_l == "a":
            href = None
            for k, v in attrs:
                if k.lower() == "href":
                    href = v
                    break
            if href:
                self._in_a = True
                self._a_href = urllib.parse.urljoin(self._page_url, href)
                self._a_text_parts = []

    def handle_endtag(self, tag: str) -> None:
        tag_l = tag.lower()
        if tag_l in ("script", "style", "noscript"):
            if self._ignore_depth > 0:
                self._ignore_depth -= 1
            return
        if self._ignore_depth > 0:
            return

        if tag_l == "title":
            self._capture_title = False
            return

        if tag_l == "a" and self._in_a:
            text = normalize_whitespace(" ".join(self._a_text_parts))
            href = self._a_href or ""
            if href and is_relevant_link_for_page(self._page_url, href):
                self.links.append({"url": href, "text": text})
            self._in_a = False
            self._a_href = None
            self._a_text_parts = []

    def handle_data(self, data: str) -> None:
        if self._ignore_depth > 0:
            return
        if self._capture_title:
            self._title_parts.append(data)
            return
        text = data.strip()
        if not text:
            return
        self._text_parts.append(text)
        if self._in_a:
            self._a_text_parts.append(text)


class AnchorExtractor(HTMLParser):
    def __init__(self, page_url: str):
        super().__init__(convert_charrefs=True)
        self._page_url = page_url
        self._ignore_depth = 0
        self._in_a = False
        self._a_href: Optional[str] = None
        self._a_text_parts: list[str] = []
        self.anchors: list[dict[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, Optional[str]]]) -> None:
        tag_l = tag.lower()
        if tag_l in ("script", "style", "noscript"):
            self._ignore_depth += 1
            return
        if self._ignore_depth > 0:
            return
        if tag_l == "a":
            href = None
            for k, v in attrs:
                if k.lower() == "href":
                    href = v
                    break
            if href:
                self._in_a = True
                self._a_href = urllib.parse.urljoin(self._page_url, href)
                self._a_text_parts = []

    def handle_endtag(self, tag: str) -> None:
        tag_l = tag.lower()
        if tag_l in ("script", "style", "noscript"):
            if self._ignore_depth > 0:
                self._ignore_depth -= 1
            return
        if self._ignore_depth > 0:
            return
        if tag_l == "a" and self._in_a:
            text = normalize_whitespace(" ".join(self._a_text_parts))
            href = self._a_href or ""
            if href:
                self.anchors.append({"url": href, "text": text})
            self._in_a = False
            self._a_href = None
            self._a_text_parts = []

    def handle_data(self, data: str) -> None:
        if self._ignore_depth > 0:
            return
        text = data.strip()
        if not text:
            return
        if self._in_a:
            self._a_text_parts.append(text)


@dataclass(frozen=True)
class FetchResult:
    url: str
    final_url: str
    status: int
    content_type: str
    headers: dict[str, str]
    body: bytes


def fetch_url(url: str, *, method: str = "GET", timeout_s: int = 45) -> FetchResult:
    req = urllib.request.Request(
        url,
        method=method,
        headers={
            "User-Agent": "BAADMarketingMonitor/1.0 (+local script)",
            "Accept": "*/*",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout_s) as resp:
            body = resp.read() if method.upper() != "HEAD" else b""
            headers = {k.lower(): v for k, v in resp.headers.items()}
            return FetchResult(
                url=url,
                final_url=resp.geturl(),
                status=getattr(resp, "status", 200),
                content_type=headers.get("content-type", ""),
                headers=headers,
                body=body,
            )
    except urllib.error.HTTPError as e:
        headers = {k.lower(): v for k, v in e.headers.items()} if e.headers else {}
        body = e.read() if hasattr(e, "read") else b""
        return FetchResult(
            url=url,
            final_url=url,
            status=int(getattr(e, "code", 0) or 0),
            content_type=headers.get("content-type", ""),
            headers=headers,
            body=body,
        )


def content_type_family(content_type: str) -> str:
    ct = content_type.lower()
    if "text/html" in ct:
        return "html"
    if "text/csv" in ct or "application/csv" in ct:
        return "csv"
    if "application/pdf" in ct:
        return "pdf"
    if ct.startswith("text/"):
        return "text"
    return "binary"


def extract_urls_from_agents_md(agents_md_path: str) -> list[str]:
    text = read_text(agents_md_path)
    urls = sorted(set(RE_URL.findall(text)))
    return urls


def parse_permit_applications_csv(csv_bytes: bytes) -> list[dict[str, str]]:
    text = csv_bytes.decode("utf-8-sig", errors="replace")
    reader = csv.DictReader(io.StringIO(text, newline=""))
    rows: list[dict[str, str]] = []
    for row in reader:
        cleaned: dict[str, str] = {}
        for k, v in row.items():
            if k is None:
                continue
            cleaned[k.strip()] = (v or "").strip()
        if cleaned:
            rows.append(cleaned)
    return rows


def permit_row_stable_id(row: dict[str, str]) -> str:
    """
    "Recent Permit Applications" CSV does not expose an application number.

    We intentionally exclude fields that frequently change (e.g., Status, Badges)
    so that we can detect updates to an existing row instead of treating them as
    brand-new rows.
    """
    key_fields = (
        normalize_whitespace(row.get("Facility Number", "")),
        normalize_whitespace(row.get("Date", "")),
        normalize_whitespace(row.get("Application Name", "")),
        normalize_whitespace(row.get("Facility", "")),
        normalize_whitespace(row.get("Address", "")),
    )
    return sha256_text("\u241f".join(key_fields))


def permit_row_fingerprint(row: dict[str, str]) -> str:
    parts: list[str] = []
    for k in sorted(row.keys()):
        parts.append(f"{k}={normalize_whitespace(row.get(k, ''))}")
    return sha256_text("\u241f".join(parts))


def is_gasoline_dispensing(row: dict[str, str]) -> bool:
    name = (row.get("Application Name", "") + " " + row.get("Facility", "")).lower()
    return (
        "gasoline dispensing facility" in name
        or "gas dispensing facility" in name
        or "gas dispensing" in name
        or "gasoline dispensing" in name
        or "gdf" in name
    )


def is_emergency_generator_only(row: dict[str, str]) -> bool:
    name = (row.get("Application Name", "") + " " + row.get("Facility", "")).lower()
    return any(
        p in name
        for p in (
            "emergency generator",
            "standby generator",
            "backup generator",
            "emergency standby",
            "emergency stand-by",
            "standby diesel engine",
            "standby engine",
            "emergency engine",
        )
    )


def is_of_interest(row: dict[str, str], keywords: Iterable[str]) -> bool:
    hay = " ".join(
        [
            row.get("Application Name", ""),
            row.get("Facility", ""),
            row.get("Address", ""),
            row.get("City", ""),
            row.get("County", ""),
            row.get("Facility Type", ""),
            row.get("Plant Reference #", ""),
            row.get("Badges", ""),
        ]
    ).lower()
    return any(k.lower() in hay for k in keywords)


def format_permit_row(row: dict[str, str]) -> str:
    parts = [
        row.get("Date", "").split(" ")[0],
        row.get("Application Name", ""),
        normalize_whitespace(row.get("Facility", "")),
        f"Facility #{row.get('Facility Number','')}" if row.get("Facility Number") else "",
        row.get("City", ""),
        row.get("Status", ""),
    ]
    parts = [p for p in parts if p]
    return " - ".join(parts)


def diff_row_fields(prev: dict[str, str], cur: dict[str, str]) -> list[str]:
    fields_to_report = [
        "Status",
        "Badges",
        "Public Participation Period",
        "Facility Type",
        "City",
        "County",
        "Plant Reference #",
    ]
    out: list[str] = []
    for k in fields_to_report:
        a = normalize_whitespace(prev.get(k, ""))
        b = normalize_whitespace(cur.get(k, ""))
        if a != b:
            if not a:
                out.append(f'{k}: (blank) -> "{b}"')
            elif not b:
                out.append(f'{k}: "{a}" -> (blank)')
            else:
                out.append(f'{k}: "{a}" -> "{b}"')
    return out


def detect_new_links(prev: list[dict[str, str]], cur: list[dict[str, str]]) -> list[dict[str, str]]:
    prev_set = {(d.get("url", ""), d.get("text", "")) for d in prev}
    out: list[dict[str, str]] = []
    for d in cur:
        key = (d.get("url", ""), d.get("text", ""))
        if key not in prev_set:
            out.append(d)
    return out


def normalize_link_url(url: str) -> str:
    try:
        p = urllib.parse.urlparse(url)
    except Exception:
        return url

    query_pairs = urllib.parse.parse_qsl(p.query, keep_blank_values=True)
    # BAAQMD URLs commonly include sc_lang=en; treat it as cosmetic.
    query_pairs = [(k, v) for (k, v) in query_pairs if k.lower() != "sc_lang"]
    query_pairs.sort(key=lambda kv: (kv[0].lower(), kv[1]))
    query = urllib.parse.urlencode(query_pairs, doseq=True)

    scheme = (p.scheme or "").lower()
    netloc = (p.netloc or "").lower()
    path = p.path or ""
    return urllib.parse.urlunparse((scheme, netloc, path, "", query, ""))


def diff_links(
    prev_links: list[dict[str, str]],
    cur_links: list[dict[str, str]],
) -> tuple[list[dict[str, str]], list[dict[str, str]], list[dict[str, str]]]:
    """
    Returns (added, removed, updated) where updated contains dicts with keys:
    text, from_url, to_url.

    We try to pair "removed" + "added" links that likely represent the same
    document but with a changed querystring (e.g., sc_lang).
    """
    prev_norm = [
        {
            "text": normalize_whitespace(d.get("text", "")),
            "url": d.get("url", ""),
            "url_norm": normalize_link_url(d.get("url", "")),
        }
        for d in prev_links
    ]
    cur_norm = [
        {
            "text": normalize_whitespace(d.get("text", "")),
            "url": d.get("url", ""),
            "url_norm": normalize_link_url(d.get("url", "")),
        }
        for d in cur_links
    ]

    prev_set = {(d["url_norm"], d["text"]) for d in prev_norm}
    cur_set = {(d["url_norm"], d["text"]) for d in cur_norm}

    added = [d for d in cur_norm if (d["url_norm"], d["text"]) not in prev_set]
    removed = [d for d in prev_norm if (d["url_norm"], d["text"]) not in cur_set]

    # Pair by (text, path) so we can surface URL updates instead of add/remove.
    removed_by_key: dict[tuple[str, str], list[dict[str, str]]] = {}
    for d in removed:
        p = urllib.parse.urlparse(d["url_norm"])
        removed_by_key.setdefault((d["text"], p.path), []).append(d)

    updated: list[dict[str, str]] = []
    remaining_added: list[dict[str, str]] = []
    for d in added:
        p = urllib.parse.urlparse(d["url_norm"])
        key = (d["text"], p.path)
        bucket = removed_by_key.get(key) or []
        if bucket:
            old = bucket.pop(0)
            updated.append({"text": d["text"] or "(no text)", "from_url": old["url"], "to_url": d["url"]})
            if not bucket:
                removed_by_key.pop(key, None)
        else:
            remaining_added.append(d)

    remaining_removed: list[dict[str, str]] = []
    for bucket in removed_by_key.values():
        remaining_removed.extend(bucket)

    # Return raw-ish dicts for added/removed for nicer printing.
    return (
        [{"text": d["text"], "url": d["url"]} for d in remaining_added],
        [{"text": d["text"], "url": d["url"]} for d in remaining_removed],
        updated,
    )


def detect_removed_links(prev: list[dict[str, str]], cur: list[dict[str, str]]) -> list[dict[str, str]]:
    cur_set = {(d.get("url", ""), d.get("text", "")) for d in cur}
    out: list[dict[str, str]] = []
    for d in prev:
        key = (d.get("url", ""), d.get("text", ""))
        if key not in cur_set:
            out.append(d)
    return out


def links_signature(links: list[dict[str, str]]) -> str:
    parts: list[str] = []
    for l in links:
        parts.append(f"{normalize_link_url(l.get('url',''))}|{normalize_whitespace(l.get('text',''))}")
    parts.sort()
    return sha256_text("\n".join(parts))


def build_digest(
    *,
    run_at_utc: str,
    previous_run_at_utc: Optional[str],
    csv_new_all: list[dict[str, str]],
    csv_new_interest: list[dict[str, str]],
    csv_changed_all: list[dict[str, Any]],
    csv_changed_interest: list[dict[str, Any]],
    csv_removed_all: list[dict[str, str]],
    csv_removed_interest: list[dict[str, str]],
    csv_note: str = "",
    permit_eval_summary: dict[str, Any],
    page_changes: list[dict[str, Any]],
) -> str:
    lines: list[str] = []
    lines.append(f"# BAAQMD Monitor Digest")
    lines.append("")
    lines.append(f"- Run (UTC): {run_at_utc}")
    if previous_run_at_utc:
        lines.append(f"- Previous run (UTC): {previous_run_at_utc}")
    lines.append("")

    lines.append("## Permit applications (Recent Permit Applications CSV)")
    if not csv_new_all and not csv_changed_all and not csv_removed_all:
        lines.append("- No new/updated/removed rows detected since last run.")
        if csv_note:
            lines.append(f"- Note: {csv_note}")
    else:
        if csv_new_all:
            lines.append(f"- New rows detected: {len(csv_new_all)} (of interest: {len(csv_new_interest)})")
        else:
            lines.append("- New rows detected: 0")
        if csv_changed_all:
            lines.append(f"- Updated rows detected: {len(csv_changed_all)} (of interest: {len(csv_changed_interest)})")
        else:
            lines.append("- Updated rows detected: 0")
        if csv_removed_all:
            lines.append(f"- Removed rows detected: {len(csv_removed_all)} (of interest: {len(csv_removed_interest)})")
        else:
            lines.append("- Removed rows detected: 0")
        if csv_note:
            lines.append(f"- Note: {csv_note}")
        lines.append("")

        if csv_new_interest:
            lines.append("### New rows of interest")
            for row in csv_new_interest[:25]:
                lines.append(f"- {format_permit_row(row)}")
            if len(csv_new_interest) > 25:
                lines.append(f"- ...and {len(csv_new_interest) - 25} more")
            lines.append("")

        if csv_changed_interest:
            lines.append("### Updated rows of interest")
            for item in csv_changed_interest[:25]:
                row = item.get("row") or {}
                changes = item.get("changes") or []
                lines.append(f"- {format_permit_row(row)}")
                for c in changes[:8]:
                    lines.append(f"  - {c}")
                if len(changes) > 8:
                    lines.append(f"  - ...and {len(changes) - 8} more")
            if len(csv_changed_interest) > 25:
                lines.append(f"- ...and {len(csv_changed_interest) - 25} more")
            lines.append("")

        if csv_new_all:
            lines.append("### Other new rows (filtered)")
            for row in csv_new_all[:25]:
                if row in csv_new_interest:
                    continue
                lines.append(f"- {format_permit_row(row)}")
            if len(csv_new_all) > 25:
                lines.append(f"- ...and {len(csv_new_all) - 25} more")
            lines.append("")

        if csv_changed_all:
            lines.append("### Other updated rows (filtered)")
            interest_ids = {it.get("id") for it in csv_changed_interest if it.get("id")}
            shown = 0
            for item in csv_changed_all:
                if item.get("id") in interest_ids:
                    continue
                row = item.get("row") or {}
                changes = item.get("changes") or []
                lines.append(f"- {format_permit_row(row)}")
                for c in changes[:4]:
                    lines.append(f"  - {c}")
                if len(changes) > 4:
                    lines.append(f"  - ...and {len(changes) - 4} more")
                shown += 1
                if shown >= 15:
                    break
            if len(csv_changed_all) > shown:
                lines.append(f"- ...and {len(csv_changed_all) - shown} more")
            lines.append("")
    lines.append("")

    lines.append("## Permit evaluations (Public Notices table)")
    pe_note = permit_eval_summary.get("note") or ""
    pe_year = int(permit_eval_summary.get("year") or 0)
    if pe_note:
        lines.append(f"- Note: {pe_note}")
    lines.append(f"- Year: {pe_year}" if pe_year else "- Year: (unknown)")
    lines.append(f"- Rows checked: {permit_eval_summary.get('rows_checked', 0)}")
    lines.append(f"- Permit evaluation docs found: {permit_eval_summary.get('docs_found', 0)}")
    lines.append(f"- New/updated texts saved: {permit_eval_summary.get('docs_saved', 0)}")
    saved = permit_eval_summary.get("saved") or []
    if saved:
        lines.append("")
        lines.append("### New/updated permit evaluation docs")
        for item in saved[:25]:
            lines.append(f"- {item.get('label')} - {item.get('url')}")
        if len(saved) > 25:
            lines.append(f"- ...and {len(saved) - 25} more")
    lines.append("")

    lines.append("## Watched pages (status)")
    if not page_changes:
        lines.append("- (No pages configured.)")
    else:
        for c in sorted(page_changes, key=lambda d: (d.get("title") or "", d.get("url") or "")):
            title = c.get("title") or "(no title)"
            url = c.get("url")
            status = int(c.get("http_status") or 0)
            reason = c.get("reason") or ""
            ctype = c.get("content_type") or ""
            if status and status >= 400:
                suffix = f" ({ctype})" if ctype else ""
                lines.append(f"- ERROR {status}: {title}{suffix} - {url}")
                continue
            if c.get("changed"):
                suffix = f" ({ctype})" if ctype else ""
                reason_txt = f" ({reason})" if reason else ""
                lines.append(f"- CHANGED{reason_txt}: {title}{suffix} - {url}")
            else:
                suffix = f" ({ctype})" if ctype else ""
                lines.append(f"- OK: {title}{suffix} - {url}")
    lines.append("")

    lines.append("## Watched pages (changes)")
    changed = [c for c in page_changes if c.get("changed") and int(c.get("http_status") or 0) < 400]
    if not page_changes:
        lines.append("- (No pages configured.)")
    elif not changed:
        lines.append("- No changes detected across watched pages.")
    else:
        for c in changed:
            title = c.get("title") or "(no title)"
            url = c.get("url")
            reason = c.get("reason") or ""
            lines.append(f"### {title}")
            lines.append(f"- URL: {url}")
            if reason:
                lines.append(f"- Detected: {reason}")
            details = c.get("details") or []
            if details:
                lines.append("- Details:")
                for d in details[:10]:
                    lines.append(f"  - {d}")
                if len(details) > 10:
                    lines.append(f"  - ...and {len(details) - 10} more")
            new_links = c.get("new_links", [])
            if new_links:
                lines.append(f"- New relevant links: {len(new_links)}")
                for link in new_links[:15]:
                    txt = link.get("text") or "(no text)"
                    lines.append(f"  - {txt} - {link.get('url')}")
                if len(new_links) > 15:
                    lines.append(f"  - ...and {len(new_links) - 15} more")
            updated_links = c.get("updated_links", [])
            if updated_links:
                lines.append(f"- Updated relevant links: {len(updated_links)}")
                for u in updated_links[:10]:
                    txt = u.get("text") or "(no text)"
                    lines.append(f"  - {txt} - {u.get('from_url')} -> {u.get('to_url')}")
                if len(updated_links) > 10:
                    lines.append(f"  - ...and {len(updated_links) - 10} more")
            removed_count = int(c.get("removed_links_count") or 0)
            if removed_count:
                lines.append(f"- Removed relevant links: {removed_count}")
            else:
                if not details and not reason:
                    lines.append("- Content changed (no new relevant links detected).")
            lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def extract_tableblock_params_all(html_text: str) -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    for m in RE_TABLEBLOCK.finditer(html_text):
        out.append(
            {
                "page_id": m.group("page_id"),
                "data_source": m.group("data_source"),
                "render_hash": m.group("render_hash"),
            }
        )
    return out


def b64_encode_text(s: str) -> str:
    import base64

    return base64.b64encode(s.encode("utf-8")).decode("ascii")


def fetch_public_notices_table_rows(
    public_notices_url: str, *, year: int
) -> tuple[Optional[dict[str, str]], list[dict[str, Any]]]:
    """
    Public Notices page contains a dynamic TableBlock (Plant/Application/Documents/Description).
    We scrape the TableBlock params from the HTML and then call the table JSON endpoint.
    """
    result = fetch_url(public_notices_url, method="GET")
    if result.status >= 400:
        return None, []

    text = result.body.decode("utf-8", errors="replace")
    candidates = extract_tableblock_params_all(text)
    if not candidates:
        return None, []

    # Respect language prefix if present (e.g. /en)
    parsed = urllib.parse.urlparse(public_notices_url)
    lang_prefix = "/en" if parsed.path.startswith("/en/") else ""

    for params in candidates:
        b64 = b64_encode_text(params["data_source"])
        api_url = f"https://{parsed.netloc}{lang_prefix}/api/admin/table/data/{params['page_id']}/{b64}/{params['render_hash']}"
        api = fetch_url(api_url, method="GET")
        if api.status >= 400:
            continue
        try:
            payload = json.loads(api.body.decode("utf-8", errors="replace"))
        except Exception:
            continue
        rows = payload.get("Data") or []
        if not isinstance(rows, list):
            continue
        year_rows = [r for r in rows if str(r.get("Date") or "").startswith(f"{year}-")]
        if year_rows:
            return params, year_rows

    return candidates[0], []


def extract_href_from_html_anchor(html_snippet: str, base_url: str) -> str:
    m = re.search(r'href\s*=\s*"([^"]+)"', html_snippet, re.I)
    if not m:
        return ""
    href = html.unescape(m.group(1))
    return urllib.parse.urljoin(base_url, href)


def extract_anchor_text_from_html_anchor(html_snippet: str) -> str:
    m = re.search(r">([^<]+)</a>", html_snippet, re.I)
    return normalize_whitespace(m.group(1)) if m else ""


def fetch_table_rows_for_page(page_url: str) -> list[dict[str, Any]]:
    """
    For pages that render TableBlock tables, fetch all table datasets.
    Returns a flattened list of rows across all tables on the page.
    """
    result = fetch_url(page_url, method="GET")
    if result.status >= 400:
        return []

    html_text = result.body.decode("utf-8", errors="replace")
    candidates = extract_tableblock_params_all(html_text)
    if not candidates:
        return []

    parsed = urllib.parse.urlparse(page_url)
    lang_prefix = "/en" if parsed.path.startswith("/en/") else ""

    all_rows: list[dict[str, Any]] = []
    for params in candidates:
        b64 = b64_encode_text(params["data_source"])
        api_url = f"https://{parsed.netloc}{lang_prefix}/api/admin/table/data/{params['page_id']}/{b64}/{params['render_hash']}"
        api = fetch_url(api_url, method="GET")
        if api.status >= 400:
            continue
        try:
            payload = json.loads(api.body.decode("utf-8", errors="replace"))
        except Exception:
            continue
        rows = payload.get("Data") or []
        if isinstance(rows, list):
            all_rows.extend(rows)
    return all_rows


def extract_text_from_pdf_bytes(pdf_bytes: bytes) -> str:
    try:
        from pypdf import PdfReader
    except Exception:
        return ""
    try:
        reader = PdfReader(io.BytesIO(pdf_bytes))
        parts: list[str] = []
        for page in reader.pages:
            try:
                t = page.extract_text() or ""
            except Exception:
                t = ""
            if t:
                parts.append(t)
        return "\n\n".join(parts).strip()
    except Exception:
        return ""


def run_rag_index(context_folder: str, rag_cli_path: str) -> bool:
    if not os.path.exists(rag_cli_path):
        return False
    try:
        proc = subprocess.run(
            [sys.executable, rag_cli_path, "index", "--context-folder", context_folder],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        # Keep logs small but still helpful when run via .bat logging.
        if proc.stdout:
            sys.stdout.write(proc.stdout[-4000:])
        return proc.returncode == 0
    except Exception:
        return False


def render_digest_html(markdown_text: str, *, generated_at_utc: str) -> str:
    def linkify(text: str) -> str:
        parts: list[str] = []
        last = 0
        for m in RE_URL.finditer(text):
            parts.append(html.escape(text[last : m.start()]))
            url = m.group(0)
            href = html.escape(url, quote=True)
            label = html.escape(url)
            parts.append(f'<a href="{href}">{label}</a>')
            last = m.end()
        parts.append(html.escape(text[last:]))
        return "".join(parts)

    lines = markdown_text.splitlines()
    body_parts: list[str] = []
    list_stack: list[int] = []

    def close_lists(to_indent: int = 0) -> None:
        nonlocal list_stack
        while list_stack and list_stack[-1] >= to_indent:
            body_parts.append("</ul>")
            list_stack.pop()

    for raw in lines:
        line = raw.rstrip("\n")
        if not line.strip():
            continue

        if line.startswith("# "):
            close_lists(0)
            body_parts.append(f"<h1>{linkify(line[2:].strip())}</h1>")
            continue
        if line.startswith("## "):
            close_lists(0)
            body_parts.append(f"<h2>{linkify(line[3:].strip())}</h2>")
            continue
        if line.startswith("### "):
            close_lists(0)
            body_parts.append(f"<h3>{linkify(line[4:].strip())}</h3>")
            continue

        m = re.match(r"^(?P<indent>\s*)-\s+(?P<text>.*)$", line)
        if m:
            indent = len(m.group("indent").replace("\t", "  "))
            level = 0 if indent < 2 else 2
            if not list_stack or list_stack[-1] < level:
                body_parts.append("<ul>")
                list_stack.append(level)
            elif list_stack[-1] > level:
                close_lists(level)
                if not list_stack or list_stack[-1] < level:
                    body_parts.append("<ul>")
                    list_stack.append(level)
            body_parts.append(f"<li>{linkify(m.group('text').strip())}</li>")
            continue

        close_lists(0)
        body_parts.append(f"<p>{linkify(line)}</p>")

    close_lists(0)

    css = """
    :root {
      color-scheme: light dark;
      --ink: #1b2b34;
      --muted: #52616b;
      --barr-blue: #0072bc;
      --barr-blue-dark: #005a9c;
      --barr-blue-light: #a9d4f2;
      --pine: #0f4c5c;
      --sage: #1f6f8b;
      --sand: #eef2f3;
      --bg: #f4f7f9;
      --card: #ffffff;
      --line: #dfe6ea;
      --shadow: rgba(14,35,46,0.08);
    }

    @media (prefers-color-scheme: dark) {
      :root {
        --ink: #e6edf3;
        --muted: #9fb0bb;
        --bg: #0b141a;
        --sand: #0f1c24;
        --card: #0f1c24;
        --line: rgba(230,237,243,0.12);
        --shadow: rgba(0,0,0,0.35);
      }
    }

    body {
      font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
      margin: 24px;
      line-height: 1.4;
      color: var(--ink);
      background:
        radial-gradient(circle at 15% -10%, #ffffff 0%, var(--sand) 40%, var(--bg) 75%),
        var(--bg);
    }

    a { color: var(--barr-blue); word-break: break-word; text-decoration: none; }
    a:hover { text-decoration: underline; }

    h1 { font-size: 1.55rem; margin: 0 0 12px; color: var(--pine); }
    h2 {
      font-size: 1.15rem;
      margin: 18px 0 10px;
      padding: 8px 10px;
      border: 1px solid var(--line);
      border-radius: 10px;
      background: linear-gradient(90deg, var(--barr-blue-light), rgba(255,255,255,0));
      color: var(--ink);
    }
    h3 { font-size: 1.0rem; margin: 14px 0 6px; color: var(--sage); }

    ul { margin: 6px 0 6px 22px; padding: 0; }
    li { margin: 2px 0; }

    .meta { color: var(--muted); font-size: 0.9rem; margin-bottom: 12px; }
    .card {
      background: var(--card);
      border: 1px solid var(--line);
      border-radius: 14px;
      padding: 16px 18px;
      box-shadow: 0 10px 24px var(--shadow);
      max-width: 1100px;
    }
    """

    body_html = "\n".join(body_parts).strip()
    return (
        "<!doctype html>\n"
        "<html lang=\"en\">\n"
        "<head>\n"
        "  <meta charset=\"utf-8\">\n"
        "  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
        "  <title>BAAQMD Monitor Digest</title>\n"
        f"  <style>{css}</style>\n"
        "</head>\n"
        "<body>\n"
        "  <div class=\"card\">\n"
        f"    <div class=\"meta\">Generated (UTC): {html.escape(generated_at_utc)}</div>\n"
        f"{body_html}\n"
        "  </div>\n"
        "</body>\n"
        "</html>\n"
    )


def main() -> int:
    ap = argparse.ArgumentParser(description="Monitor BAAQMD sources and generate a change digest.")
    ap.add_argument("--agents-md", default="AGENTS.md", help="Path to AGENTS.md (default: AGENTS.md)")
    ap.add_argument(
        "--state",
        default=os.path.join("data", "monitor", "baaqmd_state.json"),
        help="State JSON path (default: data/monitor/baaqmd_state.json)",
    )
    ap.add_argument(
        "--out",
        default=os.path.join("outputs", "baaqmd_digest.md"),
        help="Digest output path (default: outputs/baaqmd_digest.md)",
    )
    ap.add_argument(
        "--out-html",
        default=os.path.join("outputs", "baaqmd_digest.html"),
        help="HTML digest output path (default: outputs/baaqmd_digest.html)",
    )
    ap.add_argument(
        "--csv-url",
        default="https://www.baaqmd.gov/admin/tableutils/CsvExportUnfiltered?pageId=ed399e3e-0cb0-4e12-9dc3-69e5f2c79253&dataSourceId=e0REQjIyODIxLTlGN0EtNDc0MC1BNTQ2LUE2Q0NDNTgxQTMxQ30=&renderingParamsHash=1318110647",
        help="Permit applications CSV export URL",
    )
    ap.add_argument(
        "--permit-evals-year",
        type=int,
        default=datetime.now(timezone.utc).year,
        help="Year to pull permit evaluation docs for (default: current year)",
    )
    ap.add_argument(
        "--permit-evals-folder",
        default=os.path.join("data", "permit_evaluations"),
        help="Folder to store permit evaluation docs/texts (default: data/permit_evaluations)",
    )
    ap.add_argument(
        "--rag-cli",
        default=r"C:\Users\aaw\.codex\skills\agentic-rag-indexer\scripts\rag_cli.py",
        help="Path to agentic-rag-indexer rag_cli.py",
    )
    ap.add_argument(
        "--no-index-permit-evals",
        action="store_true",
        help="Do not run agentic-rag-indexer after fetching permit evaluations",
    )
    args = ap.parse_args()

    run_at = utc_now_iso()
    prev_state: dict[str, Any] = {}
    if os.path.exists(args.state):
        try:
            prev_state = read_json(args.state)
        except Exception:
            prev_state = {}

    previous_run_at = prev_state.get("run_at_utc")
    prev_csv_state = (prev_state.get("sources") or {}).get("permit_applications_csv") or {}
    prev_csv_schema = int(prev_csv_state.get("schema_version") or 0)
    prev_csv_rows_by_id: dict[str, Any] = prev_csv_state.get("rows_by_id") or {}
    prev_csv_ids = set(prev_csv_rows_by_id.keys()) if prev_csv_rows_by_id else set(prev_csv_state.get("row_ids") or [])
    csv_note = ""
    prev_permit_evals_state: dict[str, Any] = (prev_state.get("sources") or {}).get("permit_evaluations") or {}
    prev_eval_docs: dict[str, Any] = prev_permit_evals_state.get("docs") or {}

    interest_keywords = [
        "valero",
        "benicia",
        "chevron",
        "richmond",
        "phillips 66",
        "rodeo",
        "marathon",
        "martinez",
        "pbf",
        "martinez refining",
        "transmontaigne",
        "hydrogen",
        "sulfur",
        "chemtrade",
        "refinery",
        "terminal",
    ]

    # 1) Permit applications CSV (special handling)
    csv_fetch = fetch_url(args.csv_url)
    if csv_fetch.status >= 400:
        raise SystemExit(f"Failed to fetch CSV ({csv_fetch.status}): {args.csv_url}")
    csv_rows = parse_permit_applications_csv(csv_fetch.body)

    csv_rows_by_id: dict[str, dict[str, Any]] = {}
    csv_row_ids: list[str] = []
    csv_row_by_id_for_output: dict[str, dict[str, str]] = {}
    for r in csv_rows:
        rid = permit_row_stable_id(r)
        csv_row_ids.append(rid)
        csv_row_by_id_for_output[rid] = r
        csv_rows_by_id[rid] = {
            "sig": permit_row_fingerprint(r),
            "fields": {k: r.get(k, "") for k in r.keys()},
        }

    csv_row_id_set = set(csv_row_ids)
    new_ids = sorted(csv_row_id_set - prev_csv_ids)
    removed_ids = sorted(prev_csv_ids - csv_row_id_set)
    common_ids = sorted(csv_row_id_set & prev_csv_ids)

    # If we're upgrading from an older state schema, avoid a one-time flood of "new rows".
    # We'll treat this run as the new baseline and start reporting diffs on the next run.
    if prev_csv_schema < 2 or not prev_csv_rows_by_id:
        csv_note = "Permit CSV tracking upgraded; this run is treated as a baseline (row-level diffs start next run)."
        new_ids = []
        removed_ids = []
        common_ids = []

    changed_ids: list[str] = []
    for rid in common_ids:
        prev_sig = (prev_csv_rows_by_id.get(rid) or {}).get("sig") or ""
        cur_sig = (csv_rows_by_id.get(rid) or {}).get("sig") or ""
        if prev_sig and cur_sig and prev_sig != cur_sig:
            changed_ids.append(rid)

    csv_new_rows = [csv_row_by_id_for_output[rid] for rid in new_ids if rid in csv_row_by_id_for_output]
    csv_new_rows_filtered = [
        r for r in csv_new_rows if not is_gasoline_dispensing(r) and not is_emergency_generator_only(r)
    ]
    csv_new_interest = [r for r in csv_new_rows_filtered if is_of_interest(r, interest_keywords)]

    csv_changed_items: list[dict[str, Any]] = []
    for rid in changed_ids:
        cur_row = csv_row_by_id_for_output.get(rid) or {}
        prev_fields = (prev_csv_rows_by_id.get(rid) or {}).get("fields") or {}
        changes = diff_row_fields(prev_fields, cur_row)
        if changes:
            csv_changed_items.append({"id": rid, "row": cur_row, "changes": changes})

    csv_changed_rows_filtered = [
        it
        for it in csv_changed_items
        if not is_gasoline_dispensing(it.get("row") or {}) and not is_emergency_generator_only(it.get("row") or {})
    ]
    csv_changed_interest = [it for it in csv_changed_rows_filtered if is_of_interest(it.get("row") or {}, interest_keywords)]

    csv_removed_rows: list[dict[str, str]] = []
    for rid in removed_ids:
        prev_fields = (prev_csv_rows_by_id.get(rid) or {}).get("fields") or {}
        if prev_fields:
            csv_removed_rows.append({k: str(v) for k, v in prev_fields.items()})
    csv_removed_rows_filtered = [
        r for r in csv_removed_rows if not is_gasoline_dispensing(r) and not is_emergency_generator_only(r)
    ]
    csv_removed_interest = [r for r in csv_removed_rows_filtered if is_of_interest(r, interest_keywords)]

    # 2) Permit evaluation docs (Public Notices table -> Documents -> Permit Evaluation)
    permit_eval_summary: dict[str, Any] = {"rows_checked": 0, "docs_found": 0, "docs_saved": 0, "saved": [], "note": ""}
    permit_eval_docs_state: dict[str, Any] = dict(prev_eval_docs)

    public_notices_url = "https://www.baaqmd.gov/en/permits/public-notices"
    params, pn_rows = fetch_public_notices_table_rows(public_notices_url, year=int(args.permit_evals_year))
    if not params:
        permit_eval_summary["note"] = "Could not locate Public Notices table parameters; skipping permit evaluation pull."
    elif not pn_rows:
        permit_eval_summary["note"] = "Public Notices table returned no rows; skipping permit evaluation pull."
    else:
        year = int(args.permit_evals_year)
        permit_eval_summary["year"] = year
        year_folder = os.path.join(args.permit_evals_folder, str(year))
        os.makedirs(year_folder, exist_ok=True)

        for row in pn_rows:
            date_raw = str(row.get("Date") or "")
            if not date_raw.startswith(f"{year}-"):
                continue

            docs_html = str(row.get("Documents") or "")
            docs_page = extract_href_from_html_anchor(docs_html, "https://www.baaqmd.gov/en/permits/public-notices")
            if not docs_page:
                continue

            permit_eval_summary["rows_checked"] += 1
            doc_page_fetch = fetch_url(docs_page, method="GET")
            if doc_page_fetch.status >= 400:
                continue

            doc_page_text = doc_page_fetch.body.decode("utf-8", errors="replace")
            permit_eval_links: list[dict[str, str]] = []

            # Documents pages typically render a documents table via TableBlock.
            # Pull the table rows and extract "Permit Evaluation" file(s).
            doc_rows = fetch_table_rows_for_page(docs_page)
            for r in doc_rows:
                doc_html = str(r.get("DocumentFile") or r.get("Document") or "")
                if not doc_html:
                    continue
                label = extract_anchor_text_from_html_anchor(doc_html)
                href = extract_href_from_html_anchor(doc_html, docs_page)
                if not href:
                    continue
                hay = (label + " " + href).lower()
                if "permit evaluation" in hay or "_eval_" in hay or hay.endswith("_eval.pdf"):
                    permit_eval_links.append({"text": label or "Permit Evaluation", "url": href})

            if not permit_eval_links:
                # Fallback: some pages may include direct anchors (rare)
                anchor_extractor = AnchorExtractor(page_url=doc_page_fetch.final_url)
                try:
                    anchor_extractor.feed(doc_page_text)
                except Exception:
                    anchor_extractor = AnchorExtractor(page_url=doc_page_fetch.final_url)
                permit_eval_links = [
                    a
                    for a in anchor_extractor.anchors
                    if "permit evaluation" in (a.get("text") or "").lower() and a.get("url")
                ]
                if not permit_eval_links:
                    continue

            plant = sanitize_filename(str(row.get("PlantName") or "") or "plant")
            app_no = sanitize_filename(str(row.get("ApplicationNumber") or "") or "application")
            for a in permit_eval_links:
                permit_eval_summary["docs_found"] += 1
                eval_url = a["url"]
                pdf = fetch_url(eval_url, method="GET")
                if pdf.status >= 400 or not pdf.body:
                    continue

                pdf_sha = sha256_bytes(pdf.body)
                prev = permit_eval_docs_state.get(eval_url) or {}
                if prev.get("sha256") == pdf_sha:
                    continue

                base = sanitize_filename(os.path.basename(urllib.parse.urlparse(eval_url).path) or "permit_evaluation.pdf")
                stem = sanitize_filename(f"{year}-{app_no}-{plant}")
                pdf_path = os.path.join(year_folder, f"{stem}__{base}")
                txt_path = os.path.join(year_folder, f"{stem}__{os.path.splitext(base)[0]}.txt")

                write_text(
                    txt_path,
                    "\n".join(
                        [
                            f"Title: {a.get('text') or 'Permit evaluation'}",
                            f"PlantName: {row.get('PlantName') or ''}",
                            f"PlantNumber: {row.get('PlantNumber') or ''}",
                            f"ApplicationNumber: {row.get('ApplicationNumber') or ''}",
                            f"PublicNoticeDate: {row.get('Date') or ''}",
                            f"DocumentsPage: {docs_page}",
                            f"PermitEvaluationURL: {eval_url}",
                            f"FetchedAtUTC: {run_at}",
                            "",
                            extract_text_from_pdf_bytes(pdf.body),
                            "",
                        ]
                    ).rstrip()
                    + "\n",
                )
                # Save PDF as well for reference.
                os.makedirs(os.path.dirname(pdf_path), exist_ok=True)
                with open(pdf_path, "wb") as f:
                    f.write(pdf.body)

                permit_eval_docs_state[eval_url] = {"sha256": pdf_sha, "fetched_at_utc": run_at, "txt_path": txt_path}
                permit_eval_summary["docs_saved"] += 1
                permit_eval_summary["saved"].append({"url": eval_url, "label": f"{row.get('ApplicationNumber')} - {row.get('PlantName')}"})

                time.sleep(0.2)

        if not args.no_index_permit_evals:
            ok = run_rag_index(args.permit_evals_folder, args.rag_cli)
            if not ok:
                permit_eval_summary["note"] = (
                    permit_eval_summary.get("note") or ""
                ) + " RAG index update failed (rag_cli.py not found or non-zero exit)."

    # 3) Other watched pages from AGENTS.md
    urls = extract_urls_from_agents_md(args.agents_md)
    other_urls = [u for u in urls if u != args.csv_url]

    prev_pages_state: dict[str, Any] = (prev_state.get("sources") or {}).get("pages") or {}
    pages_state: dict[str, Any] = {}
    page_changes: list[dict[str, Any]] = []

    for url in other_urls:
        prev = prev_pages_state.get(url) or {}
        # Prefer HEAD for PDFs to avoid downloads unless needed.
        method = "HEAD" if is_probably_pdf_url(url) else "GET"
        result = fetch_url(url, method=method)
        family = content_type_family(result.content_type)

        snapshot: dict[str, Any] = {
            "url": url,
            "final_url": result.final_url,
            "fetched_at_utc": run_at,
            "status": result.status,
            "content_type": result.content_type,
            "etag": result.headers.get("etag", ""),
            "last_modified": result.headers.get("last-modified", ""),
            "content_length": result.headers.get("content-length", ""),
        }

        changed = False
        title = prev.get("title") or ""
        new_links: list[dict[str, str]] = []
        updated_links: list[dict[str, str]] = []
        removed_links_count = 0
        reason = ""
        details: list[str] = []

        if family == "pdf":
            # PDFs: compare headers first.
            prev_etag = prev.get("etag", "")
            prev_lm = prev.get("last_modified", "")
            prev_len = prev.get("content_length", "")
            cur_etag = snapshot["etag"]
            cur_lm = snapshot["last_modified"]
            cur_len = snapshot["content_length"]
            prev_sig = (prev_etag, prev_lm, prev_len)
            cur_sig = (cur_etag, cur_lm, cur_len)
            changed = cur_sig != prev_sig and any(cur_sig)
            snapshot["title"] = prev.get("title") or "(PDF)"
            snapshot["sig"] = sha256_text("|".join(cur_sig))
            if changed:
                reason = "pdf headers changed"
                if prev_etag != cur_etag and (prev_etag or cur_etag):
                    details.append(f'ETag: "{prev_etag}" -> "{cur_etag}"')
                if prev_lm != cur_lm and (prev_lm or cur_lm):
                    details.append(f'Last-Modified: "{prev_lm}" -> "{cur_lm}"')
                if prev_len != cur_len and (prev_len or cur_len):
                    details.append(f'Content-Length: "{prev_len}" -> "{cur_len}"')
        else:
            if result.status >= 400:
                snapshot["title"] = prev.get("title") or ""
                snapshot["text_sig"] = prev.get("text_sig") or ""
                snapshot["links_sig"] = prev.get("links_sig") or ""
                changed = (prev.get("status") or 0) != snapshot["status"]
                if changed:
                    reason = "http status changed"
                    details.append(f"HTTP status: {prev.get('status')} -> {snapshot.get('status')}")
            else:
                body = result.body
                # Some servers return HTML with an encoding; decode loosely.
                text = body.decode("utf-8", errors="replace")
                extractor = MinimalHTMLExtractor(page_url=result.final_url)
                try:
                    extractor.feed(text)
                except Exception:
                    extractor = MinimalHTMLExtractor(page_url=result.final_url)
                title = extractor.title or prev.get("title") or ""
                visible_text = extractor.visible_text
                text_sig = sha256_text(visible_text)
                cur_links_sig = links_signature(extractor.links)
                snapshot["title"] = title
                snapshot["text_sig"] = text_sig
                snapshot["links_sig"] = cur_links_sig
                snapshot["links"] = extractor.links
                snapshot["visible_text_len"] = len(visible_text)
                snapshot["relevant_links_count"] = len(extractor.links)

                prev_links_sig = prev.get("links_sig") or ""
                prev_text_sig = prev.get("text_sig") or ""

                if extractor.links:
                    changed = cur_links_sig != prev_links_sig
                    if changed:
                        reason = "relevant links changed"
                else:
                    changed = text_sig != prev_text_sig
                    if changed:
                        reason = "page text fingerprint changed"

                if changed:
                    prev_links = prev.get("links") or []
                    added_links, removed_links, updated_links = diff_links(prev_links, extractor.links)
                    new_links = added_links
                    removed_links_count = len(removed_links)
                    prev_title = prev.get("title") or ""
                    if prev_title and prev_title != title:
                        details.append(f'Title: "{prev_title}" -> "{title}"')
                    prev_count = int(prev.get("relevant_links_count") or len(prev_links) or 0)
                    cur_count = int(snapshot["relevant_links_count"] or 0)
                    if prev_count != cur_count:
                        details.append(f"Relevant links: {prev_count} -> {cur_count}")
                    prev_len = int(prev.get("visible_text_len") or 0)
                    cur_len = int(snapshot.get("visible_text_len") or 0)
                    if prev_len and cur_len and prev_len != cur_len:
                        details.append(f"Visible text length: {prev_len} -> {cur_len}")

                    if updated_links:
                        details.append(f"Updated relevant links: {len(updated_links)}")
                    if new_links:
                        details.append(f"New relevant links: {len(new_links)}")
                    if removed_links_count:
                        details.append(f"Removed relevant links: {removed_links_count}")

                    # Suppress "changes" that are almost certainly cosmetic.
                    if reason == "page text fingerprint changed" and prev_len and cur_len and abs(cur_len - prev_len) <= 1:
                        changed = False
                        reason = ""
                        details = []
                        new_links = []
                        removed_links_count = 0
                        updated_links = []

        pages_state[url] = snapshot
        page_changes.append(
            {
                "url": url,
                "title": snapshot.get("title") or title,
                "http_status": snapshot.get("status"),
                "content_type": snapshot.get("content_type"),
                "changed": changed,
                "new_links": new_links,
                "updated_links": updated_links,
                "removed_links_count": removed_links_count,
                "reason": reason,
                "details": details,
            }
        )

        # Be polite to origin servers.
        time.sleep(0.3)

    # 4) Write state + digest
    new_state = {
        "run_at_utc": run_at,
        "sources": {
            "permit_applications_csv": {
                "schema_version": 2,
                "url": args.csv_url,
                "final_url": csv_fetch.final_url,
                "fetched_at_utc": run_at,
                "status": csv_fetch.status,
                "content_type": csv_fetch.content_type,
                "etag": csv_fetch.headers.get("etag", ""),
                "last_modified": csv_fetch.headers.get("last-modified", ""),
                "content_length": csv_fetch.headers.get("content-length", ""),
                "body_sha256": sha256_bytes(csv_fetch.body),
                "row_count": len(csv_rows),
                "row_ids": csv_row_ids,
                "rows_by_id": csv_rows_by_id,
            },
            "permit_evaluations": {
                "year": int(args.permit_evals_year),
                "docs": permit_eval_docs_state,
            },
            "pages": pages_state,
        },
    }
    write_json(args.state, new_state)

    digest = build_digest(
        run_at_utc=run_at,
        previous_run_at_utc=previous_run_at,
        csv_new_all=csv_new_rows_filtered,
        csv_new_interest=csv_new_interest,
        csv_changed_all=csv_changed_rows_filtered,
        csv_changed_interest=csv_changed_interest,
        csv_removed_all=csv_removed_rows_filtered,
        csv_removed_interest=csv_removed_interest,
        csv_note=csv_note,
        permit_eval_summary=permit_eval_summary,
        page_changes=page_changes,
    )
    write_text(args.out, digest)
    write_text(args.out_html, render_digest_html(digest, generated_at_utc=run_at))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
