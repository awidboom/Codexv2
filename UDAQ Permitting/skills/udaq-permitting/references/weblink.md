# Laserfiche WebLink (Utah DEQ) navigation tips

Start at:

- `https://lf-public.deq.utah.gov/WebLink/Browse.aspx?id=8436&dbid=0&repo=Public`

Direct folder (often useful for permitting timelines/process docs):

- `Agency Interest - Permitting`: `https://lf-public.deq.utah.gov/WebLink/Browse.aspx?id=385828&dbid=0&repo=Public`

## Folder conventions

- **General program docs** live under folders named `Agency Interest - ...` (examples include air quality, compliance, monitoring, permitting).
- **Facility-specific docs** are typically organized by **facility ID** under **numeric range** folders (e.g., `1000 - 1999`, `10000 - 19999`, `20000 - 29999`).

## How to find a facility folder (by facility ID)

1. Determine the facility ID (ask the user if they don't know it).
2. In the WebLink root, open the numeric range folder that contains the ID.
3. Browse within that range to find:
   - A folder named by facility ID, facility name, or both.
4. Open documents and capture the document title + date(s) from metadata (if shown).

## URL patterns you'll commonly see

- Browse folder contents:
  - `.../WebLink/Browse.aspx?id=<folderId>&dbid=0&repo=Public`
- View a document (often):
  - `.../WebLink/DocView.aspx?id=<docId>&dbid=0&repo=Public`

If the interface exposes "Search", prefer that when you have distinctive terms (facility name, city, permit number, approval order number).

## Optional: build a local index

If you want to avoid re-browsing the UI, create an offline index (CSV/JSONL) from a starting folder id:

- `python skills/udaq-permitting/scripts/index_weblink.py --folder-id 385828 --out data/weblink-permitting.csv --depth 6`

## Optional: download a local corpus

If you want to search and cite permitting docs repeatedly, download the "Agency Interest - Permitting" folder:

- `python skills/udaq-permitting/scripts/download_weblink_folder.py --folder-id 385828 --out-dir data/weblink/agency-interest-permitting --depth 10`

The downloader writes:

- `data/weblink/agency-interest-permitting/manifest.jsonl` (doc/folder listing + local file path)
- `data/weblink/agency-interest-permitting/folders.json` (folder id -> title map)

Once downloaded, search the local PDFs for timeline-related terms (no OCR):

- `python skills/udaq-permitting/scripts/search_local_pdfs.py --dir data/weblink/agency-interest-permitting --query "timeline|time\\s*frame|deadline|comment period|hearing|extend|\\b\\d{1,3}\\s*day(s)?\\b" --top 50`

If some PDFs are scanned/image-only, OCR them to make them searchable:

- `python skills/udaq-permitting/scripts/ocr_local_pdfs.py --dir data/weblink/agency-interest-permitting/folder-385828`
