---
name: udaq-ao-extractor
description: Extract structured data from Utah DAQ issued Approval Orders (AOs) using the repo script skills/udaq-permitting/scripts/scrape_permits.py, including generating CSV exports, adjusting PDF text-extraction regexes, and capturing NOI/application received dates (e.g., 'Notice of Intent (NOI) received on ...') from issued AO PDFs.
---

# UDAQ Approval Order Extractor

Use this skill to pull a CSV of issued Approval Orders (AOs) from `daqpermitting.utah.gov` and extract key fields from the PDF text, including the NOI/application received date when present.

## Run the scraper

Script: `skills/udaq-permitting/scripts/scrape_permits.py`

- Full run (writes a CSV in the current working directory):
  - `python skills/udaq-permitting/scripts/scrape_permits.py --out permits_all.csv`
- Quick smoke test:
  - `python skills/udaq-permitting/scripts/scrape_permits.py --out permits_sample.csv --max-permits 25`

## Output columns

The CSV includes (among others):

- `ApprovalOrderID` (e.g., `DAQE-AN141970007-25`)
- `AppliedOn` (NOI/application received date extracted from the PDF, when present)
- `IssuedOn` (from the listing; typically `YYYY-MM-DD`)
- `PDFLink` (direct link to the PDF)
- Emissions split into two sets from the Summary of Emissions table:
  - `Project_*_TPY` (Change (tpy))
  - `Source_*_TPY` (Total (tpy))

## How “AppliedOn” is extracted

The scraper looks for cover-letter language like:

- `Notice of Intent (NOI) received on July 18, 2025`
- `NOI received on May 1, 2025`
- `Application received on <date>` (fallback)

If the PDF is scanned or text extraction fails, `AppliedOn` may be blank. For some garbled-text PDFs, the scraper will best-effort OCR the first page (when OCR tooling is available) to recover `AppliedOn`.

## Extend the extractor

When adding new fields:

1. Identify the exact phrase(s) used across multiple AOs.
2. Add a robust regex that tolerates line breaks introduced by PDF text extraction.
3. Update `FIELDNAMES` and the row assembly in `process_item`.

Tip: Prefer extracting from the first 1–2 pages (cover letter / cover sheet) when possible.
