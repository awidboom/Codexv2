import hashlib
import math
import os
import pickle
import re
import time
from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional, Tuple

import numpy as np

try:
    from rank_bm25 import BM25Okapi
except Exception:
    BM25Okapi = None
try:
    from sentence_transformers import SentenceTransformer
except Exception:
    SentenceTransformer = None
try:
    import hnswlib
except Exception:
    hnswlib = None

from io_utils import (
    is_ocr_pdf,
    ocr_output_path,
    ocr_pdf_to_searchable,
    pdf_needs_ocr,
    read_docx,
    read_pdf,
    read_txt,
)

CHUNK_CHARS = 1200
CONTEXT_TOKENS = 128000
EST_TOKENS_PER_CHAR = 0.25
PROMPT_OVERHEAD_TOKENS = 800


@dataclass
class DocEntry:
    path: str
    name: str
    rel: str
    summary: str
    chunks: List[str]
    summary_emb: Optional[List[float]] = None
    chunk_embs: Optional[List[List[float]]] = None


@dataclass
class Chunk:
    doc_id: int
    source: str
    idx: int
    text: str
    tf: Dict[str, int]


def cache_path(folder: str) -> str:
    return os.path.join(folder, ".rag_cache", "index.pkl")


def file_hash(path: str) -> str:
    h = hashlib.md5()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def make_summary(text: str, max_chars: int = 2000) -> str:
    cleaned = re.sub(r"\s+", " ", text).strip()
    return cleaned[:max_chars]


def estimate_tokens(text: str) -> int:
    return int(math.ceil(len(text) * EST_TOKENS_PER_CHAR))


