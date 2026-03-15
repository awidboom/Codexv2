#!/usr/bin/env python3
"""
Split a master Evaluation PDF into one PDF per evaluation (footer-safe, addendum-aware)
with strict, stable app-change detection and robust naming.

Usage:
  python split_evaluations.py
  python split_evaluations.py <pdf>
  python split_evaluations.py <pdf> <outdir>
"""

import os, re, sys, json
from typing import List, Tuple, Optional, Iterable
from collections import Counter

# ======= TUNED DEFAULTS =======
DEFAULT_PDF = "B2758_9 2023_07_Renewal_Proposed_SOB-evals.pdf"
OUTDIR_DEFAULT = "split_evals"

HEADING_REGEX = r"(ENGINEERING EVALUATION(?: REPORT)?|EVALUATION REPORT)"
DETECT_BY = "both"            # "heading" | "appchange" | "both"
TOP_LINES = 120               # lines from top-of-page to scan (ignore footers)
TOP_APP_LINES = 25            # stricter window for app-line detection (first N lines)
LOOKAHEAD_PAGES = 6           # pages from start to find app number(s) for naming
ANCHOR_LINE = True            # require heading on its own line
MIN_GAP = 2                   # min pages between starts
APPCHANGE_CONFIRM = True      # require confirmation for app changes
CONFIRM_LOOKAHEAD = 3         # pages to confirm after app-number change
DEBUG = False

SECTION_HEADS_BACKGROUND = [r"BACKGROUND"]  # early-phase anchor(s)

ADDENDUM_PAT = re.compile(r"\b(ADDENDUM|AMENDMENT)\b", re.I)
HEADING_PAT = re.compile(HEADING_REGEX, re.I)

# Try PyPDF2 first, then pypdf
try:
    from PyPDF2 import PdfReader, PdfWriter
except Exception:
    try:
        from pypdf import PdfReader, PdfWriter
    except Exception:
        raise RuntimeError("Install PyPDF2 or pypdf: pip install PyPDF2")


def extract_text(reader: PdfReader, i: int) -> str:
    try:
        t = reader.pages[i].extract_text() or ""
        return t.replace("\r\n", "\n").replace("\r", "\n")
    except Exception:
        return ""


def top_chunk(text: str, top_lines: int) -> str:
    lines = text.splitlines()
    return "\n".join(lines[:top_lines])


def has_heading_in_top(reader: PdfReader, page_idx: int) -> bool:
    txt_top = top_chunk(extract_text(reader, page_idx), TOP_LINES)
    pat = re.compile(rf"^\s*(?:{HEADING_REGEX})\s*$", re.I | re.M) if ANCHOR_LINE \
          else HEADING_PAT
    if pat.search(txt_top):
        return True

    # Some PDFs render the heading with odd unicode/spaces, causing the strict
    # anchored match to fail. As a safe fallback, look for a line that normalizes
    # to exactly the heading text, and require at least one other "start page"
    # signal (application number or BACKGROUND) to avoid false positives (e.g. TOC).
    appish = bool(anchored_app_numbers_on_page(reader, page_idx))
    bg = has_background_in_top(reader, page_idx)
    if not (appish or bg):
        return False

    for line in txt_top.splitlines():
        norm = re.sub(r"[^A-Za-z ]+", " ", line)
        norm = re.sub(r"\s+", " ", norm).strip().upper()
        if norm in ("ENGINEERING EVALUATION", "ENGINEERING EVALUATION REPORT", "EVALUATION REPORT"):
            return True
    return False


def page_has_heading_anywhere(reader: PdfReader, page_idx: int) -> bool:
    return bool(HEADING_PAT.search(extract_text(reader, page_idx)))


def has_background_in_top(reader: PdfReader, page_idx: int) -> bool:
    txt_top = top_chunk(extract_text(reader, page_idx), TOP_LINES)
    for h in SECTION_HEADS_BACKGROUND:
        if re.search(rf"^\s*{h}\s*$", txt_top, re.I | re.M):
            return True
    return False


def is_addendum_in_top(reader: PdfReader, page_idx: int) -> bool:
    txt_top = top_chunk(extract_text(reader, page_idx), TOP_LINES)
    return bool(ADDENDUM_PAT.search(txt_top))


# ---------- Application number extraction ----------

APP_LINE_STRICT = re.compile(
    r"^\s*Application\s*(?:No\.|Number|#)?\s*[:\-]?\s*(\d{5,6})\b.*$",
    re.I,
)

