import os, re, time, json, pickle, hashlib, math, io
from dataclasses import dataclass
from typing import List, Tuple, Dict, Iterable, Optional

import numpy as np

try:
    from pypdf import PdfReader, PdfWriter
except Exception:
    PdfReader = None
    PdfWriter = None

try:
    import docx
except Exception:
    docx = None

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

CACHE_SCHEMA_VERSION = 2
DEFAULT_EMBEDDER_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


# ----------------------------
# Document loading + caching
# ----------------------------

def read_txt(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def read_pdf(path: str) -> str:
    if PdfReader is None:
        raise RuntimeError("pypdf is not installed; cannot read PDFs.")
    reader = PdfReader(path)
    out = []
    for page in reader.pages:
        text = page.extract_text() or ""
        if text.strip():
            out.append(text)
    return "\n".join(out)


def read_docx(path: str) -> str:
    if docx is None:
        raise RuntimeError("python-docx is not installed; cannot read .docx files.")
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


def cache_path(folder: str) -> str:
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


def ocr_available() -> bool:
    return pytesseract is not None and convert_from_path is not None and PdfReader is not None and PdfWriter is not None


def _pdf_needs_ocr(path: str, min_chars: int = 40, min_text_ratio: float = 0.3) -> bool:
    if PdfReader is None:
        return False
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
    if not ocr_available():
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


def _load_cache(folder: str) -> Dict:
    path = cache_path(folder)
    if not os.path.exists(path):
        return {"schema_version": CACHE_SCHEMA_VERSION, "entries": {}}
    try:
        with open(path, "rb") as f:
            cache = pickle.load(f)
        if not isinstance(cache, dict):
            return {"schema_version": CACHE_SCHEMA_VERSION, "entries": {}}
        if "entries" not in cache:
            cache["entries"] = {}
        return cache
    except Exception:
        return {"schema_version": CACHE_SCHEMA_VERSION, "entries": {}}


def _save_cache(folder: str, cache: Dict) -> None:
    path = cache_path(folder)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        pickle.dump(cache, f)


def load_documents_cached(
    folder: str,
    enable_ocr: bool = False,
    exts: Optional[Iterable[str]] = None,
) -> Tuple[List[DocEntry], Dict]:
    exts = set(exts or [".txt", ".md", ".pdf", ".docx"])

    cache = _load_cache(folder)
    entries = cache.get("entries", {}) or {}
    new_entries: Dict[str, Dict] = {}
    docs: List[DocEntry] = []
    changed = False

    enable_ocr = bool(enable_ocr and ocr_available())

    for root, _, files in os.walk(folder):
        for fn in files:
            path = os.path.join(root, fn)
            ext = os.path.splitext(fn.lower())[1]
            if ext not in exts:
                continue
            if ext == ".pdf" and _is_ocr_pdf(path):
                continue
            rel = os.path.relpath(path, folder)
            try:
                st = os.stat(path)
                mtime_ns = int(getattr(st, "st_mtime_ns", int(st.st_mtime * 1e9)))
                size = int(st.st_size)

                cached = entries.get(rel) or {}
                cached_mtime = cached.get("mtime_ns")
                cached_size = cached.get("size")

                use_cached = (
                    bool(cached)
                    and cached_mtime == mtime_ns
                    and cached_size == size
                    and cached.get("summary") is not None
                    and cached.get("chunks") is not None
                )
                if ext == ".pdf" and enable_ocr:
                    use_cached = use_cached and cached.get("ocr_ready") is True

                if use_cached:
                    entry = dict(cached)
                    summary = entry.get("summary", "")
                    chunks = entry.get("chunks", [])
                    summary_emb = entry.get("summary_emb")
                    chunk_embs = entry.get("chunk_embs")
                else:
                    changed = True
                    if ext in [".txt", ".md"]:
                        text = read_txt(path)
                        ocr_used = False
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
                        ocr_used = False

                    chunks = chunk_text(text)
                    summary = _make_summary(text)
                    summary_emb = None
                    chunk_embs = None
                    entry = {
                        "hash": _file_hash(path),
                        "summary": summary,
                        "chunks": chunks,
                        "summary_emb": summary_emb,
                        "chunk_embs": chunk_embs,
                        "ocr_ready": (enable_ocr and ext == ".pdf"),
                        "ocr_used": bool(ocr_used) if ext == ".pdf" else False,
                    }

                entry["mtime_ns"] = mtime_ns
                entry["size"] = size

                new_entries[rel] = entry
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
                continue

    # deletions
    if set(entries.keys()) - set(new_entries.keys()):
        changed = True

    # schema upgrade / metadata normalization
    if cache.get("schema_version") != CACHE_SCHEMA_VERSION:
        changed = True
    cache["schema_version"] = CACHE_SCHEMA_VERSION
    cache["entries"] = new_entries
    cache["chunk_chars"] = CHUNK_CHARS
    cache["updated_local"] = time.strftime("%Y-%m-%dT%H:%M:%S")

    if changed:
        _save_cache(folder, cache)

    return docs, cache


# ----------------------------
# Chunking + Retrieval (simple BM25-like)
# ----------------------------

STOPWORDS = set(
    """
a an the and or but if then else when while of for to in on at from by with without as is are was were be been being
this that these those it its it's i you we they he she them his her our your their not no yes do does did done
""".split()
)


def tokenize(text: str) -> List[str]:
    text = text.lower()
    toks = re.findall(r"[a-z0-9']{2,}", text)
    return [t for t in toks if t not in STOPWORDS]


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
    docs: List[DocEntry], doc_idxs: List[int], include_embeddings: bool = False
) -> Tuple[List[Chunk], List[List[float]]]:
    chunks: List[Chunk] = []
    chunk_embs: List[List[float]] = []
    for doc_idx in doc_idxs:
        doc = docs[doc_idx]
        for i, ch in enumerate(doc.chunks):
            tf = {}
            for t in tokenize(ch):
                tf[t] = tf.get(t, 0) + 1
            chunks.append(Chunk(doc_id=doc_idx, source=doc.name, idx=i, text=ch, tf=tf))
            if include_embeddings and doc.chunk_embs and i < len(doc.chunk_embs):
                chunk_embs.append(doc.chunk_embs[i])
            elif include_embeddings:
                chunk_embs.append([])
    return chunks, chunk_embs


