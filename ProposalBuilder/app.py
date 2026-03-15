import os, json, uuid, time
from typing import List, Tuple

import streamlit as st
import streamlit.components.v1 as components

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
    is_ocr_pdf,
    ocr_output_path,
    ocr_pdf_to_searchable,
    pdf_needs_ocr,
    pytesseract,
    read_docx,
    read_pdf,
    read_txt,
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
    rfp_chunks: List[Chunk] = None,
    rfp_folder: str = "",
    rfp_full_text: str = "",
) -> str:
    header = {
        "job_id": job_id,
        "created_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "top_k": len(selected),
        "source_folder": source_folder,
    }
    if rfp_chunks or rfp_full_text:
        header["rfp_folder"] = rfp_folder
        header["rfp_chunks"] = len(rfp_chunks) if rfp_chunks else 0
        header["rfp_full_text"] = bool(rfp_full_text)

    lines = [json.dumps(header)]
    lines += ["", "### USER_QUESTION", question.strip(), ""]
    n = 1
    if rfp_full_text:
        lines += ["### RFP_CONTEXT", rfp_full_text.strip(), ""]
    elif rfp_chunks:
        lines += ["### RFP_CONTEXT"]
        for ch in rfp_chunks:
            if include_citations:
                lines.append(f"[{n}] (file={ch.source}, chunk={ch.idx}, score=RFP)")
            else:
                lines.append(f"(source={ch.source}, chunk={ch.idx}, score=RFP)")
            lines.append(ch.text)
            lines.append("")
            n += 1
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

def _load_rfp_full_text(folder: str, enable_ocr: bool = False) -> str:
    parts = []
    for root, _, files in os.walk(folder):
        for fn in files:
            path = os.path.join(root, fn)
            ext = os.path.splitext(fn.lower())[1]
            if ext not in [".txt", ".md", ".pdf", ".docx"]:
                continue
            if ext == ".pdf" and is_ocr_pdf(path):
                continue
            try:
                if ext in [".txt", ".md"]:
                    text = read_txt(path)
                elif ext == ".pdf":
                    if enable_ocr and pdf_needs_ocr(path):
                        ocr_path = ocr_output_path(path)
                        if ocr_pdf_to_searchable(path, ocr_path):
                            text = read_pdf(ocr_path)
                        else:
                            text = read_pdf(path)
                    else:
                        text = read_pdf(path)
                else:
                    text = read_docx(path)
            except Exception:
                continue
            if text.strip():
                parts.append(f"## {fn}\n{text.strip()}\n")
    return "\n".join(parts).strip()

st.set_page_config(page_title="RAG Prompt Builder", layout="wide")
st.title("RAG Prompt Builder")

with st.sidebar:
    max_chunks_cap = min(125, max(2, max_chunks_for_context()))
    top_k = st.slider("Top-K context chunks", 2, max_chunks_cap, min(6, max_chunks_cap))
    use_dense = st.checkbox("Use dense retrieval (embeddings)", value=True)
    enable_ocr = st.checkbox("Auto-OCR scanned PDFs", value=False)
    ensure_coverage = st.checkbox("Ensure coverage across documents", value=True)
    force_reindex = st.checkbox("Force reindex (ignore cached index)", value=False)
    allow_missing_sources = st.checkbox(
        "Allow missing source files (use cached text)",
        value=False,
        help="Keeps cached chunks for files that were deleted/moved from disk. Use with care: citations may point to paths that no longer exist.",
    )
    include_citations = st.checkbox("Include chunk citations in prompt", value=True)
    use_rfp_for_retrieval = st.checkbox("Use RFP text to guide retrieval", value=False)
    rfp_query_chars = st.slider("RFP chars for retrieval", 500, 12000, 4000, step=500)
    include_full_rfp = st.checkbox("Include full RFP verbatim", value=False)
    min_per_doc = st.slider("Min chunks per document", 1, 3, 1, disabled=not ensure_coverage)
    st.caption(f"Context window: {CONTEXT_TOKENS} tokens (est. max chunks: {max_chunks_cap})")

st.subheader("1) Select your local context folder")
context_folder = st.text_input("Context folder (local)", value=os.path.join(os.getcwd(), "context"))

