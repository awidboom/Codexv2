<INSTRUCTIONS>
## Goal
Automate pulling regulatory resources for a given eCFR rule so context stays focused. Start with:
- https://www.ecfr.gov/current/title-40/chapter-I/subchapter-C/part-63/subpart-Y

## What to download
1) The rule text itself from the eCFR page (use the Developer Tools link).
   - Prefer XML from the Developer Tools options (JSON/HTML/XML are available).
   - If XML is not available, use HTML, then JSON.

2) All Federal Register (FR) documents cited by the rule.
   - From the top "Source: 60 FR 48399..." link.
   - From each section’s trailing source bracket, e.g.:
     "[60 FR 48399, Sept. 19, 1995, as amended at 76 FR 22595, Apr. 21, 2011; 80 FR 75237, Dec. 1, 2015; 85 FR 73892, Nov. 19, 2020]"

3) The proposed rule(s) associated with each final rule.
   - Look inside the final rule for a sentence like "proposed at 84 FR 36304" or a hyperlink.
   - If only a proposal date is given, use the Federal Register date index:
     https://www.federalregister.gov/documents/YYYY/MM/DD
     Then locate the document whose title matches the final rule name
     (for this rule: "National Emission Standards for Marine Tank Vessel Loading Operations").

## How to download FR documents
Use the Federal Register API (avoid landing pages; bot-blocked):
- Search by citation with `/api/v1/documents.json?conditions[term]=<VOL>+FR+<PAGE>`.
- Prefer `full_text_xml_url` for content; fall back to `raw_text_url` if XML is missing.
- Capture `document_number`, `publication_date`, `title`, `type`, and source URLs in the manifest.

## Parsing strategy
- Always capture every FR link present in the eCFR rule text.
- For each final rule document, search for referenced proposed rules and follow them.
- If a referenced FR is not hyperlinked, fall back to the date index + title match.
- Avoid pulling extra materials (supporting or backup docs) for now.

## Suggested folder layout
- data/
- data/ecfr/
- data/ecfr/title-40_part-63_subpart-Y/
- data/ecfr/title-40_part-63_subpart-Y/rule.xml
- data/fr/
- data/fr/60-fr-48399/
- data/fr/60-fr-48399/final-rule.xml
- data/fr/60-fr-48399/proposed-rule.xml
- data/fr/76-fr-22595/final-rule.xml
- data/fr/80-fr-75237/final-rule.xml
- data/fr/85-fr-73892/final-rule.xml

## Script usage and outputs
- Use `download_regs.py` to pull the eCFR rule, all cited final FRs, and proposed FRs.
- A run writes/updates `data/manifest.json` with downloaded file paths and metadata.
- Optional batch config:
  - JSON file with `rules` array of objects:
    - `url` (required), `title` (optional), `out_dir` (optional).
  - Example:
    - {"rules":[{"url":"https://www.ecfr.gov/current/title-40/chapter-I/subchapter-C/part-63/subpart-Y","title":"National Emission Standards for Marine Tank Vessel Loading Operations","out_dir":"data"}]}

## CLI workflow (preferred)
- Use `regpuller_cli.py` for all tasks (rule/FR download, Regulations.gov attachments, prompt building).
- Rule/FR download: `python regpuller_cli.py rule --url <ecfr_url> --out-dir data`
- Regulations.gov download: `python regpuller_cli.py reggov --docket <docket_id> --keywords "Technical Support Document, Response to Comments" --api-key <key>`
- Prompt build: `python regpuller_cli.py prompt --context-folder <folder> --question "<question>"`
- Streamlit (`app.py`) remains optional; avoid relying on it for CLI workflows.
- eCFR-only: `python ecfr_cli.py download --url <ecfr_url> --out-dir data`
- eCFR precedents: `python ecfr_cli.py precedents --rule-xml <path>`
- FR-only: `python fr_cli.py --citations "60 FR 48399, 84 FR 36304" --out-dir data`

## Regulations.gov downloads
- Use `https://api.regulations.gov/v4/documents` with `filter[docketId]` and `filter[searchTerm]`.
- For each document, call `GET /documents/{documentId}?include=attachments` and download attachment `fileFormats[].fileUrl`.
- Match keywords against both document titles and attachment titles.
- Download only PDF or TXT attachments for now.
</INSTRUCTIONS>
