# ProposalBuilder Agent Guidance

## Purpose
- Primary goal: help generate high-quality proposal content using RAG over local context.
- Output sections: Introduction / Understanding of the Project, Scope of Work, Service Assumptions, Schedule, Project Team, Budget, Service Agreement, Closing.

## Repo overview
- App entrypoint: `app.py`
- Default context folder: `context/` (relative to repo root)
- Cache location: `.rag_cache/` under each context folder

## Workflow
- Run locally: `streamlit run app.py`
- Use the app to build query prompts and paste into the LLM of choice.
- Prefer reusing cached indexes unless explicitly forced.

## RAG behavior
- Supported file types: `.txt`, `.md`, `.pdf`, `.docx`
- Subfolders under `context/` are included.
- Avoid changing or deleting `.rag_cache/` unless explicitly requested.

## Content and tone
- Prioritize clarity, specificity, and alignment with client needs.
- Use consistent, professional tone appropriate for formal proposals.
- If output is missing details, call out gaps explicitly.

## Editing rules
- Do not delete or modify files in `context/` unless asked.
- Keep changes minimal and explain when new UI options or retrieval logic are added.

## Validation
- If UI changes are made, confirm they load without errors and the sidebar options appear.
- If caching logic changes, verify that a second run reuses the cache.

## Open questions / escalation
- Ask for clarification if the requested change might alter proposal content structure or required sections.
