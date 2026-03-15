import os, re, time, json, uuid, pickle, hashlib, math, io
from dataclasses import dataclass
from typing import List, Tuple, Dict, Iterable, Optional

import streamlit as st
from pypdf import PdfReader, PdfWriter
import docx
import streamlit.components.v1 as components
import numpy as np
try:
    from rank_bm25 import BM25Okapi
except Exception:
    BM25Okapi = None
try:
    import pytesseract
    from pdf2image import convert_from_path
except Exception:
    pytesseract = None
    convert_from_path = None
try:
    from sentence_transformers import SentenceTransformer
except Exception:
    SentenceTransformer = None
try:
    import hnswlib
except Exception:
    hnswlib = None

CHUNK_CHARS = 1200
CONTEXT_TOKENS = 128000
EST_TOKENS_PER_CHAR = 0.25
PROMPT_OVERHEAD_TOKENS = 800

# To run: streamlit run C:\Users\aaw\OneDrive - Barr Engineering Co\RAG\app.py
# or streamlit run app.py

# ----------------------------
# Document loading + caching
# ----------------------------

def read_txt(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()

def read_pdf(path: str) -> str:
    reader = PdfReader(path)
    out = []
    for i, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        if text.strip():
            out.append(text)
    return "\n".join(out)

def read_docx(path: str) -> str:
    d = docx.Document(path)
    return "\n".join(p.text for p in d.paragraphs if p.text.strip())

@dataclass
class DocEntry:
    path: str
    name: str
    rel: str
    summary: str
    chunks: List[str]
    summary_emb: Optional[List[float]] = None
    chunk_embs: Optional[List[List[float]]] = None

def _cache_path(folder: str) -> str:
    return os.path.join(folder, ".rag_cache", "index.pkl")

def _file_hash(path: str) -> str:
    h = hashlib.md5()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

def _make_summary(text: str, max_chars: int = 2000) -> str:
    cleaned = re.sub(r"\s+", " ", text).strip()
    return cleaned[:max_chars]

def _ocr_output_path(path: str) -> str:
    root, ext = os.path.splitext(path)
    return f"{root}_OCR{ext}"

def _is_ocr_pdf(path: str) -> bool:
    return path.lower().endswith("_ocr.pdf")

def _pdf_needs_ocr(path: str, min_chars: int = 40, min_text_ratio: float = 0.3) -> bool:
    try:
        reader = PdfReader(path)
        total = len(reader.pages)
        if total == 0:
            return False
        with_text = 0
        for page in reader.pages:
            text = (page.extract_text() or "").strip()
            if len(text) >= min_chars:
                with_text += 1
        return (with_text / total) < min_text_ratio
    except Exception:
        return False

def _ocr_pdf_to_searchable(path: str, output_path: str, dpi: int = 300) -> bool:
    if pytesseract is None or convert_from_path is None:
        return False
    try:
        images = convert_from_path(path, dpi=dpi)
        writer = PdfWriter()
        for img in images:
            pdf_bytes = pytesseract.image_to_pdf_or_hocr(img, extension="pdf")
            page_reader = PdfReader(io.BytesIO(pdf_bytes))
            for page in page_reader.pages:
                writer.add_page(page)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "wb") as f:
            writer.write(f)
        return True
    except Exception:
        return False

def estimate_tokens(text: str) -> int:
    return int(math.ceil(len(text) * EST_TOKENS_PER_CHAR))

