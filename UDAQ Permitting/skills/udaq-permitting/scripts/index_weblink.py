#!/usr/bin/env python
"""
Index Utah DEQ's public Laserfiche WebLink folder tree into a CSV/JSONL file.

Designed for repo-local/offline indexing to support faster lookup (e.g., Agency Interest - Permitting).

Example:
  python skills/udaq-permitting/scripts/index_weblink.py --folder-id 385828 --out data/weblink-permitting.csv --depth 6
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
import time
from dataclasses import dataclass
from typing import Iterable
from urllib.parse import urljoin, urlparse, parse_qs

import requests
from lxml import html


BASE = "https://lf-public.deq.utah.gov/WebLink/"


@dataclass(frozen=True)
class Entry:
    kind: str  # "folder" | "document"
    entry_id: int
    title: str
    url: str
    parent_id: int


def _parse_entry_id(url: str) -> int | None:
    try:
        q = parse_qs(urlparse(url).query)
        if "id" not in q:
            return None
        return int(q["id"][0])
    except Exception:
        return None


def _is_weblink_href(href: str) -> bool:
    return (
        "Browse.aspx" in href
        or "DocView.aspx" in href
        or "docview.aspx" in href.lower()
        or "browse.aspx" in href.lower()
    )


def _kind_from_href(href: str) -> str | None:
    lower = href.lower()
    if "browse.aspx" in lower:
        return "folder"
    if "docview.aspx" in lower:
        return "document"
    return None


def _extract_entries(page_url: str, page_html: str, parent_id: int) -> list[Entry]:
    doc = html.fromstring(page_html)
    doc.make_links_absolute(page_url)

    entries: list[Entry] = []
    seen: set[tuple[str, int]] = set()

    for a in doc.xpath("//a[@href]"):
        href = a.get("href") or ""
        if not _is_weblink_href(href):
            continue
        kind = _kind_from_href(href)
        if kind is None:
            continue

        abs_url = urljoin(page_url, href)
        entry_id = _parse_entry_id(abs_url)
        if entry_id is None:
            continue

        title = " ".join((a.text_content() or "").split())
        if not title:
            continue

        key = (kind, entry_id)
        if key in seen:
            continue
        seen.add(key)

        entries.append(
            Entry(
                kind=kind,
                entry_id=entry_id,
                title=title,
                url=abs_url,
                parent_id=parent_id,
            )
        )

    return entries


def _find_next_page_url(page_url: str, page_html: str) -> str | None:
    """
    Best-effort pagination support.
    WebLink list pages sometimes have "Next" navigation; if absent, return None.
    """
    doc = html.fromstring(page_html)
    doc.make_links_absolute(page_url)

    # Common patterns: link text "Next", ">", or an element with title/aria-label "Next".
    candidates = doc.xpath(
        "//a[normalize-space(text())='Next']/@href"
        " | //a[normalize-space(text())='>']/@href"
        " | //a[contains(@title,'Next')]/@href"
        " | //a[contains(@aria-label,'Next')]/@href"
    )
    for href in candidates:
        if not href:
            continue
        abs_url = urljoin(page_url, href)
        if abs_url != page_url:
            return abs_url
    return None


def iter_folder_tree(
    session: requests.Session,
    root_folder_id: int,
    depth: int,
    sleep_s: float,
    max_pages_per_folder: int,
) -> Iterable[Entry]:
    root_url = f"{BASE}Browse.aspx?id={root_folder_id}&dbid=0&repo=Public"

    queue: list[tuple[int, str, int]] = [(root_folder_id, root_url, 0)]
    seen_folders: set[int] = set()

    while queue:
        folder_id, folder_url, level = queue.pop(0)
        if folder_id in seen_folders:
            continue
        seen_folders.add(folder_id)

        page_url = folder_url
        page_count = 0
        while page_url and page_count < max_pages_per_folder:
            page_count += 1
            resp = session.get(page_url, timeout=60)
            resp.raise_for_status()

            entries = _extract_entries(page_url, resp.text, parent_id=folder_id)
            for entry in entries:
                yield entry
                if entry.kind == "folder" and level + 1 < depth:
                    queue.append((entry.entry_id, entry.url, level + 1))

            next_url = _find_next_page_url(page_url, resp.text)
            page_url = next_url

            if sleep_s > 0:
                time.sleep(sleep_s)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder-id", type=int, required=True, help="WebLink folder id (Browse.aspx?id=...)")
    parser.add_argument("--depth", type=int, default=6, help="Max recursion depth for subfolders")
    parser.add_argument("--out", type=str, required=True, help="Output file path (.csv or .jsonl)")
    parser.add_argument("--sleep", type=float, default=0.25, help="Seconds to sleep between requests")
    parser.add_argument("--max-pages-per-folder", type=int, default=50, help="Safety cap for pagination per folder")
    parser.add_argument(
        "--user-agent",
        type=str,
        default="udaq-permitting-indexer/1.0",
        help="Custom User-Agent header",
    )
    args = parser.parse_args(argv)

    out_lower = args.out.lower()
    if not (out_lower.endswith(".csv") or out_lower.endswith(".jsonl")):
        raise SystemExit("--out must end with .csv or .jsonl")

    session = requests.Session()
    session.headers.update({"User-Agent": args.user_agent})

    entries = iter_folder_tree(
        session=session,
        root_folder_id=args.folder_id,
        depth=args.depth,
        sleep_s=args.sleep,
        max_pages_per_folder=args.max_pages_per_folder,
    )

    if out_lower.endswith(".csv"):
        with open(args.out, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(
                f,
                fieldnames=["kind", "id", "title", "url", "parent_id"],
            )
            w.writeheader()
            for e in entries:
                w.writerow(
                    {
                        "kind": e.kind,
                        "id": e.entry_id,
                        "title": e.title,
                        "url": e.url,
                        "parent_id": e.parent_id,
                    }
                )
    else:
        with open(args.out, "w", encoding="utf-8") as f:
            for e in entries:
                f.write(
                    json.dumps(
                        {
                            "kind": e.kind,
                            "id": e.entry_id,
                            "title": e.title,
                            "url": e.url,
                            "parent_id": e.parent_id,
                        },
                        ensure_ascii=False,
                    )
                    + "\n"
                )

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

