# CDPHE Enforcement Pipeline

## Goal
Build a repeatable pipeline that pulls CDPHE enforcement documents, extracts structured details for each violation, and produces a clean dataset that can drive summaries and visual storytelling.

## Agentic Structure
- Download agent: fetch enforcement PDFs and store a manifest with metadata.
- Processing agent: read PDFs, split violations, extract citations, and write a CSV.
- Summary agent (future): roll up statistics and trends for reporting.
- Visualization agent (future): render an infographic or report from the CSV.

## Core Scripts
- cdphe_downloader.py: downloads PDFs and writes `downloads/cdphe_download_manifest.csv`.
- cdphe_processor.py: parses PDFs and writes `downloads/cdphe_enforcement_summary.csv`.
- cdphe_pipeline.py: runs download then processing in sequence.

## Outputs
- downloads/*.pdf: raw enforcement documents.
- downloads/cdphe_download_manifest.csv: portal metadata captured during download.
- downloads/cdphe_enforcement_summary.csv: per-violation records with portal metadata, citations, and categories.

## Portal Metadata Contract
The downloader now treats the CDPHE portal grid as the authoritative source for document-level metadata and writes these fields to the manifest:

- `file_name`
- `pdf_url`
- `document_date`
- `document_title`
- `airs_no`
- `air_permit_number`
- `case_number`
- `facility_name`
- `company`
- `document_handle`

The processor carries those manifest fields into the summary CSV and uses the portal metadata as the default source for:

- `document_date`
- `document_title`
- `airs_no`
- `air_permit_number`
- `case_number`
- `facility_name`
- `company`
- `document_handle`

PDF text extraction remains a fallback for fields such as `inspection_date`, `violation_description`, `rule_citation`, `equipment_type`, and `source_type`.

`document_handle` is also used by the downloader to avoid re-downloading the same portal document multiple times when the search grid repeats it across multiple rows.

## Typical Use
- `python cdphe_pipeline.py`
- `python cdphe_downloader.py` (download only)
- `python cdphe_processor.py` (process only)

## Date-Range Workflows (Month-by-Month)
- Download + parse one month, then delete those PDFs:
  - `python cdphe_pipeline.py --month 2025-12 --cleanup-pdfs`
- Download a custom range:
  - `python cdphe_downloader.py --from-date 2025-12-01 --to-date 2025-12-31`
- Parse + delete PDFs listed in the current manifest:
  - `python cdphe_processor.py --cleanup-pdfs`

## Extensibility
If CDPHE adds different document types, add a new downloader or processor module and keep the pipeline contract the same: write a manifest, then produce structured outputs. This keeps the reporting and visualization steps stable even as sources change.

## End State
Use the structured CSV to generate an infographic or narrative report that highlights enforcement trends, recurring violation types, penalties, and company profiles.