def score_overlap(query_tokens: List[str], chunk: Chunk) -> float:
    score = 0.0
    for t in query_tokens:
        score += (1.5 if t in chunk.tf else 0.0) + min(chunk.tf.get(t, 0), 3) * 0.3
    return score


def retrieve(chunks: List[Chunk], query: str, top_k: int = 6) -> List[Tuple[float, Chunk]]:
    qtoks = tokenize(query)
    scored = [(score_overlap(qtoks, ch), ch) for ch in chunks]
    scored.sort(key=lambda x: x[0], reverse=True)
    return [(s, ch) for (s, ch) in scored if s > 0][:top_k]

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


def get_embedder(model: str = DEFAULT_EMBEDDER_MODEL):
    if SentenceTransformer is None:
        return None
    return SentenceTransformer(model)


def _embed_texts(embedder, texts: List[str], batch_size: int = 32) -> List[List[float]]:
    try:
        embs = embedder.encode(
            texts, batch_size=batch_size, show_progress_bar=False, normalize_embeddings=True
        )
        return [e.tolist() for e in embs]
    except TypeError:
        embs = embedder.encode(texts, batch_size=batch_size, show_progress_bar=False)
        embs = np.asarray(embs, dtype=np.float32)
        norms = np.linalg.norm(embs, axis=1, keepdims=True) + 1e-12
        embs = embs / norms
        return [e.tolist() for e in embs]


def ensure_embeddings(docs: List[DocEntry], cache: Dict, folder: str, embedder, embedder_model: str) -> None:
    if embedder is None:
        return
    entries = cache.get("entries", {}) or {}
    updated = False

    if cache.get("embedder_model") != embedder_model:
        updated = True
        cache["embedder_model"] = embedder_model
        for doc in docs:
            doc.summary_emb = None
            doc.chunk_embs = None

    for doc in docs:
        entry = entries.get(doc.rel, {}) or {}
        needs_summary = not doc.summary_emb
        needs_chunks = (not doc.chunk_embs) or len(doc.chunk_embs) != len(doc.chunks)
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
        cache["updated_local"] = time.strftime("%Y-%m-%dT%H:%M:%S")
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
        distances = distances[0].tolist()
        scores = [1.0 - float(d) for d in distances]
        return labels, scores

    sims = vecs @ query_emb.astype(np.float32)
    idxs = np.argsort(-sims)[: min(top_k, len(sims))].tolist()
    return idxs, [float(sims[i]) for i in idxs]


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
        scores = [
            score_overlap(qtoks, Chunk(doc_id=-1, source="", idx=0, text=s, tf={t: 1 for t in tokenize(s)}))
            for s in summaries
        ]
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


def retrieve_hybrid(
    chunks: List[Chunk], chunk_embs: List[List[float]], query: str, top_k: int, embedder=None
) -> List[Tuple[float, Chunk]]:
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
