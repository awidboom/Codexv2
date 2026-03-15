import argparse
import os
import sys
import uuid

import rag_core as rc


def _bool_flag(parser: argparse.ArgumentParser, name: str, default: bool, help_text: str):
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument(f"--{name}", dest=name.replace("-", "_"), action="store_true", help=help_text)
    group.add_argument(
        f"--no-{name}",
        dest=name.replace("-", "_"),
        action="store_false",
        help=f"Disable: {help_text}",
    )
    parser.set_defaults(**{name.replace("-", "_"): default})


def _common_args(p: argparse.ArgumentParser):
    p.add_argument("--context-folder", default=os.getcwd(), help="Folder to index/query (default: cwd).")
    p.add_argument("--top-k", type=int, default=min(6, max(2, rc.max_chunks_for_context())), help="Top-K chunks.")
    _bool_flag(p, "use-dense", default=True, help_text="Use dense retrieval (embeddings).")
    _bool_flag(p, "enable-ocr", default=False, help_text="Auto-OCR scanned PDFs when possible.")
    _bool_flag(p, "ensure-coverage", default=True, help_text="Ensure coverage across documents.")
    p.add_argument("--min-per-doc", type=int, default=1, help="Minimum chunks per document (coverage mode).")
    p.add_argument(
        "--embedder-model",
        default=rc.DEFAULT_EMBEDDER_MODEL,
        help=f"SentenceTransformers model id (default: {rc.DEFAULT_EMBEDDER_MODEL}).",
    )


def cmd_index(args: argparse.Namespace) -> int:
    folder = os.path.abspath(args.context_folder)
    if not os.path.isdir(folder):
        print(f"Context folder not found: {folder}", file=sys.stderr)
        return 2

    docs, cache = rc.load_documents_cached(folder, enable_ocr=args.enable_ocr)
    embedder = rc.get_embedder(args.embedder_model) if args.use_dense else None
    if args.use_dense and embedder is None:
        print("Dense retrieval requested but sentence-transformers is not installed.", file=sys.stderr)
    rc.ensure_embeddings(docs, cache, folder, embedder, embedder_model=args.embedder_model)
    print(f"Indexed {len(docs)} documents. Cache: {rc.cache_path(folder)}")
    return 0


def _read_question(args: argparse.Namespace) -> str:
    if args.question is not None:
        return args.question
    if args.question_file is not None:
        with open(args.question_file, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    return sys.stdin.read()


def cmd_query(args: argparse.Namespace) -> int:
    folder = os.path.abspath(args.context_folder)
    if not os.path.isdir(folder):
        print(f"Context folder not found: {folder}", file=sys.stderr)
        return 2

    question = (_read_question(args) or "").strip()
    if not question:
        print("Question is empty. Use --question, --question-file, or stdin.", file=sys.stderr)
        return 2

    docs, cache = rc.load_documents_cached(folder, enable_ocr=args.enable_ocr)
    embedder = rc.get_embedder(args.embedder_model) if args.use_dense else None
    if args.use_dense and embedder is None:
        print("Dense retrieval requested but sentence-transformers is not installed.", file=sys.stderr)
    rc.ensure_embeddings(docs, cache, folder, embedder, embedder_model=args.embedder_model)

    if args.ensure_coverage and len(docs) > 0:
        selected_doc_idxs = list(range(len(docs)))
    else:
        doc_top_k = min(max(args.top_k * 4, 10), max(1, len(docs)))
        selected_doc_idxs = rc.retrieve_docs(docs, question, top_k=doc_top_k, embedder=embedder)

    chunks, chunk_embs = rc.build_chunk_index(docs, selected_doc_idxs, include_embeddings=embedder is not None)
    if args.ensure_coverage:
        selected = rc.retrieve_with_coverage(
            chunks,
            chunk_embs,
            question,
            top_k=args.top_k,
            embedder=embedder,
            min_per_doc=args.min_per_doc,
        )
    else:
        selected = rc.retrieve_hybrid(chunks, chunk_embs, question, top_k=args.top_k, embedder=embedder)

    job_id = str(uuid.uuid4())[:8]
    prompt = rc.build_query_txt(job_id, question, selected, folder)

    if args.out:
        out_path = os.path.abspath(args.out)
        os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(prompt)

    if not args.quiet:
        sys.stdout.write(prompt)

    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Agent-friendly RAG index + prompt builder.")
    sub = p.add_subparsers(dest="cmd", required=True)

    p_index = sub.add_parser("index", help="Update the on-disk cache/index incrementally.")
    _common_args(p_index)
    p_index.set_defaults(func=cmd_index)

    p_query = sub.add_parser("query", help="Build a RAG prompt for a question.")
    _common_args(p_query)
    p_query.add_argument("--question", help="Question text (otherwise uses --question-file or stdin).")
    p_query.add_argument("--question-file", help="Read question from a file.")
    p_query.add_argument("--out", help="Write prompt to a file (optional).")
    p_query.add_argument("--quiet", action="store_true", help="Do not print prompt to stdout.")
    p_query.set_defaults(func=cmd_query)

    return p


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
