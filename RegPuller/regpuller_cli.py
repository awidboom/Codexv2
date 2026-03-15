import argparse
import json
import os
import sys
import time
import uuid
from typing import Dict, Iterable, List, Tuple

import download_regs
import download_regulations_gov
from indexing import (
    CONTEXT_TOKENS,
    Chunk,
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
from io_utils import convert_from_path, pytesseract


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


def run_prompt(
    context_folder: str,
    question: str,
    top_k: int,
    use_dense: bool,
    ensure_coverage: bool,
    min_per_doc: int,
    force_reindex: bool,
    enable_ocr: bool,
    include_citations: bool,
) -> Tuple[str, int]:
    ocr_available = enable_ocr and pytesseract is not None and convert_from_path is not None
    if enable_ocr and not ocr_available:
        print("OCR is enabled but pytesseract/pdf2image are not installed.", file=sys.stderr)
    docs, cache = load_documents_cached(
        context_folder,
        enable_ocr=ocr_available,
        force_reindex=force_reindex,
    )
    meta = cache.get("meta", {})
    if meta.get("last_indexed"):
        print(f"Last indexed: {meta.get('last_indexed')}", file=sys.stderr)
    if meta.get("new_files_detected") is not None:
        print(f"New files detected: {meta.get('new_files_detected')}", file=sys.stderr)
    failed_files = meta.get("failed_files") or []
    if failed_files:
        shown = failed_files[:10]
        more = len(failed_files) - len(shown)
        msg = "Failed to index (cached): " + ", ".join(shown)
        if more > 0:
            msg += f" (+{more} more)"
        print(msg, file=sys.stderr)
    embedder = get_embedder() if use_dense else None
    if use_dense and embedder is None:
        print("Dense retrieval is enabled but sentence-transformers is not installed.", file=sys.stderr)
    ensure_embeddings(docs, cache, context_folder, embedder)
    if ensure_coverage and len(docs) > 300:
        print("Coverage mode is enabled; large folders may be slow to process.", file=sys.stderr)
    if ensure_coverage and top_k < len(docs):
        print("Top-K is smaller than the document count; not all documents can be included.", file=sys.stderr)
    retrieval_query = question
    if ensure_coverage:
        selected_doc_idxs = list(range(len(docs)))
    else:
        doc_top_k = min(max(top_k * 4, 10), len(docs))
        selected_doc_idxs = retrieve_docs(docs, retrieval_query, top_k=doc_top_k, embedder=embedder)
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
    job_id = str(uuid.uuid4())[:8]
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
            print(
                "Estimated tokens exceed the 128k context window; consider reducing Top-K.",
                file=sys.stderr,
            )
    return query_txt, est_tokens


def write_manifest_entries(manifest_path: str, entries: List[Dict[str, object]]) -> None:
    manifest = download_regs.load_manifest(manifest_path)
    manifest_entries = manifest.get("entries", [])
    if not isinstance(manifest_entries, list):
        manifest_entries = []
    manifest_entries.extend(entries)
    manifest["entries"] = manifest_entries
    download_regs.write_manifest(manifest_path, manifest)


def parse_keywords(value: str) -> List[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="RegPuller CLI: download rule/FR docs, Regulations.gov files, or build a RAG prompt."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    rule_parser = subparsers.add_parser("rule", help="Download eCFR rule + FR documents")
    rule_parser.add_argument("--url", default="", help="eCFR rule URL")
    rule_parser.add_argument("--out-dir", default="data", help="Output directory (default: data)")
    rule_parser.add_argument("--rule-title", default="", help="Optional override for rule title")
    rule_parser.add_argument(
        "--config",
        default="",
        help="Optional JSON config file with rules to download",
    )
    rule_parser.add_argument(
        "--manifest",
        default="",
        help="Optional manifest file path (default: <out-dir>/manifest.json)",
    )
    rule_parser.add_argument("--no-manifest", action="store_true", help="Skip manifest update")
    rule_parser.add_argument("--json", action="store_true", help="Print result JSON to stdout")

    reggov_parser = subparsers.add_parser("reggov", help="Download Regulations.gov attachments")
    reggov_parser.add_argument("--docket", required=True, help="Docket ID")
    reggov_parser.add_argument(
        "--keywords",
        default="Technical Support Document, Response to Comments",
        help="Comma-separated keywords",
    )
    reggov_parser.add_argument("--out-dir", default="data", help="Output directory (default: data)")
    reggov_parser.add_argument(
        "--api-key",
        default=os.environ.get("REGGOV_API_KEY", ""),
        help="Regulations.gov API key (X-Api-Key).",
    )
    reggov_parser.add_argument(
        "--formats",
        default="pdf,txt",
        help="Comma-separated formats to download (default: pdf,txt)",
    )
    reggov_parser.add_argument("--json", action="store_true", help="Print result JSON to stdout")

    prompt_parser = subparsers.add_parser("prompt", help="Build a RAG prompt from local files")
    prompt_parser.add_argument("--context-folder", required=True, help="Folder with local docs")
    prompt_parser.add_argument("--question", required=True, help="Question to answer")
    prompt_parser.add_argument(
        "--top-k",
        type=int,
        default=min(6, max_chunks_for_context()),
        help="Top-K chunks (default: 6 or max allowed)",
    )
    prompt_parser.add_argument("--use-dense", dest="use_dense", action="store_true", default=True)
    prompt_parser.add_argument("--no-dense", dest="use_dense", action="store_false")
    prompt_parser.add_argument("--ensure-coverage", dest="ensure_coverage", action="store_true", default=True)
    prompt_parser.add_argument("--no-coverage", dest="ensure_coverage", action="store_false")
    prompt_parser.add_argument(
        "--min-per-doc",
        type=int,
        default=1,
        help="Minimum chunks per document when ensure-coverage is enabled.",
    )
    prompt_parser.add_argument("--force-reindex", action="store_true", help="Force reindex")
    prompt_parser.add_argument("--enable-ocr", action="store_true", help="Enable OCR for PDFs")
    prompt_parser.add_argument(
        "--include-citations",
        dest="include_citations",
        action="store_true",
        default=True,
    )
    prompt_parser.add_argument(
        "--no-citations",
        dest="include_citations",
        action="store_false",
    )
    prompt_parser.add_argument("--output", default="", help="Write prompt to a file")

    args = parser.parse_args()

    if args.command == "rule":
        entries: List[Dict[str, object]] = []
        if args.config:
            try:
                with open(args.config, "r", encoding="utf-8") as f:
                    cfg = json.load(f)
            except (OSError, json.JSONDecodeError) as exc:
                print(f"Failed to read config: {exc}", file=sys.stderr)
                return 2
            rules = cfg.get("rules", [])
            if not isinstance(rules, list):
                print("Config file must include a 'rules' array.", file=sys.stderr)
                return 2
            for rule in rules:
                if not isinstance(rule, dict) or not rule.get("url"):
                    continue
                out_dir = rule.get("out_dir", args.out_dir)
                title = rule.get("title", "")
                entries.append(download_regs.run_download(rule["url"], out_dir, title))
        else:
            if not args.url:
                print("Missing --url for rule command.", file=sys.stderr)
                return 2
            entries.append(download_regs.run_download(args.url, args.out_dir, args.rule_title))

        if not args.no_manifest:
            manifest_path = args.manifest or os.path.join(args.out_dir, "manifest.json")
            write_manifest_entries(manifest_path, entries)
            print(f"Manifest updated: {manifest_path}")
        if args.json:
            print(json.dumps(entries, indent=2))
        else:
            for entry in entries:
                errors = entry.get("errors") or []
                rule_dir = entry.get("rule_dir") or ""
                status = "ok" if not errors else "errors"
                print(f"{entry.get('rule_title')}: {status} ({rule_dir})")
                if errors:
                    print(" - " + "; ".join(errors))
        return 0

    if args.command == "reggov":
        if not args.api_key:
            print("Missing --api-key (or REGGOV_API_KEY).", file=sys.stderr)
            return 2
        keywords = parse_keywords(args.keywords)
        formats = [item.strip().lower() for item in args.formats.split(",") if item.strip()]
        downloads = download_regulations_gov.download_docket_attachments(
            args.docket,
            keywords,
            args.out_dir,
            args.api_key,
            allowed_formats=tuple(formats),
        )
        if args.json:
            print(json.dumps(downloads, indent=2))
        else:
            print(f"Downloaded {len(downloads)} file(s).")
            for item in downloads:
                print(f"- {item.get('path')}")
        return 0

    if args.command == "prompt":
        if not os.path.isdir(args.context_folder):
            print("Context folder not found.", file=sys.stderr)
            return 2
        query_txt, est_tokens = run_prompt(
            args.context_folder,
            args.question,
            args.top_k,
            args.use_dense,
            args.ensure_coverage,
            args.min_per_doc,
            args.force_reindex,
            args.enable_ocr,
            args.include_citations,
        )
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(query_txt)
            print(f"Prompt written: {args.output} (est. {est_tokens} tokens)")
        else:
            print(query_txt)
            print(f"\n[estimated tokens: {est_tokens}]", file=sys.stderr)
        return 0

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