def max_chunks_for_context() -> int:
    avg_chunk_tokens = int(CHUNK_CHARS * EST_TOKENS_PER_CHAR)
    available = max(CONTEXT_TOKENS - PROMPT_OVERHEAD_TOKENS, avg_chunk_tokens)
    return max(1, available // avg_chunk_tokens)

def _load_cache(folder: str) -> Dict[str, Dict[str, str]]:
    path = _cache_path(folder)
    if not os.path.exists(path):
        return {"version": 1, "entries": {}}
    try:
        with open(path, "rb") as f:
            data = pickle.load(f)
        if isinstance(data, dict) and "entries" in data:
            return data
    except Exception:
        pass
    return {"version": 1, "entries": {}}

def _save_cache(folder: str, cache: Dict[str, Dict[str, str]]) -> None:
    path = _cache_path(folder)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        pickle.dump(cache, f)

def load_documents_cached(folder: str, enable_ocr: bool = False) -> Tuple[List[DocEntry], Dict[str, Dict[str, str]]]:
    cache = _load_cache(folder)
    entries = cache.get("entries", {})
    new_entries: Dict[str, Dict[str, str]] = {}
    docs: List[DocEntry] = []
    for root, _, files in os.walk(folder):
        for fn in files:
            path = os.path.join(root, fn)
            ext = os.path.splitext(fn.lower())[1]
            if ext not in [".txt", ".md", ".pdf", ".docx"]:
                continue
            if ext == ".pdf" and _is_ocr_pdf(path):
                continue
            rel = os.path.relpath(path, folder)
            try:
                fhash = _file_hash(path)
                cached = entries.get(rel)
                use_cached = cached and cached.get("hash") == fhash
                if ext == ".pdf" and enable_ocr:
                    use_cached = use_cached and cached.get("ocr_ready") is True
                if use_cached:
                    summary = cached.get("summary", "")
                    chunks = cached.get("chunks", [])
                    summary_emb = cached.get("summary_emb")
                    chunk_embs = cached.get("chunk_embs")
                    ocr_used = cached.get("ocr_used", False)
                else:
                    if ext in [".txt", ".md"]:
                        text = read_txt(path)
                    elif ext == ".pdf":
                        ocr_used = False
                        if enable_ocr and _pdf_needs_ocr(path):
                            ocr_path = _ocr_output_path(path)
                            if _ocr_pdf_to_searchable(path, ocr_path):
                                text = read_pdf(ocr_path)
                                ocr_used = True
                            else:
                                text = read_pdf(path)
                        else:
                            text = read_pdf(path)
                    else:
                        text = read_docx(path)
                    chunks = chunk_text(text)
                    summary = _make_summary(text)
                    summary_emb = None
                    chunk_embs = None
                new_entries[rel] = {
                    "hash": fhash,
                    "summary": summary,
                    "chunks": chunks,
                    "summary_emb": summary_emb,
                    "chunk_embs": chunk_embs,
                    "ocr_ready": (enable_ocr and ext == ".pdf"),
                    "ocr_used": ocr_used if ext == ".pdf" else False,
                }
                docs.append(
                    DocEntry(
                        path=path,
                        name=os.path.basename(path),
                        rel=rel,
                        summary=summary,
                        chunks=chunks,
                        summary_emb=summary_emb,
                        chunk_embs=chunk_embs,
                    )
                )
            except Exception:
                # skip unreadable files
                continue
    _save_cache(folder, {"version": 1, "entries": new_entries})
    return docs, {"version": 1, "entries": new_entries}

# ----------------------------
# Chunking + Retrieval (simple BM25-like)
# ----------------------------

STOPWORDS = set("""
a an the and or but if then else when while of for to in on at from by with without as is are was were be been being
this that these those it its it's i you we they he she them his her our your their not no yes do does did done
""".split())

def tokenize(text: str) -> List[str]:
    tokens = re.findall(r"[a-zA-Z0-9]+", text.lower())
    return [t for t in tokens if t not in STOPWORDS and len(t) > 1]

def chunk_text(text: str, chunk_chars: int = CHUNK_CHARS, overlap: int = 150) -> List[str]:
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        return []
    chunks = []
    i = 0
    while i < len(text):
        j = min(len(text), i + chunk_chars)
        chunks.append(text[i:j])
        i = max(i + chunk_chars - overlap, j)
    return chunks

@dataclass
class Chunk:
    doc_id: int
    source: str
    idx: int
    text: str
    tf: Dict[str, int]

def build_chunk_index(
    docs: List[DocEntry],
    selected_doc_idxs: Iterable[int] = None,
    include_embeddings: bool = False,
) -> Tuple[List[Chunk], List[List[float]]]:
    chunks: List[Chunk] = []
    chunk_embs: List[List[float]] = []
    selected = set(selected_doc_idxs) if selected_doc_idxs is not None else None
    for doc_idx, doc in enumerate(docs):
        if selected is not None and doc_idx not in selected:
            continue
        for i, ch in enumerate(doc.chunks):
            toks = tokenize(ch)
            tf: Dict[str, int] = {}
            for t in toks:
                tf[t] = tf.get(t, 0) + 1
            chunks.append(Chunk(doc_id=doc_idx, source=doc.name, idx=i, text=ch, tf=tf))
            if include_embeddings and doc.chunk_embs and i < len(doc.chunk_embs):
                chunk_embs.append(doc.chunk_embs[i])
            elif include_embeddings:
                chunk_embs.append([])
    return chunks, chunk_embs

def score_overlap(query_tokens: List[str], chunk: Chunk) -> float:
    # Simple weighted overlap (not full BM25, but works well enough as a starter)
    score = 0.0
    for t in query_tokens:
        score += (1.5 if t in chunk.tf else 0.0) + min(chunk.tf.get(t, 0), 3) * 0.3
    return score

def retrieve(chunks: List[Chunk], query: str, top_k: int = 6) -> List[Tuple[float, Chunk]]:
    qtoks = tokenize(query)
    scored = [(score_overlap(qtoks, ch), ch) for ch in chunks]
    scored.sort(key=lambda x: x[0], reverse=True)
    return [(s, ch) for (s, ch) in scored if s > 0][:top_k]

@st.cache_resource
def _get_embedder():
    if SentenceTransformer is None:
        return None
    return SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def _embed_texts(embedder, texts: List[str], batch_size: int = 32) -> List[List[float]]:
    try:
        embs = embedder.encode(texts, batch_size=batch_size, show_progress_bar=False, normalize_embeddings=True)
        return [e.tolist() for e in embs]
    except TypeError:
        embs = embedder.encode(texts, batch_size=batch_size, show_progress_bar=False)
        embs = np.asarray(embs, dtype=np.float32)
        norms = np.linalg.norm(embs, axis=1, keepdims=True) + 1e-12
        embs = embs / norms
        return [e.tolist() for e in embs]

def ensure_embeddings(docs: List[DocEntry], cache: Dict[str, Dict[str, str]], folder: str, embedder) -> None:
    if embedder is None:
        return
    entries = cache.get("entries", {})
    updated = False
    for doc in docs:
        entry = entries.get(doc.rel, {})
        needs_summary = not doc.summary_emb
        needs_chunks = not doc.chunk_embs or len(doc.chunk_embs) != len(doc.chunks)
        if needs_summary:
            doc.summary_emb = _embed_texts(embedder, [doc.summary])[0]
            entry["summary_emb"] = doc.summary_emb
            updated = True
        if needs_chunks:
            doc.chunk_embs = _embed_texts(embedder, doc.chunks)
            entry["chunk_embs"] = doc.chunk_embs
            updated = True
        entries[doc.rel] = entry
    if updated:
        cache["entries"] = entries
        _save_cache(folder, cache)

def _dense_scores(embs: List[List[float]], query_emb: np.ndarray, top_k: int) -> Tuple[List[int], List[float]]:
    if not embs:
        return [], []
    vecs = np.asarray(embs, dtype=np.float32)
    if hnswlib is not None and len(vecs) > 2000:
        dim = vecs.shape[1]
        index = hnswlib.Index(space="cosine", dim=dim)
        index.init_index(max_elements=len(vecs), ef_construction=200, M=16)
        index.add_items(vecs, ids=np.arange(len(vecs)))
        index.set_ef(min(200, len(vecs)))
        labels, distances = index.knn_query(query_emb.astype(np.float32), k=min(top_k, len(vecs)))
        labels = labels[0].tolist()
        sims = (1.0 - distances[0]).tolist()
        return labels, sims
    sims = np.dot(vecs, query_emb)
    ranked = np.argsort(-sims)
    top = ranked[: min(top_k, len(vecs))]
    return top.tolist(), sims[top].tolist()

def _rrf_merge(sparse_scores: List[float], dense_ranks: Dict[int, int], k: int = 60) -> List[float]:
    scores: List[float] = []
    sparse_ranked = sorted(range(len(sparse_scores)), key=lambda i: sparse_scores[i], reverse=True)
    sparse_rank = {idx: rank for rank, idx in enumerate(sparse_ranked, start=1) if sparse_scores[idx] > 0}
    for i in range(len(sparse_scores)):
        s = 0.0
        if i in sparse_rank:
            s += 1.0 / (k + sparse_rank[i])
        if i in dense_ranks:
            s += 1.0 / (k + dense_ranks[i])
        scores.append(s)
    return scores

def retrieve_docs(docs: List[DocEntry], query: str, top_k: int, embedder=None) -> List[int]:
    if not docs:
        return []
    qtoks = tokenize(query)
    summaries = [doc.summary for doc in docs]
    if BM25Okapi is not None:
        corpus = [tokenize(s) for s in summaries]
        bm25 = BM25Okapi(corpus)
        scores = bm25.get_scores(qtoks)
    else:
        scores = [score_overlap(qtoks, Chunk(doc_id=-1, source="", idx=0, text=s, tf={t: 1 for t in tokenize(s)})) for s in summaries]
    if embedder is None:
        ranked = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)
        return ranked[:top_k]
    query_emb = np.asarray(_embed_texts(embedder, [query])[0], dtype=np.float32)
    doc_embs = [doc.summary_emb or [] for doc in docs]
    dense_idxs, _ = _dense_scores(doc_embs, query_emb, top_k=len(docs))
    dense_rank = {idx: rank for rank, idx in enumerate(dense_idxs, start=1)}
    merged = _rrf_merge(list(scores), dense_rank)
    ranked = sorted(range(len(merged)), key=lambda i: merged[i], reverse=True)
    return ranked[:top_k]