st.subheader("2) Select your RFP folder (optional)")
rfp_folder = st.text_input("RFP folder (local)", value=os.path.join(os.getcwd(), "rfp"))

st.subheader("3) Ask a question")
question = st.text_area("Question", height=120, placeholder="Type your question here...")

run = st.button("Build query prompt", type="primary", disabled=not (question.strip() and os.path.isdir(context_folder)))

if run:
    job_id = str(uuid.uuid4())[:8]

    rfp_chunks = []
    rfp_chunk_list = []
    rfp_max_chunks = 0
    rfp_available = False
    rfp_query_text = ""
    rfp_full_text = ""
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
        if rfp_folder and os.path.isdir(rfp_folder):
            rfp_docs, rfp_cache = load_documents_cached(
                rfp_folder,
                enable_ocr=False,
                force_reindex=force_reindex,
                progress_cb=_progress,
            )
            rfp_embedder = _get_embedder() if use_dense else None
            ensure_embeddings(rfp_docs, rfp_cache, rfp_folder, rfp_embedder)
            rfp_doc_idxs = list(range(len(rfp_docs)))
            rfp_chunk_list, _ = build_chunk_index(rfp_docs, rfp_doc_idxs, include_embeddings=False)
            rfp_max_chunks = len(rfp_chunk_list)
            rfp_available = True
            if use_rfp_for_retrieval and rfp_chunk_list:
                parts = []
                total_chars = 0
                for ch in rfp_chunk_list:
                    if total_chars >= rfp_query_chars:
                        break
                    parts.append(ch.text)
                    total_chars += len(ch.text)
                rfp_query_text = "\n".join(parts)
            if include_full_rfp:
                rfp_full_text = _load_rfp_full_text(rfp_folder, enable_ocr=False)
        elif rfp_folder:
            st.warning("RFP folder does not exist; continuing without RFP context.")
        docs, cache = load_documents_cached(
            context_folder,
            enable_ocr=ocr_available,
            force_reindex=force_reindex,
            allow_missing_sources=allow_missing_sources,
            progress_cb=_progress,
        )
        meta = cache.get("meta", {})
        if meta.get("last_indexed"):
            st.caption(f"Last indexed: {meta.get('last_indexed')}")
        if meta.get("last_updated"):
            st.caption(f"Index last updated: {meta.get('last_updated')}")
        if meta.get("new_files_detected") is not None:
            st.caption(f"New files detected: {meta.get('new_files_detected')}")
        if meta.get("total_files_on_disk") is not None and meta.get("total_files_in_index") is not None:
            st.caption(f"Files on disk: {meta.get('total_files_on_disk')} | Files in index: {meta.get('total_files_in_index')}")
        missing_sources = meta.get("missing_source_files") or []
        if missing_sources:
            shown = missing_sources[:10]
            more = len(missing_sources) - len(shown)
            msg = "Missing source files (using cached text): " + ", ".join(shown)
            if more > 0:
                msg += f" (+{more} more)"
            st.warning(msg)
        meta_path = os.path.join(context_folder, ".rag_cache", "index_meta.json")
        if os.path.exists(meta_path):
            st.caption(f"Index metadata file: {meta_path}")
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
        if use_rfp_for_retrieval and rfp_query_text:
            retrieval_query = f"{question.strip()}\n\nRFP:\n{rfp_query_text}"
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

    if rfp_available and not include_full_rfp:
        if rfp_max_chunks == 0:
            st.warning("No RFP chunks found in the selected folder.")
        rfp_limit = st.slider(
            "RFP chunks to include",
            0,
            rfp_max_chunks,
            rfp_max_chunks,
            help="Reduce if the prompt gets too long.",
            key="rfp_chunk_limit",
        )
        rfp_chunks = rfp_chunk_list[:rfp_limit]
    elif rfp_available and include_full_rfp and not rfp_full_text:
        st.warning("No RFP text could be loaded; continuing without RFP context.")

    query_txt = build_query_txt(
        job_id,
        question,
        selected,
        context_folder,
        include_citations=include_citations,
        rfp_chunks=rfp_chunks,
        rfp_folder=rfp_folder,
        rfp_full_text=rfp_full_text,
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
                rfp_chunks=rfp_chunks,
                rfp_folder=rfp_folder,
                rfp_full_text=rfp_full_text,
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
