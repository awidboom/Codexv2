---
name: pic-nomcom-eval
description: "Evaluate a PIC/Principal VP candidate’s folder against the 8 criteria (A1-A4, P1-P4) in their ‘Principal VP Evaluation Form’. Use when asked to write or update `Candidate X/Assessment.md`, summarize per-criterion supporting evidence/gaps/contradictions, and cross-check supporting documents (meeting notes, feedback PDFs/DOCX, surveys/XLSX, LFAR/XLSX, slide decks/PPTX) for consistency—while following the evidence expectations in `README.md` (e.g., contracting and leverage guidance)."
---

# PIC-NomCom-Eval

## Overview

Produce a candidate assessment that is traceable to source files: for each criterion, summarize (1) what the evaluation form claims, (2) what the supporting docs corroborate, (3) what is missing, and (4) what conflicts or needs clarification.

## Workflow

### Step 0: Align to repo guidance

- Read `README.md` first and treat its “Notes on Evidence Expectations” as guardrails (e.g., contracting expectations; leverage target range).
- If you need to interpret criteria meaning, prioritize: `officer charter and supporting attachments.docx` and `Principal Vice President role description.docx` (either at repo root or the candidate’s `TemplatesCandidateTools/` copy).

### Step 1: Generate searchable extracts (Office/PDF → text)

In this repo, prefer the built-in extractor so you can reliably search across `.docx`, `.xlsx`, `.pptx`, and `.pdf`:

```powershell
python scripts/extract_candidate_materials.py --input "Candidate X"
```

Confirm it produced:
- `Candidate X/_evalform_extracted.md`
- `Candidate X/_extracted/`

If `_extracted/` already exists, re-run only if files changed (mtime/size) or if you suspect stale extracts.

### Step 2: Build the “criteria map” from the evaluation form

- Use `Candidate X/_evalform_extracted.md` as the canonical criteria ordering and headings.
- Extract the 8 criterion blocks: `A1–A4` and `P1–P4`.
- For each criterion, list the evaluation-form claims you will try to corroborate (numbers, client names, dates, roles, outcomes).

### Step 3: Evidence and contradiction pass (per criterion)

For each criterion:
- **Evaluation-form evidence:** Summarize what the long form asserts (avoid long quotes; paraphrase).
- **Corroboration:** Search `Candidate X/_extracted/` for matching claims (same client names, dates, counts, metrics, outcomes). Prefer corroboration from multiple independent documents when possible (e.g., meeting notes + survey export).
- **Gaps:** Identify what would strengthen the criterion (missing artifacts, unclear definitions, “evaluation-form only” claims, unquantified impact).
- **Contradictions / discrepancies:** Note mismatched counts/dates/metrics, perception mismatches (“no line of sight” vs “well known”), or claims that appear outdated relative to later meeting notes.

When flagging a discrepancy, state:
- the claim as written (short paraphrase),
- the conflicting evidence,
- the exact file paths you used.

### Step 4: Cross-document consistency checks (minimum set)

- **Pulse survey counts:** Cross-check totals across (a) survey XLSX exports, (b) “compare surveys” workbooks, and (c) meeting notes referencing those results.
- **LFAR claims:** Cross-check totals and variance framing against the LFAR export; call out when “minimal variances” depends on aggregation choice (job vs project; $ vs %; exclusions).
- **Development themes:** Confirm that the development areas in meeting notes and feedback align with how the long form frames them (or call out mismatches).

### Step 5: Write `Candidate X/Assessment.md`

Use the template in `skills/pic-nomcom-eval/assets/Assessment.template.md` as a starting point and adapt it as needed.

Required output characteristics:
- Per-criterion sections with: evaluation-form evidence, corroboration, gaps, contradictions.
- A dedicated “Consistency checks” section for surveys/LFAR/development themes.
- A short “Questions NomCom may want to ask” section.
- Reference key sources using clickable file paths (wrap paths in `...`).

## Quick checklist (before finalizing)

- Each non-obvious claim is traceable to at least one file path.
- Any numbers (survey totals, LFAR totals/variance) are cross-checked against an export source.
- Any “absolute” language (“minimal”, “consistently”) is either supported by the exports or softened/qualified.
- The assessment reflects the evidence expectations in `README.md` (especially contracting and leverage framing).
