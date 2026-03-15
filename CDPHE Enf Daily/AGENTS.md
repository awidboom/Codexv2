# Agent Guide (CDPHE Enf Daily)

## Project goal
This repo is a small, repeatable pipeline to (1) download CDPHE air enforcement PDFs, (2) extract structured per-violation records, and (3) generate simple reporting outputs for analysis and storytelling.

## What “done” looks like
- `cdphe_downloader.py` writes `downloads/cdphe_download_manifest.csv` and downloads PDFs into `downloads/`.
- `cdphe_processor.py` reads the manifest + PDFs and writes `downloads/cdphe_enforcement_summary.csv`.
- `cdphe_report.py` reads the summary CSV and writes `downloads/cdphe_enforcement_summary_report.html`.
- The above scripts continue to run end-to-end via `python cdphe_pipeline.py` (and ideally remain stable as internals evolve).

## Working style for this repo
- Optimize for clarity over cleverness; the primary user is an environmental engineer with basic coding knowledge.
- Prefer small, incremental changes that keep outputs stable.
- If a workflow will be repeated, propose a reusable “skill” or CLI workflow first; write Python only when it meaningfully reduces repeated manual work.
- Avoid introducing heavy dependencies; if a new dependency is needed, explain why and how it will be installed/used on Windows.

## Data & safety
- Treat downloaded PDFs and extracted text as potentially sensitive; avoid pasting large excerpts into chat and avoid logging full document bodies.
- Keep raw downloads out of version control (the `downloads/` folder is expected to be local-only).
- Be conservative with automation that hits external services; prefer explicit user intent before changing scraping/downloading behavior.

## Repo conventions
- Keep pipeline “contracts” stable: don’t rename output columns/files without updating downstream consumers and `README.md`.
- Prefer configurable paths (repo-relative defaults) over machine-specific absolute paths; when changing path behavior, keep backward-compatible defaults when possible.
- Keep output deterministic where feasible (stable ordering, stable column sets).

## Coding guidelines (Python)
- Use `pathlib.Path`, type hints where helpful, and straightforward function boundaries.
- Favor pure helpers for parsing/normalization (easy to test and reason about).
- Avoid broad exception swallowing; handle expected failure modes and surface actionable error messages.
- If you add parsing logic that’s easy to regress, add a minimal test or fixture-driven check only if the repo already has a test pattern; otherwise keep a small, runnable “sanity check” snippet or documented example in `README.md`.

## How to run (common commands)
- `python cdphe_pipeline.py`
- `python cdphe_downloader.py`
- `python cdphe_processor.py`
- `python cdphe_report.py`

## When you’re unsure
- Ask clarifying questions about the desired output columns, categorization rules, or how results will be consumed (CSV vs HTML vs dashboard).
- Prefer changes that are explainable in domain terms (facility, case number, inspection date, citations) rather than software patterns.
