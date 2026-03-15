import os, re, time, json, uuid
from dataclasses import dataclass
from typing import List, Tuple, Dict, Iterable

import streamlit as st
from pypdf import PdfReader
import docx

# ----------------------------
# Document loading
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

def load_documents(folder: str) -> List[Tuple[str, str]]:
    docs = []
    for root, _, files in os.walk(folder):
        for fn in files:
            path = os.path.join(root, fn)
            ext = os.path.splitext(fn.lower())[1]
            try:
                if ext in [".txt", ".md"]:
                    docs.append((path, read_txt(path)))
                elif ext == ".pdf":
                    docs.append((path, read_pdf(path)))
                elif ext == ".docx":
                    docs.append((path, read_docx(path)))
                else:
                    continue
            except Exception as e:
                # skip unreadable files
                continue
    return docs

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

def chunk_text(text: str, chunk_chars: int = 1200, overlap: int = 150) -> List[str]:
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
    source: str
    idx: int
    text: str
    tf: Dict[str, int]

def build_chunk_index(docs: List[Tuple[str, str]]) -> List[Chunk]:
    chunks: List[Chunk] = []
    for path, text in docs:
        for i, ch in enumerate(chunk_text(text)):
            toks = tokenize(ch)
            tf: Dict[str, int] = {}
            for t in toks:
                tf[t] = tf.get(t, 0) + 1
            chunks.append(Chunk(source=os.path.basename(path), idx=i, text=ch, tf=tf))
    return chunks

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

# ----------------------------
# Prompt packaging + file I/O
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
        "- If the context is insufficient, say what’s missing.",
        "- Cite context chunks like [1], [2] when you rely on them.",
    ]
    return "\n".join(lines).strip() + "\n"

def write_text(path: str, content: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def wait_for_file(path: str, timeout_s: int = 180) -> str:
    # blocking poll (simple + reliable)
    start = time.time()
    while True:
        if os.path.exists(path):
            return read_txt(path)
        if time.time() - start > timeout_s:
            raise TimeoutError(f"Timed out waiting for: {path}")
        time.sleep(1.0)

# ----------------------------
# Streamlit UI
# ----------------------------

st.set_page_config(page_title="File-triggered RAG GUI", layout="wide")
st.title("File-triggered RAG (OneDrive + Power Automate + AI Builder)")

with st.sidebar:
    st.subheader("Paths")
    base = r"C:\Users\aaw\OneDrive - Barr Engineering Co\RAG"

    onedrive_inbox = st.text_input(
        "OneDrive Inbox folder (local sync path)",
        value=os.path.join(base, "RAG_Inbox")
    )
    onedrive_outbox = st.text_input(
        "OneDrive Outbox folder (local sync path)",
        value=os.path.join(base, "RAG_Outbox")
    )
    st.divider()
    top_k = st.slider("Top-K context chunks", 2, 12, 6)
    timeout_s = st.slider("Wait for output (seconds)", 30, 600, 180)

st.subheader("1) Select your local context folder")
context_folder = st.text_input("Context folder (local)", value=os.getcwd())

st.subheader("2) Ask a question")
question = st.text_area("Question", height=120, placeholder="Type your question here...")

run = st.button("Run RAG → Write query file → Wait for output", type="primary", disabled=not (question.strip() and os.path.isdir(context_folder)))

if run:
    job_id = str(uuid.uuid4())[:8]
    query_name = f"query_{job_id}.txt"
    out_name = f"output_{job_id}.txt"
    query_path = os.path.join(onedrive_inbox, query_name)
    out_path = os.path.join(onedrive_outbox, out_name)

    with st.status("Indexing and retrieving context…", expanded=False):
        docs = load_documents(context_folder)
        chunks = build_chunk_index(docs)
        selected = retrieve(chunks, question, top_k=top_k)

    query_txt = build_query_txt(job_id, question, selected, context_folder)
    write_text(query_path, query_txt)

    st.success(f"Wrote: {query_path}  (OneDrive should sync it; Power Automate should pick it up.)")
    st.code(query_txt[:4000] + ("\n...\n" if len(query_txt) > 4000 else ""), language="text")

    with st.status("Waiting for output file…", expanded=False):
        try:
            result = wait_for_file(out_path, timeout_s=timeout_s)
            st.subheader("Result")
            st.text_area("output", value=result, height=300)
            st.info(f"Read: {out_path}")
        except TimeoutError as e:
            st.error(str(e))
            st.caption("If this happens: confirm OneDrive sync is working and the Flow writes output_<jobid>.txt to /RAG_Outbox.")
