import os, json, uuid, time
from typing import List, Tuple

import streamlit as st
import streamlit.components.v1 as components

import download_regs
import download_regulations_gov

from indexing import (
    CONTEXT_TOKENS,
    Chunk,
    DocEntry,
    build_chunk_index,
    ensure_embeddings,
    estimate_tokens,
    get_embedder,
    load_documents_cached,
    max_chunks_for_context,
    retrieve_docs,
    retrieve_hybrid,
    retrieve_with_coverage,
)
from io_utils import (
    convert_from_path,
    pytesseract,
)

# To run: streamlit run C:\Users\aaw\OneDrive - Barr Engineering Co\RAG\app.py
# or streamlit run app.py

# ----------------------------
# Prompt packaging
# ----------------------------

@st.cache_resource
def _get_embedder():
    return get_embedder()

def build_query_txt(
    job_id: str,
    question: str,
    selected: List[Tuple[float, Chunk]],
    source_folder: str,
    include_citations: bool = True,
) -> str:
    header = {
        "job_id": job_id,
        "created_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "top_k": len(selected),
        "source_folder": source_folder,
    }

    lines = [json.dumps(header)]
    lines += ["", "### USER_QUESTION", question.strip(), ""]
    n = 1
    lines += ["### RAG_CONTEXT"]
    for score, ch in selected:
        if include_citations:
            lines.append(f"[{n}] (file={ch.source}, chunk={ch.idx}, score={score:.2f})")
        else:
            lines.append(f"(source={ch.source}, chunk={ch.idx}, score={score:.2f})")
        lines.append(ch.text)
        lines.append("")
        n += 1
    lines += [
        "### INSTRUCTIONS",
        "- Answer using the context when relevant.",
        "- If the context is insufficient, say what's missing.",
    ]
    if include_citations:
        lines.append("- Cite context chunks like [1], [2] when you rely on them.")
        lines.append(
            "- Append a References section that lists each cited chunk number with its filename."
        )
    return "\n".join(lines).strip() + "\n"

def render_copy_button(text: str) -> None:
    # Streamlit doesn't include a native clipboard helper; use a small JS shim.
    safe_text = json.dumps(text)
    components.html(
        f"""
        <button id="copy-btn" style="padding:0.4rem 0.8rem;">Copy query to clipboard</button>
        <script>
        const btn = document.getElementById("copy-btn");
        btn.addEventListener("click", async () => {{
            const text = {safe_text};
            try {{
                await navigator.clipboard.writeText(text);
                btn.textContent = "Copied!";
                setTimeout(() => (btn.textContent = "Copy query to clipboard"), 1500);
            }} catch (err) {{
                btn.textContent = "Copy failed";
                setTimeout(() => (btn.textContent = "Copy query to clipboard"), 1500);
            }}
        }});
        </script>
        """,
        height=48,
    )

# ----------------------------
# Streamlit UI
# ----------------------------

st.set_page_config(page_title="RAG Prompt Builder", layout="wide")
st.title("RAG Prompt Builder")

with st.sidebar:
    max_chunks_cap = min(125, max(2, max_chunks_for_context()))
    top_k = st.slider("Top-K context chunks", 2, max_chunks_cap, min(6, max_chunks_cap))
    use_dense = st.checkbox("Use dense retrieval (embeddings)", value=True)
    enable_ocr = st.checkbox("Auto-OCR scanned PDFs", value=False)
    ensure_coverage = st.checkbox("Ensure coverage across documents", value=True)
    force_reindex = st.checkbox("Force reindex (ignore cached index)", value=False)
    include_citations = st.checkbox("Include chunk citations in prompt", value=True)
    min_per_doc = st.slider("Min chunks per document", 1, 3, 1, disabled=not ensure_coverage)
    st.caption(f"Context window: {CONTEXT_TOKENS} tokens (est. max chunks: {max_chunks_cap})")

if "context_folder" not in st.session_state:
    st.session_state.context_folder = os.path.join(os.getcwd(), "data")
if "ecfr_date" not in st.session_state:
    st.session_state.ecfr_date = ""
if "reggov_downloads" not in st.session_state:
    st.session_state.reggov_downloads = []
if "docket_ids" not in st.session_state:
    st.session_state.docket_ids = []
if "docket_sources" not in st.session_state:
    st.session_state.docket_sources = []