def score_chunks(chunks: List[Chunk], chunk_embs: List[List[float]], query: str, embedder=None) -> List[float]:
    qtoks = tokenize(query)
    sparse_scores = [score_overlap(qtoks, ch) for ch in chunks]
    if embedder is None or not chunk_embs:
        return sparse_scores
    query_emb = np.asarray(_embed_texts(embedder, [query])[0], dtype=np.float32)
    dense_idxs, _ = _dense_scores(chunk_embs, query_emb, top_k=len(chunks))
    dense_rank = {idx: rank for rank, idx in enumerate(dense_idxs, start=1)}
    return _rrf_merge(sparse_scores, dense_rank)

def retrieve_hybrid(chunks: List[Chunk], chunk_embs: List[List[float]], query: str, top_k: int, embedder=None) -> List[Tuple[float, Chunk]]:
    scores = score_chunks(chunks, chunk_embs, query, embedder=embedder)
    scored = [(s, ch) for s, ch in zip(scores, chunks)]
    scored.sort(key=lambda x: x[0], reverse=True)
    return [(s, ch) for (s, ch) in scored if s > 0][:top_k]

def retrieve_with_coverage(
    chunks: List[Chunk],
    chunk_embs: List[List[float]],
    query: str,
    top_k: int,
    embedder=None,
    min_per_doc: int = 1,
) -> List[Tuple[float, Chunk]]:
    if not chunks:
        return []
    scores = score_chunks(chunks, chunk_embs, query, embedder=embedder)
    doc_ids = sorted({ch.doc_id for ch in chunks})
    selected = set()
    for doc_id in doc_ids:
        indices = [i for i, ch in enumerate(chunks) if ch.doc_id == doc_id]
        if not indices:
            continue
        indices.sort(key=lambda i: scores[i], reverse=True)
        for i in indices[:min_per_doc]:
            selected.add(i)
    if len(selected) < top_k:
        ranked = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)
        for i in ranked:
            if i in selected:
                continue
            selected.add(i)
            if len(selected) >= top_k:
                break
    ordered = sorted(selected, key=lambda i: scores[i], reverse=True)
    return [(scores[i], chunks[i]) for i in ordered[:top_k]]