def max_chunks_for_context() -> int:
    avg_chunk_tokens = int(CHUNK_CHARS * EST_TOKENS_PER_CHAR)
    available = max(CONTEXT_TOKENS - PROMPT_OVERHEAD_TOKENS, avg_chunk_tokens)
    return max(1, available // avg_chunk_tokens)


def load_cache(folder: str) -> Dict[str, Dict[str, str]]:
    path = cache_path(folder)
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


def save_cache(folder: str, cache: Dict[str, Dict[str, str]]) -> None:
    path = cache_path(folder)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        pickle.dump(cache, f)


def parse_ts(ts: Optional[str]) -> float:
    if not ts:
        return 0.0
    try:
        return time.mktime(time.strptime(ts, "%Y-%m-%dT%H:%M:%S"))
    except Exception:
        return 0.0


def scan_context_files(folder: str) -> Dict[str, str]:
    found: Dict[str, str] = {}
    for root, _, files in os.walk(folder):
        for fn in files:
            path = os.path.join(root, fn)
            ext = os.path.splitext(fn.lower())[1]
            if ext not in [".txt", ".md", ".pdf", ".docx"]:
                continue
            if ext == ".pdf" and is_ocr_pdf(path):
                continue
            rel = os.path.relpath(path, folder)
            found[rel] = path
    return found


def load_documents_cached(
    folder: str,
    enable_ocr: bool = False,
    force_reindex: bool = False,
    progress_cb=None,
) -> Tuple[List[DocEntry], Dict[str, Dict[str, str]]]:
    cache = load_cache(folder)
    entries = cache.get("entries", {})
    files = scan_context_files(folder)
    current_keys = set(files.keys())
    cached_keys = set(entries.keys())
    meta_in = cache.get("meta", {})
    last_indexed_ts = parse_ts(meta_in.get("last_indexed"))
    cached_failed = set(meta_in.get("failed_files", []) or [])
    new_files_count = 0
    for rel, path in files.items():
        try:
            mtime = os.path.getmtime(path)
        except Exception:
            mtime = 0.0
        if rel in cached_failed:
            continue
        if rel not in cached_keys or (last_indexed_ts and mtime > last_indexed_ts):
            new_files_count += 1

    # Fast path: no file list changes and not forcing; trust cached index.
    if (not force_reindex) and entries and current_keys == cached_keys:
        docs: List[DocEntry] = []
        for rel, path in files.items():
            cached = entries.get(rel, {})
            docs.append(
                DocEntry(
                    path=path,
                    name=os.path.basename(path),
                    rel=rel,
                    summary=cached.get("summary", ""),
                    chunks=cached.get("chunks", []),
                    summary_emb=cached.get("summary_emb"),
                    chunk_embs=cached.get("chunk_embs"),
                )
            )
        cache["meta"] = {
            "last_indexed": meta_in.get("last_indexed"),
            "total_files": len(files),
            "new_files_detected": 0,
            "failed_files": meta_in.get("failed_files", []) or [],
        }
        if progress_cb:
            progress_cb(1, 1, "Using cached index")
        return docs, cache

    new_entries: Dict[str, Dict[str, str]] = {}
    docs = []
    failed_files: List[str] = []
    total = max(1, len(files))
    for i, (rel, path) in enumerate(files.items(), start=1):
        ext = os.path.splitext(path.lower())[1]
        try:
            cached = entries.get(rel)
            ocr_used = False
            use_cached = False
            if cached and not force_reindex:
                try:
                    stat = os.stat(path)
                    if cached.get("mtime") == stat.st_mtime and cached.get("size") == stat.st_size:
                        use_cached = True
                except Exception:
                    use_cached = False
            if use_cached:
                summary = cached.get("summary", "")
                chunks = cached.get("chunks", [])
                summary_emb = cached.get("summary_emb")
                chunk_embs = cached.get("chunk_embs")
            else:
                fhash = file_hash(path)
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
                        if enable_ocr and pdf_needs_ocr(path):
                            ocr_path = ocr_output_path(path)
                            if ocr_pdf_to_searchable(path, ocr_path):
                                text = read_pdf(ocr_path)
                                ocr_used = True
                            else:
                                text = read_pdf(path)
                        else:
                            text = read_pdf(path)
                    else:
                        text = read_docx(path)
                    chunks = chunk_text(text)
                    summary = make_summary(text)
                    summary_emb = None
                    chunk_embs = None
            try:
                stat = os.stat(path)
                mtime = stat.st_mtime
                size = stat.st_size
            except Exception:
                mtime = None
                size = None
            new_entries[rel] = {
                "hash": cached.get("hash") if use_cached and cached else file_hash(path),
                "summary": summary,
                "chunks": chunks,
                "summary_emb": summary_emb,
                "chunk_embs": chunk_embs,
                "ocr_ready": (enable_ocr and ext == ".pdf"),
                "ocr_used": ocr_used if ext == ".pdf" else False,
                "mtime": mtime,
                "size": size,
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
            failed_files.append(rel)
            try:
                stat = os.stat(path)
                mtime = stat.st_mtime
                size = stat.st_size
            except Exception:
                mtime = None
                size = None
            new_entries[rel] = {
                "hash": None,
                "summary": "",
                "chunks": [],
                "summary_emb": None,
                "chunk_embs": None,
                "ocr_ready": (enable_ocr and ext == ".pdf"),
                "ocr_used": False,
                "mtime": mtime,
                "size": size,
                "failed": True,
            }
            continue
        if progress_cb:
            progress_cb(i, total, "Indexing files...")
    meta = {
        "last_indexed": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "total_files": len(files),
        "new_files_detected": new_files_count,
        "failed_files": failed_files,
    }
    save_cache(folder, {"version": 1, "entries": new_entries, "meta": meta})
    return docs, {"version": 1, "entries": new_entries, "meta": meta}


STOPWORDS = set(
    """
a an the and or but if then else when while of for to in on at from by with without as is are was were be been being
this that these those it its it's i you we they he she them his her our your their not no yes do does did done
""".split()
)

EXACT_MATCH_BOOST = 2.0


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
        if t in chunk.tf:
            score += EXACT_MATCH_BOOST
        score += (1.5 if t in chunk.tf else 0.0) + min(chunk.tf.get(t, 0), 3) * 0.3
    return score


def retrieve(chunks: List[Chunk], query: str, top_k: int = 6) -> List[Tuple[float, Chunk]]:
    qtoks = tokenize(query)
    scored = [(score_overlap(qtoks, ch), ch) for ch in chunks]
    scored.sort(key=lambda x: x[0], reverse=True)
    return [(s, ch) for (s, ch) in scored if s > 0][:top_k]


def get_embedder():
    if SentenceTransformer is None:
        return None
    return SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


def embed_texts(embedder, texts: List[str], batch_size: int = 32) -> List[List[float]]:
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
            doc.summary_emb = embed_texts(embedder, [doc.summary])[0]
            entry["summary_emb"] = doc.summary_emb
            updated = True
        if needs_chunks:
            doc.chunk_embs = embed_texts(embedder, doc.chunks)
            entry["chunk_embs"] = doc.chunk_embs
            updated = True
        entries[doc.rel] = entry
    if updated:
        cache["entries"] = entries
        save_cache(folder, cache)


def dense_scores(embs: List[List[float]], query_emb: np.ndarray, top_k: int) -> Tuple[List[int], List[float]]:
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


def rrf_merge(sparse_scores: List[float], dense_ranks: Dict[int, int], k: int = 60) -> List[float]:
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
        scores = [
            score_overlap(qtoks, Chunk(doc_id=-1, source="", idx=0, text=s, tf={t: 1 for t in tokenize(s)}))
            for s in summaries
        ]
    if embedder is None:
        ranked = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)
        return ranked[:top_k]
    query_emb = np.asarray(embed_texts(embedder, [query])[0], dtype=np.float32)
    doc_embs = [doc.summary_emb or [] for doc in docs]
    dense_idxs, _ = dense_scores(doc_embs, query_emb, top_k=len(docs))
    dense_rank = {idx: rank for rank, idx in enumerate(dense_idxs, start=1)}
    merged = rrf_merge(list(scores), dense_rank)
    ranked = sorted(range(len(merged)), key=lambda i: merged[i], reverse=True)
    return ranked[:top_k]


def score_chunks(chunks: List[Chunk], chunk_embs: List[List[float]], query: str, embedder=None) -> List[float]:
    qtoks = tokenize(query)
    sparse_scores = [score_overlap(qtoks, ch) for ch in chunks]
    if embedder is None or not chunk_embs:
        return sparse_scores
    query_emb = np.asarray(embed_texts(embedder, [query])[0], dtype=np.float32)
    dense_idxs, _ = dense_scores(chunk_embs, query_emb, top_k=len(chunks))
    dense_rank = {idx: rank for rank, idx in enumerate(dense_idxs, start=1)}
    return rrf_merge(sparse_scores, dense_rank)


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