st.subheader("1) Download rule documents (optional)")
rule_url = st.text_input(
    "Rule URL",
    value="https://www.ecfr.gov/current/title-40/chapter-I/subchapter-C/part-63/subpart-Y",
)
download_out_dir = st.text_input(
    "Download output folder",
    value=os.path.join(os.getcwd(), "data"),
)
rule_title_override = st.text_input("Rule title override (optional)", value="")
download_clicked = st.button("Download rule files")
if download_clicked:
    if not rule_url.strip():
        st.warning("Please enter a rule URL.")
    else:
        with st.status("Downloading rule and FR documents...", expanded=False):
            hierarchy = download_regs.parse_ecfr_hierarchy(rule_url.strip())
            ecfr_date = ""
            if hierarchy.get("title"):
                ecfr_date = download_regs.get_ecfr_title_date(hierarchy["title"]) or ""
            entry = download_regs.run_download(
                rule_url.strip(),
                download_out_dir.strip(),
                rule_title_override.strip(),
            )
        errors = entry.get("errors") or []
        rule_dir = entry.get("rule_dir", "")
        if errors:
            st.warning("Download completed with errors: " + "; ".join(errors))
        if rule_dir:
            st.session_state.context_folder = rule_dir
            st.session_state.ecfr_date = ecfr_date
            st.success(f"Downloads saved under: {rule_dir}")
        st.session_state.docket_ids = entry.get("docket_ids") or []
        st.session_state.docket_sources = entry.get("docket_sources") or []
        prov_path = entry.get("fr_provenance_path")
        if not prov_path:
            candidates = [
                os.path.join(download_out_dir.strip() or "data", "fr_provenance.md"),
                os.path.join(rule_dir or "", "fr_provenance.md"),
                os.path.join(os.getcwd(), "fr_provenance.md"),
            ]
            for candidate in candidates:
                if candidate and os.path.exists(candidate):
                    prov_path = candidate
                    break
        if not prov_path:
            fallback_path = os.path.join(download_out_dir.strip() or "data", "fr_provenance.md")
            try:
                download_regs.write_fr_provenance_markdown(fallback_path, entry)
                prov_path = fallback_path
            except Exception as exc:
                st.warning(f"Failed to write fr_provenance.md: {exc}")
                prov_path = ""
        if prov_path and os.path.exists(prov_path):
            st.subheader("FR provenance")
            with open(prov_path, "r", encoding="utf-8") as f:
                st.markdown(f.read())
        elif entry.get("fr_provenance"):
            st.subheader("FR provenance")
            st.markdown("Provenance file not found; showing in-memory summary.")
            st.markdown("\n".join([str(p) for p in entry.get("fr_provenance") or []]))
        else:
            st.warning("No FR provenance data available for this run.")
        summary_checks = entry.get("fr_summary_checks") or []
        if summary_checks:
            st.subheader("FR summary match check")
            missing = [item for item in summary_checks if not item.get("matched")]
            filtered = [item for item in summary_checks if item.get("filtered")]
            if missing:
                st.warning(f"{len(missing)} FR document(s) missing summary match.")
            if filtered:
                st.warning(f"{len(filtered)} FR document(s) filtered out by summary match.")
            st.write(
                [
                    f"{item.get('citation')} ({item.get('role')}): "
                    + (
                        "filtered"
                        if item.get("filtered")
                        else ("matched" if item.get("matched") else "missing")
                    )
                    + (
                        f" ({item.get('keywords_missing')}/{item.get('keywords_total')} missing)"
                        if item.get("keywords_total")
                        else ""
                    )
                    + (f" | {item.get('matched_phrase')}" if item.get('matched_phrase') else "")
                    for item in summary_checks
                ]
            )
if st.session_state.ecfr_date:
    st.caption(f"eCFR date used: {st.session_state.ecfr_date}")

st.subheader("2) Download Regulations.gov attachments (optional)")
if st.session_state.docket_ids:
    if st.session_state.docket_sources:
        st.markdown("Docket ID sources:")
        st.write(
            [
                f"{item.get('docket_id')}: {', '.join(item.get('citations') or [])}"
                for item in st.session_state.docket_sources
            ]
        )
else:
    st.caption("No docket IDs extracted yet. Run step 1 to populate this list.")
reggov_docket = st.text_input("Docket ID", value="")
reggov_keywords = st.text_input(
    "Title keywords (comma-separated)",
    value="Technical Support Document, Response to Comments, Regulatory Impacts Analysis",
)
reggov_api_key = st.text_input(
    "Regulations.gov API key (X-Api-Key)",
    value=os.environ.get("REGGOV_API_KEY", "4iAEDZhA1V9aTGaq4LKfEQDHQUcBcfo4t7YVcBuy"),
    type="password",
)
reggov_out_dir = st.text_input(
    "Regulations.gov output folder",
    value=os.path.join(os.getcwd(), "data"),
)
reggov_clicked = st.button("Download Regulations.gov files")
if reggov_clicked:
    if not reggov_docket.strip():
        st.warning("Please enter a docket ID.")
    elif not reggov_api_key.strip():
        st.warning("Please enter your Regulations.gov API key.")
    else:
        keywords = [k.strip() for k in reggov_keywords.split(",") if k.strip()]
        with st.status("Downloading Regulations.gov attachments...", expanded=False):
            downloads = download_regulations_gov.download_docket_attachments(
                reggov_docket.strip(),
                keywords,
                reggov_out_dir.strip(),
                reggov_api_key.strip(),
                allowed_formats=("pdf", "txt"),
            )
        st.session_state.reggov_downloads = downloads
        if downloads:
            st.success(f"Downloaded {len(downloads)} file(s).")
        else:
            st.warning("No matching attachments found.")