# ----------------------------
# Prompt packaging
# ----------------------------

def build_query_txt(job_id: str, question: str, selected: List[Tuple[float, Chunk]], source_folder: str) -> str:
    header = {
        "job_id": job_id,
        "created_local": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "top_k": len(selected),
        "source_folder": source_folder,
    }

    lines = [json.dumps(header)]
    lines += ["", "### USER_QUESTION", question.strip(), "", "### RAG_CONTEXT"]
    for n, (score, ch) in enumerate(selected, start=1):
        lines.append(f"[{n}] (file={ch.source}, chunk={ch.idx}, score={score:.2f})")
        lines.append(ch.text)
        lines.append("")
    lines += [
        "### INSTRUCTIONS",
        "- Answer using the context when relevant.",
        "- If the context is insufficient, say what's missing.",
        "- Cite context chunks like [1], [2] when you rely on them.",
    ]
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
    max_chunks_cap = max(2, max_chunks_for_context())
    top_k = st.slider("Top-K context chunks", 2, max_chunks_cap, min(6, max_chunks_cap))
    use_dense = st.checkbox("Use dense retrieval (embeddings)", value=True)
    enable_ocr = st.checkbox("Auto-OCR scanned PDFs", value=False)
    ensure_coverage = st.checkbox("Ensure coverage across documents", value=True)
    min_per_doc = st.slider("Min chunks per document", 1, 3, 1, disabled=not ensure_coverage)
    st.caption(f"Context window: {CONTEXT_TOKENS} tokens (est. max chunks: {max_chunks_cap})")

