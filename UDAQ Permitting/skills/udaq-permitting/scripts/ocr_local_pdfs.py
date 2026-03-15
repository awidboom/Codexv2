#!/usr/bin/env python
"""
OCR local PDFs to make them text-searchable (best-effort).

This repo's permitting corpus includes some scanned/image-only PDFs. This script:
  - detects PDFs with low/no extractable text
  - runs OCR (if OCR tooling is available)
  - writes new searchable PDFs (by default alongside originals with a *_ocr.pdf suffix)

Supported OCR backends (in order):
  1) ocrmypdf (preferred) if installed/available on PATH
  2) pytesseract + pdf2image (requires Tesseract + Poppler/pdftoppm on PATH)

Examples:
  # OCR a directory (recursively), writing *_ocr.pdf next to originals
  python skills/udaq-permitting/scripts/ocr_local_pdfs.py --dir data/weblink/agency-interest-permitting/folder-385828

  # OCR specific files
  python skills/udaq-permitting/scripts/ocr_local_pdfs.py --files <path1> <path2>
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

from pypdf import PdfReader


@dataclass(frozen=True)
class OcrResult:
    pdf: Path
    output: Path
    status: str  # "skipped" | "ok" | "failed"
    message: str


def _has_extractable_text(pdf: Path, min_chars: int, max_pages: int) -> bool:
    reader = PdfReader(str(pdf))
    pages = reader.pages if max_pages <= 0 else reader.pages[:max_pages]
    extracted = []
    for page in pages:
        extracted.append(page.extract_text() or "")
    compact_len = len("".join(" ".join(extracted).split()))
    return compact_len >= min_chars


def _ocrmypdf_available() -> bool:
    return shutil.which("ocrmypdf") is not None


def _find_tesseract() -> Path | None:
    """
    Prefer PATH, but fall back to common Windows install locations.
    """
    found = shutil.which("tesseract")
    if found:
        return Path(found)
    candidates = [
        Path(r"C:\Program Files\Tesseract-OCR\tesseract.exe"),
        Path(r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"),
    ]
    for c in candidates:
        if c.exists():
            return c
    return None


def _find_pdftoppm() -> Path | None:
    """
    Prefer PATH, but fall back to a typical WinGet Poppler install path.
    """
    found = shutil.which("pdftoppm")
    if found:
        return Path(found)
    # WinGet installs Poppler under LOCALAPPDATA\Microsoft\WinGet\Packages\...\Library\bin
    local = Path.home() / "AppData" / "Local" / "Microsoft" / "WinGet" / "Packages"
    if local.exists():
        matches = list(local.glob("**/Library/bin/pdftoppm.exe"))
        if matches:
            # pick the shortest path (usually the direct package path)
            matches.sort(key=lambda p: len(str(p)))
            return matches[0]
    return None


def _run_ocrmypdf(inp: Path, out: Path) -> tuple[bool, str]:
    cmd = [
        "ocrmypdf",
        "--skip-text",
        "--force-ocr",
        "--output-type",
        "pdf",
        str(inp),
        str(out),
    ]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True)
        if proc.returncode == 0:
            return True, "ocrmypdf ok"
        return False, (proc.stderr or proc.stdout or f"ocrmypdf failed ({proc.returncode})")[:8000]
    except FileNotFoundError:
        return False, "ocrmypdf not found on PATH"


def _run_pytesseract_pdf2image(inp: Path, out: Path) -> tuple[bool, str]:
    """
    Minimal fallback OCR: render pages to images (pdf2image) and OCR them with pytesseract.
    Output is a text-only PDF built from page images plus a hidden text layer is not trivial
    without extra tooling, so this path is mainly a diagnostics fallback.

    In practice, prefer installing ocrmypdf.
    """
    try:
        from pdf2image import convert_from_path  # type: ignore
        import pytesseract  # type: ignore
        from pypdf import PdfWriter
    except Exception as e:
        return False, f"missing python deps for fallback (pdf2image/pytesseract): {e}"

    tesseract = _find_tesseract()
    if not tesseract:
        return False, "tesseract not found (install Tesseract OCR; common path is C:\\Program Files\\Tesseract-OCR\\tesseract.exe)"

    pdftoppm = _find_pdftoppm()
    if not pdftoppm:
        return False, "pdftoppm not found (install Poppler for Windows; WinGet installs under %LOCALAPPDATA%\\Microsoft\\WinGet\\Packages\\...\\Library\\bin)"
    poppler_path = str(pdftoppm.parent)

    # Point pytesseract at the binary even if it's not on PATH.
    pytesseract.pytesseract.tesseract_cmd = str(tesseract)

    # This fallback writes a searchable PDF produced by Tesseract for each page, then merges them.
    # pytesseract can output per-page PDFs; we'll concatenate.
    tmp_dir = out.parent / (out.stem + "_tmp_pages")
    tmp_dir.mkdir(parents=True, exist_ok=True)
    page_pdfs: list[Path] = []

    try:
        # Process one page at a time to avoid loading the entire PDF as images in memory.
        page_count = len(PdfReader(str(inp)).pages)
        for i in range(1, page_count + 1):
            images = convert_from_path(
                str(inp),
                dpi=300,
                first_page=i,
                last_page=i,
                poppler_path=poppler_path,
            )
            if not images:
                continue
            img = images[0]
            page_pdf = tmp_dir / f"page_{i:04d}.pdf"
            pdf_bytes = pytesseract.image_to_pdf_or_hocr(img, extension="pdf")
            page_pdf.write_bytes(pdf_bytes)
            page_pdfs.append(page_pdf)

        w = PdfWriter()
        for p in page_pdfs:
            r = PdfReader(str(p))
            for page in r.pages:
                w.add_page(page)
        with open(out, "wb") as f:
            w.write(f)

        return True, "pytesseract ok (page-OCR + merge)"
    except Exception as e:
        return False, f"pytesseract/pdf2image failed: {e}"
    finally:
        # Keep tmp pages for debugging if OCR fails; remove on success.
        pass


def _default_output_path(pdf: Path) -> Path:
    return pdf.with_name(pdf.stem + "_ocr" + pdf.suffix)


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--dir", type=str, help="Directory to scan recursively for PDFs")
    g.add_argument("--files", nargs="+", help="Explicit PDF file paths")
    ap.add_argument("--min-chars", type=int, default=200, help="Treat PDFs with <N extracted chars as needing OCR")
    ap.add_argument("--max-pages", type=int, default=2, help="Only test first N pages for text (0=all)")
    ap.add_argument("--overwrite", action="store_true", help="Overwrite existing *_ocr.pdf outputs")
    ap.add_argument("--dry-run", action="store_true", help="Report what would be OCR'd, without writing files")
    ap.add_argument("--backend", choices=["auto", "ocrmypdf", "pytesseract"], default="auto")
    args = ap.parse_args(argv)

    if args.dir:
        pdfs = sorted(Path(args.dir).rglob("*.pdf"))
    else:
        pdfs = [Path(p) for p in args.files]

    pdfs = [p for p in pdfs if p.exists()]

    if not pdfs:
        print("No PDFs found.")
        return 2

    backend = args.backend
    if backend == "auto":
        if _ocrmypdf_available():
            backend = "ocrmypdf"
        else:
            backend = "pytesseract"

    if backend == "ocrmypdf" and not _ocrmypdf_available():
        print("ERROR: ocrmypdf not found on PATH.")
        print("Install ocrmypdf + its dependencies (and ensure 'ocrmypdf' is on PATH), then retry.")
        return 2

    if backend == "pytesseract":
        # Validate prerequisites early to give clear errors.
        if not _find_tesseract():
            print("ERROR: tesseract not found.")
            print("Install Tesseract OCR (or ensure it exists at C:\\Program Files\\Tesseract-OCR\\tesseract.exe), then retry.")
            return 2
        if not _find_pdftoppm():
            print("ERROR: pdftoppm not found.")
            print("Install Poppler for Windows (pdftoppm), then retry.")
            return 2

    results: list[OcrResult] = []

    for pdf in pdfs:
        try:
            if _has_extractable_text(pdf, min_chars=args.min_chars, max_pages=args.max_pages):
                results.append(OcrResult(pdf=pdf, output=_default_output_path(pdf), status="skipped", message="already has text"))
                continue

            out = _default_output_path(pdf)
            if out.exists() and not args.overwrite:
                results.append(OcrResult(pdf=pdf, output=out, status="skipped", message="output exists"))
                continue

            if args.dry_run:
                results.append(OcrResult(pdf=pdf, output=out, status="skipped", message="dry-run (would OCR)"))
                continue

            if backend == "ocrmypdf":
                ok, msg = _run_ocrmypdf(pdf, out)
            else:
                ok, msg = _run_pytesseract_pdf2image(pdf, out)

            if ok and out.exists():
                # sanity check
                if _has_extractable_text(out, min_chars=args.min_chars, max_pages=args.max_pages):
                    results.append(OcrResult(pdf=pdf, output=out, status="ok", message=msg))
                else:
                    results.append(OcrResult(pdf=pdf, output=out, status="failed", message="OCR ran but output still has low text"))
            else:
                results.append(OcrResult(pdf=pdf, output=out, status="failed", message=msg))

        except Exception as e:
            results.append(OcrResult(pdf=pdf, output=_default_output_path(pdf), status="failed", message=str(e)))

    ok = sum(1 for r in results if r.status == "ok")
    skipped = sum(1 for r in results if r.status == "skipped")
    failed = sum(1 for r in results if r.status == "failed")

    print(f"backend: {backend}")
    print(f"pdfs: {len(results)} ok: {ok} skipped: {skipped} failed: {failed}")
    for r in results:
        if r.status != "skipped":
            print(f"- {r.status}: {r.pdf} -> {r.output} ({r.message})")

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
