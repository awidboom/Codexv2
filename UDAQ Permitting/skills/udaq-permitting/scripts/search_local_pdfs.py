#!/usr/bin/env python
"""
Search local PDFs for keywords by extracting text (no OCR).

Example:
  python skills/udaq-permitting/scripts/search_local_pdfs.py ^
    --dir data/weblink/agency-interest-permitting ^
    --query \"timeline|time\\s*frame|deadline|comment period|hearing|extend|\\b\\d{1,3}\\s*day(s)?\\b\" ^
    --top 50

To print small excerpts around the first match per PDF:
  python skills/udaq-permitting/scripts/search_local_pdfs.py ^
    --dir data/weblink/agency-interest-permitting ^
    --query \"notice of intent|\\bNOI\\b|approval order|\\bAO\\b|complete application|completeness|\\b(30|90)\\s*day(s)?\\b\" ^
    --top 25 --snippets 1 --context 200
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

from pypdf import PdfReader


@dataclass(frozen=True)
class Hit:
    path: Path
    score: int
    total_hits: int
    first_snippet: str | None


def _extract_text(path: Path, max_pages: int = 0) -> str:
    reader = PdfReader(str(path))
    pages = reader.pages if max_pages <= 0 else reader.pages[:max_pages]
    parts: list[str] = []
    for page in pages:
        parts.append(page.extract_text() or "")
    return "\n".join(parts)


def _make_snippet(text: str, start: int, end: int, context: int) -> str:
    a = max(0, start - context)
    b = min(len(text), end + context)
    snippet = " ".join(text[a:b].split())
    return snippet


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--dir", required=True, help="Directory to search (recursively) for .pdf files")
    p.add_argument("--query", required=True, help="Regex to search in extracted text (case-insensitive)")
    p.add_argument("--top", type=int, default=25, help="Number of results to print")
    p.add_argument("--max-pages", type=int, default=0, help="Limit extraction to first N pages (0 = all pages)")
    p.add_argument("--min-chars", type=int, default=200, help="Treat PDFs with <N non-whitespace chars as needing OCR")
    p.add_argument("--snippets", type=int, default=0, help="Print up to N snippet(s) per matching PDF")
    p.add_argument("--context", type=int, default=180, help="Snippet context characters before/after match")
    args = p.parse_args(argv)

    root = Path(args.dir)
    if not root.exists():
        raise SystemExit(f"Directory not found: {root}")

    rx = re.compile(args.query, re.IGNORECASE)

    pdfs = sorted(root.rglob("*.pdf"))
    # Ignore intermediate per-page OCR artifacts (used by ocr_local_pdfs.py fallback).
    pdfs = [p for p in pdfs if "_ocr_tmp_pages" not in str(p)]
    hits: list[Hit] = []
    needs_ocr: list[Path] = []
    errors: list[tuple[Path, str]] = []

    for pdf in pdfs:
        try:
            text = _extract_text(pdf, max_pages=args.max_pages)
            compact_len = len("".join(text.split()))
            if compact_len < args.min_chars:
                needs_ocr.append(pdf)
                continue

            m0 = rx.search(text)
            if not m0:
                continue
            all_matches = list(rx.finditer(text))

            # Score: number of distinct matched groups/terms isn't available, so use match count,
            # and separately track total hits.
            first_snippet = _make_snippet(text, m0.start(), m0.end(), context=args.context)
            hits.append(Hit(path=pdf, score=1, total_hits=len(all_matches), first_snippet=first_snippet))
        except Exception as e:
            errors.append((pdf, str(e)))

    hits.sort(key=lambda h: h.total_hits, reverse=True)

    print(f"pdfs: {len(pdfs)}")
    print(f"matched: {len(hits)}")
    print(f"needs_ocr_or_image_only: {len(needs_ocr)}")
    print(f"errors: {len(errors)}")

    if hits:
        print("\nTop matches:")
        for h in hits[: max(0, args.top)]:
            print(f"- {h.path} (hits={h.total_hits})")
            if args.snippets and h.first_snippet:
                try:
                    print(f"  snippet: {h.first_snippet}")
                except UnicodeEncodeError:
                    enc = sys.stdout.encoding or "utf-8"
                    safe = h.first_snippet.encode(enc, errors="backslashreplace").decode(enc, errors="strict")
                    print(f"  snippet: {safe}")

    if needs_ocr:
        print("\nLikely needs OCR (low/no extractable text):")
        for n in needs_ocr[:50]:
            print(f"- {n}")
        if len(needs_ocr) > 50:
            print(f"... (+{len(needs_ocr) - 50} more)")

    if errors:
        print("\nErrors (first 10):")
        for path, err in errors[:10]:
            print(f"- {path}: {err}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
