---
name: udaq-permitting
description: Support answering questions about Utah Division of Air Quality (UDAQ) permitting and Utah air quality rules (Utah Administrative Code R307 Series 100-800), including locating/citing relevant rule sections and retrieving supporting documents from Utah DEQ's public Laserfiche WebLink document system (agency-interest folders and facility-ID-based folders).
---

# UDAQ Permitting (Utah Air Quality)

Use this skill to (1) find and cite the right Utah air quality rule text (primarily UAC `R307-*`) and (2) locate supporting permitting/agency documents in Utah DEQ's public Laserfiche WebLink repository.

## Workflow: rule questions (UAC R307)

1. Confirm the user's target: topic + program (e.g., NSR, Title V, SIP, registration, fees, penalties) + the kind of output they want (plain-English summary vs. exact citations).
2. Locate the authoritative rule text:
   - Start with Utah DEQ's "Air Quality Laws and Rules" page for navigation and DAQ-curated links.
   - For exact/official text and revision history, prefer the Utah Administrative Rules site (linked from DEQ) and cite the specific section (e.g., `R307-401-8(1)(a)`).
3. Answer with:
   - The exact rule citation(s) and the relevant subsection(s).
   - Effective/last-updated date if the source provides it (rules change).
   - A concise plain-English explanation scoped to the user's question.
4. If the user is asking for a compliance determination or legal interpretation, be explicit about assumptions and suggest confirming with UDAQ or counsel.

If you need a quick map of "Series 100-800" and what each series covers, read `skills/udaq-permitting/references/r307-series.md`.

## Workflow: document retrieval (Laserfiche WebLink)

If a local WebLink corpus exists in this repo (recommended for repeat permitting work), prefer it first:

- `data/weblink/agency-interest-permitting/` (downloaded from Agency Interest - Permitting)
- Use `data/weblink/agency-interest-permitting/manifest.jsonl` to find candidate documents by title/id, then open the local file.

1. Start at the public WebLink browse root (see `skills/udaq-permitting/references/sources.md`).
2. Choose the right branch:
   - **General program files**: open the folders starting with `Agency Interest - ...` (e.g., permitting, compliance).
   - **Facility-specific files**: use the facility ID to find the numeric "range" folder that contains it (e.g., `10000 - 19999`), then locate the facility's folder/documents under that range.
3. When returning results, include:
   - The document title, document/folder id (if visible), and the WebLink URL you used.
   - Any dates shown in the document metadata.

For navigation tips and URL patterns, read `skills/udaq-permitting/references/weblink.md`.

If you want to build a local catalog of a WebLink folder (e.g., "Agency Interest - Permitting") for faster searching, run `skills/udaq-permitting/scripts/index_weblink.py` to export a `.csv`/`.jsonl` index.

If you want to download the folder contents locally, run `skills/udaq-permitting/scripts/download_weblink_folder.py` (see `skills/udaq-permitting/references/weblink.md` for an example).

If you want to keyword-search the local permitting corpus for timelines (without OCR), use `skills/udaq-permitting/scripts/search_local_pdfs.py`.

## Source hygiene

- Prefer official sources (Utah DEQ/DAQ pages, Utah Administrative Rules, and the DEQ WebLink repository).
- Always verify "latest" by checking the current online source before answering (especially for rules, fee schedules, and forms).