# OCR/text-extraction often introduces spaces inside tokens, e.g.:
#   "Application 21 713" or "APPLICATI ON NO.  21713"
# We'll compact whitespace for a second pass to recover the number.
APP_LINE_COMPACT = re.compile(
    r"^Application(?:No\.|Number|#)?[:\-]?(\d{5,6})\b.*$",
    re.I,
)

EXCLUDE_INLINE_TOKENS = re.compile(
    r"\b(PERMIT\s+APPLICATION|NSR|AUTHORITY\s+TO\s+CONSTRUCT|ATC|TITLE\s+V|BANKING|OFFSET|CONDITION)\b",
    re.I
)

PAGE_OF_PAT = re.compile(r"\bPage\s+\d+\s+of\s+\d+\b", re.I)

APP_INLINE = re.compile(
    r"\bApplication\s*(?:No\.|Number|#)?\s*[:\-]?\s*(\d{5,6})\b",
    re.I,
)
APP_INLINE_COMPACT = re.compile(
    r"Application(?:No\.|Number|#)?[:\-]?(\d{5,6})\b",
    re.I,
)

def anchored_app_numbers_on_page(reader: PdfReader, page_idx: int) -> List[str]:
    """
    Return all anchored app numbers from the first TOP_APP_LINES lines.
    - Must be a line that STARTS with 'Application ... <digits>'
    - Ignore lines with clear cross-ref/permit keywords (EXCLUDE_INLINE_TOKENS)
    """
    txt = extract_text(reader, page_idx)
    top = top_chunk(txt, TOP_APP_LINES)
    nums = []
    for line in top.splitlines():
        # Many PDFs have a persistent header like:
        #   "Application # 16082  Page 195 of 1354  Plant #14628"
        # which is not the eval's application number and will drown out detection.
        if PAGE_OF_PAT.search(line):
            continue
        if EXCLUDE_INLINE_TOKENS.search(line):
            continue
        m = APP_LINE_STRICT.match(line)
        if m:
            nums.append(m.group(1))
            continue

        compact = re.sub(r"\s+", "", line)
        m2 = APP_LINE_COMPACT.match(compact)
        if m2:
            nums.append(m2.group(1))
            continue

        # Fallback: allow "… Application 16888 …" in title/header lines.
        m3 = APP_INLINE.search(line)
        if m3:
            nums.append(m3.group(1))
            continue
        m4 = APP_INLINE_COMPACT.search(compact)
        if m4:
            nums.append(m4.group(1))
    return nums


def mode_then_max(nums: Iterable[str]) -> Optional[str]:
    nums = list(nums)
    if not nums:
        return None
    c = Counter(nums)
    most = c.most_common()
    top_count = most[0][1]
    candidates = [n for n, cnt in most if cnt == top_count]
    if len(candidates) == 1:
        return candidates[0]
    # tie-breaker: choose numerically largest
    try:
        return sorted(candidates, key=lambda x: int(x))[-1]
    except Exception:
        return candidates[-1]


def confirm_new_section(reader: PdfReader, start_idx: int, end_limit: int) -> bool:
    """
    Confirm a new section by seeing either:
      - the main heading ANYWHERE within CONFIRM_LOOKAHEAD pages, OR
      - an anchored BACKGROUND in the top chunk within CONFIRM_LOOKAHEAD pages.
    (We no longer count generic section headers to avoid mid-eval confirmations.)
    """
    last = min(end_limit, start_idx + CONFIRM_LOOKAHEAD)
    for i in range(start_idx, last + 1):
        if page_has_heading_anywhere(reader, i):
            return True
        if has_background_in_top(reader, i):
            return True
    return False


def find_eval_starts(reader: PdfReader) -> List[int]:
    """
    Start detection:
      1) Heading-based: top-of-page heading (robust, but not always present).
      2) App-change-based: anchored app # appears in TOP_APP_LINES AND
         repeats on the very next page (stability). Then confirm.
    """
    starts: List[int] = []
    last_app_seen: Optional[str] = None

    n_pages = len(reader.pages)
    for i in range(n_pages):
        heading_hit = (DETECT_BY in ("heading", "both")) and has_heading_in_top(reader, i)

        app_nums_here = anchored_app_numbers_on_page(reader, i) if (DETECT_BY in ("appchange", "both")) else []
        stable_app = None
        if app_nums_here:
            # require stability: same app appears on next page's top lines
            if i + 1 < n_pages:
                next_nums = anchored_app_numbers_on_page(reader, i + 1)
                common = set(app_nums_here).intersection(next_nums)
                if common:
                    stable_app = mode_then_max(common)

        app_hit = False
        if stable_app and stable_app != last_app_seen:
            if not APPCHANGE_CONFIRM or confirm_new_section(reader, i, n_pages - 1):
                app_hit = True
                last_app_seen = stable_app

        if heading_hit or app_hit:
            if (not starts) or (i - starts[-1]) >= MIN_GAP:
                starts.append(i)

        # Keep tracking the last stable app for context
        if stable_app:
            last_app_seen = stable_app

    return starts