st.subheader("1) Select your local context folder")
context_folder = st.text_input("Context folder (local)", value=os.getcwd())

st.subheader("2) Ask a question")
question = st.text_area("Question", height=120, placeholder="Type your question here...")

run = st.button("Build query prompt", type="primary", disabled=not (question.strip() and os.path.isdir(context_folder)))

if run:
    job_id = str(uuid.uuid4())[:8]

    with st.status("Indexing and retrieving context...", expanded=False):
        ocr_available = enable_ocr and pytesseract is not None and convert_from_path is not None
        if enable_ocr and not ocr_available:
            st.warning("OCR is enabled but pytesseract/pdf2image are not installed.")
        docs, cache = load_documents_cached(context_folder, enable_ocr=ocr_available)
        embedder = _get_embedder() if use_dense else None
        if use_dense and embedder is None:
            st.warning("Dense retrieval is enabled but sentence-transformers is not installed.")
        ensure_embeddings(docs, cache, context_folder, embedder)
        if ensure_coverage and len(docs) > 300:
            st.warning("Coverage mode is enabled; large folders may be slow to process.")
        if ensure_coverage and top_k < len(docs):
            st.warning("Top-K is smaller than the document count; not all documents can be included.")
        if ensure_coverage:
            selected_doc_idxs = list(range(len(docs)))
        else:
            doc_top_k = min(max(top_k * 4, 10), len(docs))
            selected_doc_idxs = retrieve_docs(docs, question, top_k=doc_top_k, embedder=embedder)
        chunks, chunk_embs = build_chunk_index(docs, selected_doc_idxs, include_embeddings=embedder is not None)
        if ensure_coverage:
            selected = retrieve_with_coverage(
                chunks,
                chunk_embs,
                question,
                top_k=top_k,
                embedder=embedder,
                min_per_doc=min_per_doc,
            )
        else:
            selected = retrieve_hybrid(chunks, chunk_embs, question, top_k=top_k, embedder=embedder)

    query_txt = build_query_txt(job_id, question, selected, context_folder)
    est_tokens = estimate_tokens(query_txt)
    if est_tokens > CONTEXT_TOKENS and selected:
        trimmed = list(selected)
        while len(trimmed) > 1:
            trimmed = trimmed[:-1]
            query_txt = build_query_txt(job_id, question, trimmed, context_folder)
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