if st.session_state.reggov_downloads:
    st.subheader("Regulations.gov downloaded files")
    st.write([item.get("path") for item in st.session_state.reggov_downloads if item.get("path")])

st.subheader("3) Select your local context folder")
context_folder = st.text_input(
    "Context folder (local)",
    value=st.session_state.context_folder,
)

st.subheader("4) Ask a question")
question = st.text_area("Question", height=120, placeholder="Type your question here...")

run = st.button("Build query prompt", type="primary", disabled=not (question.strip() and os.path.isdir(context_folder)))

if run:
    job_id = str(uuid.uuid4())[:8]

    with st.status("Indexing and retrieving context...", expanded=False):
        progress = st.progress(0.0)
        def _progress(done: int, total: int, label: str) -> None:
            if total <= 0:
                progress.progress(0.0, text=label)
                return
            progress.progress(min(done / total, 1.0), text=label)
        ocr_available = enable_ocr and pytesseract is not None and convert_from_path is not None
        if enable_ocr and not ocr_available:
            st.warning("OCR is enabled but pytesseract/pdf2image are not installed.")
        docs, cache = load_documents_cached(
            context_folder,
            enable_ocr=ocr_available,
            force_reindex=force_reindex,
            progress_cb=_progress,
        )
        meta = cache.get("meta", {})
        if meta.get("last_indexed"):
            st.caption(f"Last indexed: {meta.get('last_indexed')}")
        if meta.get("new_files_detected") is not None:
            st.caption(f"New files detected: {meta.get('new_files_detected')}")
        failed_files = meta.get("failed_files") or []
        if failed_files:
            shown = failed_files[:10]
            more = len(failed_files) - len(shown)
            msg = "Failed to index (cached): " + ", ".join(shown)
            if more > 0:
                msg += f" (+{more} more)"
            st.warning(msg)
        embedder = _get_embedder() if use_dense else None
        if use_dense and embedder is None:
            st.warning("Dense retrieval is enabled but sentence-transformers is not installed.")
        ensure_embeddings(docs, cache, context_folder, embedder)
        if ensure_coverage and len(docs) > 300:
            st.warning("Coverage mode is enabled; large folders may be slow to process.")
        if ensure_coverage and top_k < len(docs):
            st.warning("Top-K is smaller than the document count; not all documents can be included.")
        retrieval_query = question
        if ensure_coverage:
            selected_doc_idxs = list(range(len(docs)))
        else:
            doc_top_k = min(max(top_k * 4, 10), len(docs))
            selected_doc_idxs = retrieve_docs(docs, retrieval_query, top_k=doc_top_k, embedder=embedder)
        progress.progress(0.85, text="Building retrieval index...")
        chunks, chunk_embs = build_chunk_index(docs, selected_doc_idxs, include_embeddings=embedder is not None)
        if ensure_coverage:
            selected = retrieve_with_coverage(
                chunks,
                chunk_embs,
                retrieval_query,
                top_k=top_k,
                embedder=embedder,
                min_per_doc=min_per_doc,
            )
        else:
            selected = retrieve_hybrid(chunks, chunk_embs, retrieval_query, top_k=top_k, embedder=embedder)
        progress.progress(1.0, text="Done")

    query_txt = build_query_txt(
        job_id,
        question,
        selected,
        context_folder,
        include_citations=include_citations,
    )
    est_tokens = estimate_tokens(query_txt)
    if est_tokens > CONTEXT_TOKENS and selected:
        trimmed = list(selected)
        while len(trimmed) > 1:
            trimmed = trimmed[:-1]
            query_txt = build_query_txt(
                job_id,
                question,
                trimmed,
                context_folder,
                include_citations=include_citations,
            )
            est_tokens = estimate_tokens(query_txt)
            if est_tokens <= CONTEXT_TOKENS:
                selected = trimmed
                break
        if est_tokens > CONTEXT_TOKENS:
            st.warning("Estimated tokens exceed the 128k context window; consider reducing Top-K.")

    st.subheader("Query Prompt")
    st.caption(f"Estimated prompt size: {est_tokens} tokens (context window: {CONTEXT_TOKENS})")
    st.text_area("prompt", value=query_txt, height=300)
    render_copy_button(query_txt)
    st.code(query_txt[:4000] + ("\n...\n" if len(query_txt) > 4000 else ""), language="text")
