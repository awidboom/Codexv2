#!/usr/bin/env python
"""
Download documents from Utah DEQ's public Laserfiche WebLink folder tree.

Target use: download and mirror the "Agency Interest - Permitting" folder locally,
then search/analyze the local corpus for permitting questions.

Example:
  python skills/udaq-permitting/scripts/download_weblink_folder.py ^
    --folder-id 385828 ^
    --out-dir data/weblink/agency-interest-permitting ^
    --depth 8 ^
    --sleep 0.25
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from dataclasses import dataclass
from pathlib import Path
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


def _parse_id(url: str) -> int | None:
    try:
        q = parse_qs(urlparse(url).query)
        if "id" not in q:
            return None
        return int(q["id"][0])
    except Exception:
        return None


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
        kind = _kind_from_href(href)
        if kind is None:
            continue

        abs_url = urljoin(page_url, href)
        entry_id = _parse_id(abs_url)
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
    doc = html.fromstring(page_html)
    doc.make_links_absolute(page_url)
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
            if not entries:
                # WebLink browse pages are often JS-driven; try the server-side prerendered
                # output by using a bot UA (it fills <span id="CrawlerPreRender">).
                #
                # Note: this is a best-effort fallback; if it stops working, you may need
                # a different retrieval approach (API endpoints).
                bot_headers = {
                    "User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; udaq-permitting-downloader/1.0)",
                }
                resp2 = session.get(page_url, timeout=60, headers=bot_headers)
                resp2.raise_for_status()
                entries = _extract_entries(page_url, resp2.text, parent_id=folder_id)

            for entry in entries:
                yield entry
                if entry.kind == "folder" and level + 1 < depth:
                    queue.append((entry.entry_id, entry.url, level + 1))

            page_url = _find_next_page_url(page_url, resp.text)

            if sleep_s > 0:
                time.sleep(sleep_s)


_ILLEGAL_CHARS = re.compile(r'[<>:"/\\\\|?*]+')


def _safe_name(name: str, max_len: int = 120) -> str:
    name = name.strip().strip(".")
    name = _ILLEGAL_CHARS.sub("_", name)
    name = re.sub(r"\s+", " ", name).strip()
    if len(name) > max_len:
        name = name[:max_len].rstrip()
    return name or "untitled"


def _write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _extract_download_url(doc_view_url: str, doc_view_html: str) -> str | None:
    """
    Best-effort extraction: look for a "Download" link or a href that looks like a file download endpoint.
    """
    doc = html.fromstring(doc_view_html)
    doc.make_links_absolute(doc_view_url)

    # 1) Prefer explicit "Download" text links.
    for href in doc.xpath("//a[contains(translate(normalize-space(text()), 'DOWNLOAD', 'download'), 'download')]/@href"):
        if not href:
            continue
        return urljoin(doc_view_url, href)

    # 2) Look for common endpoint substrings.
    substrings = ["docdownload", "download", "getfile", "filedownload", "docread", "binary"]
    for href in doc.xpath("//a[@href]/@href"):
        if not href:
            continue
        lower = href.lower()
        if any(s in lower for s in substrings) and "docview.aspx" not in lower:
            return urljoin(doc_view_url, href)

    return None


def _guess_extension_from_content_type(content_type: str | None) -> str | None:
    if not content_type:
        return None
    ct = content_type.split(";")[0].strip().lower()
    return {
        "application/pdf": ".pdf",
        "text/plain": ".txt",
        "text/html": ".html",
        "application/msword": ".doc",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document": ".docx",
        "application/vnd.ms-excel": ".xls",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": ".xlsx",
        "application/vnd.ms-powerpoint": ".ppt",
        "application/vnd.openxmlformats-officedocument.presentationml.presentation": ".pptx",
        "image/tiff": ".tif",
        "image/tiff-fx": ".tif",
        "image/jpeg": ".jpg",
        "image/png": ".png",
    }.get(ct)


def _stream_download(session: requests.Session, url: str, out_path: Path, timeout_s: int) -> tuple[int, str | None]:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with session.get(url, stream=True, timeout=timeout_s) as r:
        r.raise_for_status()
        content_type = r.headers.get("Content-Type")
        size = 0
        with open(out_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024 * 256):
                if not chunk:
                    continue
                f.write(chunk)
                size += len(chunk)
        return size, content_type


def _electronic_file_url(doc_id: int) -> str:
    # This endpoint is referenced by WebLink's doc viewer JS bundle and typically returns the file bytes.
    return f"{BASE}ElectronicFile.aspx?docid={doc_id}&dbid=0&repo=Public"


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder-id", type=int, required=True, help="WebLink folder id (Browse.aspx?id=...)")
    parser.add_argument("--out-dir", type=str, required=True, help="Output directory for downloaded corpus")
    parser.add_argument("--depth", type=int, default=8, help="Max recursion depth for subfolders")
    parser.add_argument("--sleep", type=float, default=0.25, help="Seconds to sleep between requests")
    parser.add_argument("--max-pages-per-folder", type=int, default=50, help="Safety cap for pagination per folder")
    parser.add_argument("--timeout", type=int, default=120, help="Request timeout seconds")
    parser.add_argument("--limit-docs", type=int, default=0, help="Stop after N documents (0 = no limit)")
    parser.add_argument("--overwrite", action="store_true", help="Redownload files even if already present")
    parser.add_argument(
        "--user-agent",
        type=str,
        default="udaq-permitting-downloader/1.0",
        help="Custom User-Agent header",
    )
    parser.add_argument(
        "--trust-env",
        action="store_true",
        help="Allow Requests to read proxy/cert env vars (by default this script ignores env proxies).",
    )
    args = parser.parse_args(argv)

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    session = requests.Session()
    # Avoid surprising proxy settings in locked-down environments (common in CI/sandboxes).
    # Users can opt back in via --trust-env if they rely on corporate proxies.
    session.trust_env = bool(args.trust_env)
    session.headers.update({"User-Agent": args.user_agent})

    # We'll store a minimal folder-id -> title map to build a readable local structure.
    folder_titles: dict[int, str] = {args.folder_id: f"folder-{args.folder_id}"}
    entries_manifest_path = out_dir / "manifest.jsonl"
    errors_path = out_dir / "errors.jsonl"

    downloaded_docs = 0

    def append_jsonl(path: Path, obj: dict) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps(obj, ensure_ascii=False) + "\n")

    for entry in iter_folder_tree(
        session=session,
        root_folder_id=args.folder_id,
        depth=args.depth,
        sleep_s=args.sleep,
        max_pages_per_folder=args.max_pages_per_folder,
    ):
        if entry.kind == "folder":
            folder_titles.setdefault(entry.entry_id, entry.title)
            append_jsonl(
                entries_manifest_path,
                {
                    "kind": "folder",
                    "id": entry.entry_id,
                    "title": entry.title,
                    "url": entry.url,
                    "parent_id": entry.parent_id,
                },
            )
            continue

        # document
        if args.limit_docs and downloaded_docs >= args.limit_docs:
            break

        # Build an approximate local path by parent folder id/title (best-effort).
        parent_title = folder_titles.get(entry.parent_id, f"folder-{entry.parent_id}")
        subdir = out_dir / _safe_name(parent_title)
        base_name = _safe_name(entry.title)

        download_url = _electronic_file_url(entry.entry_id)

        existing = list(subdir.glob(f"{base_name}__{entry.entry_id}.*"))
        if existing and (not args.overwrite):
            append_jsonl(
                entries_manifest_path,
                {
                    "kind": "document",
                    "id": entry.entry_id,
                    "title": entry.title,
                    "url": entry.url,
                    "download_url": download_url,
                    "parent_id": entry.parent_id,
                    "local_path": str(existing[0].relative_to(out_dir)),
                    "skipped": True,
                },
            )
            continue

        tmp_path = subdir / f"{base_name}__{entry.entry_id}.bin"
        final_path = tmp_path

        if (not args.overwrite) and final_path.exists() and final_path.stat().st_size > 0:
            # already there (unknown extension); still write manifest record
            append_jsonl(
                entries_manifest_path,
                {
                    "kind": "document",
                    "id": entry.entry_id,
                    "title": entry.title,
                    "url": entry.url,
                    "download_url": download_url,
                    "parent_id": entry.parent_id,
                    "local_path": str(final_path.relative_to(out_dir)),
                    "skipped": True,
                },
            )
            continue

        try:
            size, content_type = _stream_download(session, download_url, tmp_path, timeout_s=args.timeout)
            # Some documents may not have an electronic file; fail fast if HTML is returned.
            if content_type and content_type.lower().startswith("text/html"):
                append_jsonl(
                    errors_path,
                    {
                        "kind": "document",
                        "id": entry.entry_id,
                        "url": entry.url,
                        "download_url": download_url,
                        "error": f"electronic file returned HTML (no file?)",
                    },
                )
                continue
            ext = _guess_extension_from_content_type(content_type)
            if ext:
                final_path = subdir / f"{base_name}__{entry.entry_id}{ext}"
                if final_path.exists() and args.overwrite:
                    final_path.unlink()
                tmp_path.rename(final_path)
            downloaded_docs += 1
            append_jsonl(
                entries_manifest_path,
                {
                    "kind": "document",
                    "id": entry.entry_id,
                    "title": entry.title,
                    "url": entry.url,
                    "download_url": download_url,
                    "parent_id": entry.parent_id,
                    "local_path": str(final_path.relative_to(out_dir)),
                    "bytes": size,
                    "content_type": content_type,
                },
            )
        except Exception as e:
            append_jsonl(
                errors_path,
                {"kind": "document", "id": entry.entry_id, "url": entry.url, "download_url": download_url, "error": f"download: {e}"},
            )
            # keep partial .bin if created; user can inspect

        if args.sleep > 0:
            time.sleep(args.sleep)

    _write_json(out_dir / "folders.json", {str(k): v for k, v in sorted(folder_titles.items(), key=lambda x: x[0])})

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
