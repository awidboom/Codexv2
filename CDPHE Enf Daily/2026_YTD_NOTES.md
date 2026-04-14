# 2026 Year-to-Date Notes

This project was refreshed for the date range `2026-01-01` through `2026-03-18`.

## Current 2026 YTD artifacts

- Manifest: [downloads/cdphe_download_manifest.csv](C:/Users/aaw/Codex/CDPHE%20Enf%20Daily/downloads/cdphe_download_manifest.csv)
- CSV: [downloads/cdphe_enforcement_summary_2026_to_date.csv](C:/Users/aaw/Codex/CDPHE%20Enf%20Daily/downloads/cdphe_enforcement_summary_2026_to_date.csv)
- HTML report: [outputs/cdphe_enforcement_summary_report_2026_to_date.html](C:/Users/aaw/Codex/CDPHE%20Enf%20Daily/outputs/cdphe_enforcement_summary_report_2026_to_date.html)

The canonical `downloads/cdphe_enforcement_summary.csv` was locked during the 2026 year-to-date refresh, so the parsed output was written to the alternate `*_2026_to_date.csv` file instead.

## Metadata handling

The pipeline now uses CDPHE portal metadata as the source of truth for the following document-level fields:

- `document_date`
- `document_title`
- `airs_no`
- `air_permit_number`
- `case_number`
- `facility_name`
- `company`
- `document_handle`

`document_title` is used as the primary key for `enforcement_type` normalization when it is available from the manifest.

`document_handle` is used by the downloader to suppress repeated downloads of the same underlying portal document.