def detect_app_for_range(reader: PdfReader, start: int, end: int) -> Optional[str]:
    """
    Determine the application number for naming by looking at anchored Application
    lines across the first LOOKAHEAD_PAGES pages; pick the mode, tie→max.
    """
    # Prefer the start page: later pages often include persistent headers or other
    # cross-references that can drown out the eval's true application number.
    first_page_nums = anchored_app_numbers_on_page(reader, start)
    if first_page_nums:
        return mode_then_max(first_page_nums)

    last = min(end, start + LOOKAHEAD_PAGES)
    all_nums = []
    for i in range(start, last + 1):
        all_nums.extend(anchored_app_numbers_on_page(reader, i))
    return mode_then_max(all_nums)


# ---------- Splitting & Output ----------

def unique_outpath(base_dir: str, base_name: str) -> str:
    """Never overwrite: add -2, -3... if file exists."""
    path = os.path.join(base_dir, base_name)
    if not os.path.exists(path):
        return path
    root, ext = os.path.splitext(base_name)
    k = 2
    while True:
        cand = os.path.join(base_dir, f"{root}-{k}{ext}")
        if not os.path.exists(cand):
            return cand
        k += 1


def split_pdf(pdf_path: str, outdir: str, debug: bool=False) -> dict:
    os.makedirs(outdir, exist_ok=True)
    reader = PdfReader(pdf_path)

    starts = find_eval_starts(reader)
    if not starts:
        raise RuntimeError("No evaluation starts found with current settings.")

    # Build [start,end] ranges
    ranges: List[Tuple[int, int]] = []
    for idx, s in enumerate(starts):
        e = (starts[idx + 1] - 1) if (idx + 1 < len(starts)) else (len(reader.pages) - 1)
        ranges.append((s, e))

    # Separate repeated application numbers (treat repeats as addendums/parts).
    counters = {}
    results = []
    for idx, (s, e) in enumerate(ranges, 1):
        app = detect_app_for_range(reader, s, e)
        counters.setdefault(app, 0)
        counters[app] += 1
        repeat_count = counters[app]
        is_repeat_for_app = (app is not None) and (repeat_count > 1)

        if app:
            if repeat_count == 1:
                base = f"application_{app}.pdf"
            else:
                base = f"application_{app}-addendum-{repeat_count - 1}.pdf"
        else:
            base = f"evaluation_{idx:02d}.pdf"

        out_path = unique_outpath(outdir, base)

        writer = PdfWriter()
        for p in range(s, e + 1):
            writer.add_page(reader.pages[p])
        with open(out_path, "wb") as f:
            writer.write(f)

        rec = {
            "index": idx, "start_page": s, "end_page": e,
            "application_number": app, "output": out_path,
            "addendum_like": is_repeat_for_app
        }
        if debug:
            rec["top_preview"] = top_chunk(extract_text(reader, s), TOP_LINES)[:1200]
        results.append(rec)

    manifest = {
        "source_pdf": os.path.abspath(pdf_path),
        "heading_regex": HEADING_REGEX,
        "detect_by": DETECT_BY,
        "top_lines": TOP_LINES,
        "top_app_lines": TOP_APP_LINES,
        "lookahead_pages": LOOKAHEAD_PAGES,
        "anchor_line": ANCHOR_LINE,
        "min_gap": MIN_GAP,
        "appchange_confirm": APPCHANGE_CONFIRM,
        "confirm_lookahead": CONFIRM_LOOKAHEAD,
        "sections": results
    }
    with open(os.path.join(outdir, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    return manifest


def main():
    pdf = DEFAULT_PDF
    outdir = OUTDIR_DEFAULT
    if len(sys.argv) >= 2 and sys.argv[1].strip():
        pdf = sys.argv[1]
    if len(sys.argv) >= 3 and sys.argv[2].strip():
        outdir = sys.argv[2]

    if not os.path.exists(pdf):
        raise SystemExit(f"Input PDF not found: {pdf}")

    manifest = split_pdf(pdf, outdir, debug=DEBUG)
    print(json.dumps(manifest, indent=2))
    print(f"\nWrote split PDFs to: {os.path.abspath(outdir)}")
    print(f"Manifest: {os.path.join(os.path.abspath(outdir), 'manifest.json')}")

if __name__ == "__main__":
    main()
