#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import parse_baaqmd_regulations as rule_parser


RAG_CLI = Path(r"C:\Users\aaw\.codex\skills\agentic-rag-indexer\scripts\rag_cli.py")
DEFAULT_OUT_ROOT = ROOT / "baaqmd_rules"
DEFAULT_JSON_DIR = DEFAULT_OUT_ROOT / "json"
DEFAULT_MD_DIR = DEFAULT_OUT_ROOT / "rag_md"
DEFAULT_MANIFEST = DEFAULT_OUT_ROOT / "manifest.json"
DEFAULT_NSR_GUIDANCE_DIR = ROOT / "NSR guidance"


@dataclass
class UpdateSummary:
    current_total: int
    new_keys: list[str]
    changed_keys: list[str]
    removed_keys: list[str]


def _record_key(record: dict[str, Any]) -> str:
    return str(record.get("rule_number") or record.get("title") or "untitled").strip()


def _load_manifest(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _fetch_current_rule_records(source_url: str, timeout: int) -> list[dict[str, Any]]:
    page_html = rule_parser.fetch_url_text(source_url, timeout_s=timeout)
    rules = rule_parser.build_rule_objects_from_table_api(page_html, source_url, timeout_s=timeout)
    if not rules:
        rules = rule_parser.build_rule_objects(page_html, source_url)
    records: list[dict[str, Any]] = []
    for rule in rules:
        records.append(
            {
                "rule_number": rule.rule_no,
                "title": rule.title,
                "source_url": rule.url or None,
                **(rule.metadata or {}),
            }
        )
    return records


def check_for_updates(manifest_path: Path, source_url: str, timeout: int) -> UpdateSummary:
    previous_manifest = _load_manifest(manifest_path)
    previous_records = {
        _record_key(record): record for record in previous_manifest.get("records", []) if isinstance(record, dict)
    }
    current_records = _fetch_current_rule_records(source_url, timeout)
    current_map = {_record_key(record): record for record in current_records}

    new_keys: list[str] = []
    changed_keys: list[str] = []
    removed_keys = sorted(set(previous_records) - set(current_map))

    compare_fields = ["title", "source_url", "version_status", "adopted", "amended", "description"]
    for key, record in current_map.items():
        old = previous_records.get(key)
        if old is None:
            new_keys.append(key)
            continue
        if any((old.get(field) or None) != (record.get(field) or None) for field in compare_fields):
            changed_keys.append(key)

    return UpdateSummary(
        current_total=len(current_records),
        new_keys=sorted(new_keys),
        changed_keys=sorted(changed_keys),
        removed_keys=removed_keys,
    )


def _delete_if_exists(path: Path) -> None:
    if path.exists():
        path.unlink()


def _md_path_for_json(json_path: Path, md_dir: Path) -> Path:
    return md_dir / f"{json_path.stem}.md"


def purge_stale_artifacts(summary: UpdateSummary, manifest_path: Path, md_dir: Path) -> None:
    previous_manifest = _load_manifest(manifest_path)
    previous_records = {
        _record_key(record): record for record in previous_manifest.get("records", []) if isinstance(record, dict)
    }
    for key in summary.changed_keys + summary.removed_keys:
        record = previous_records.get(key)
        if not record:
            continue
        local_pdf = record.get("local_pdf")
        if local_pdf:
            _delete_if_exists(ROOT / local_pdf)
        rule_no = record.get("rule_number")
        title = record.get("title")
        stem = f"rule_{rule_no}" if rule_no else rule_parser.safe_slug(str(title))
        json_path = DEFAULT_JSON_DIR / f"{rule_parser.safe_slug(stem)}.json"
        _delete_if_exists(json_path)
        _delete_if_exists(_md_path_for_json(json_path, md_dir))


def run_subprocess(args: list[str]) -> None:
    result = subprocess.run(args, cwd=ROOT, text=True)
    if result.returncode != 0:
        raise SystemExit(result.returncode)


def run_subprocess_capture(args: list[str]) -> str:
    result = subprocess.run(args, cwd=ROOT, text=True, capture_output=True)
    if result.returncode != 0:
        sys.stderr.write(result.stderr or "")
        raise SystemExit(result.returncode)
    return result.stdout or ""


def _is_regulation_2_question(question: str) -> bool:
    q = question.lower()
    return bool(
        re.search(r"\breg(?:ulation)?\s*2\b", q)
        or re.search(r"\b2-\d+\b", q)
        or "nsr" in q
        or "new source review" in q
    )


def _ensure_index(context_folder: Path, *, top_k: int, use_dense: bool, ensure_coverage: bool) -> None:
    index_path = context_folder / ".rag_cache" / "index.pkl"
    if index_path.exists():
        return
    run_subprocess(
        [
            sys.executable,
            str(RAG_CLI),
            "index",
            "--context-folder",
            str(context_folder),
            "--top-k",
            str(top_k),
            "--use-dense" if use_dense else "--no-use-dense",
            "--ensure-coverage" if ensure_coverage else "--no-ensure-coverage",
        ]
    )


def run_refresh(out_root: Path, *, source_url: str, timeout: int, top_k: int, use_dense: bool, ensure_coverage: bool) -> UpdateSummary:
    summary = check_for_updates(out_root / "manifest.json", source_url, timeout)
    print(
        f"Rules on site: {summary.current_total}; new: {len(summary.new_keys)}; "
        f"changed: {len(summary.changed_keys)}; removed: {len(summary.removed_keys)}"
    )
    purge_stale_artifacts(summary, out_root / "manifest.json", out_root / "rag_md")

    run_subprocess(
        [
            sys.executable,
            str(ROOT / "parse_baaqmd_regulations.py"),
            "--out-root",
            str(out_root),
            "--source-url",
            source_url,
            "--timeout",
            str(timeout),
        ]
    )
    run_subprocess(
        [
            sys.executable,
            str(ROOT / "scripts" / "baaqmd_rules_json_to_md.py"),
            "--json-folder",
            str(out_root / "json"),
            "--out-folder",
            str(out_root / "rag_md"),
        ]
    )
    run_subprocess(
        [
            sys.executable,
            str(RAG_CLI),
            "index",
            "--context-folder",
            str(out_root / "rag_md"),
            "--top-k",
            str(top_k),
            "--use-dense" if use_dense else "--no-use-dense",
            "--ensure-coverage" if ensure_coverage else "--no-ensure-coverage",
        ]
    )
    return summary


def cmd_check(args: argparse.Namespace) -> int:
    summary = check_for_updates(Path(args.out_root) / "manifest.json", args.source_url, args.timeout)
    print(json.dumps(summary.__dict__, indent=2))
    return 0


def cmd_refresh(args: argparse.Namespace) -> int:
    run_refresh(
        Path(args.out_root),
        source_url=args.source_url,
        timeout=args.timeout,
        top_k=args.top_k,
        use_dense=args.use_dense,
        ensure_coverage=args.ensure_coverage,
    )
    return 0


def cmd_query(args: argparse.Namespace) -> int:
    out_root = Path(args.out_root)
    if args.refresh_first:
        run_refresh(
            out_root,
            source_url=args.source_url,
            timeout=args.timeout,
            top_k=args.top_k,
            use_dense=args.use_dense,
            ensure_coverage=args.ensure_coverage,
        )
    query_args = [
        sys.executable,
        str(RAG_CLI),
        "query",
        "--context-folder",
        str(out_root / "rag_md"),
        "--question",
        args.question,
        "--top-k",
        str(args.top_k),
        "--use-dense" if args.use_dense else "--no-use-dense",
        "--ensure-coverage" if args.ensure_coverage else "--no-ensure-coverage",
    ]
    if args.out:
        query_args.extend(["--out", args.out])
    primary_output = run_subprocess_capture(query_args)
    sys.stdout.write(primary_output)

    nsr_guidance_folder = Path(args.nsr_guidance_folder)
    if _is_regulation_2_question(args.question) and nsr_guidance_folder.exists():
        _ensure_index(
            nsr_guidance_folder,
            top_k=args.top_k,
            use_dense=args.use_dense,
            ensure_coverage=args.ensure_coverage,
        )
        nsr_args = [
            sys.executable,
            str(RAG_CLI),
            "query",
            "--context-folder",
            str(nsr_guidance_folder),
            "--question",
            args.question,
            "--top-k",
            str(args.top_k),
            "--use-dense" if args.use_dense else "--no-use-dense",
            "--ensure-coverage" if args.ensure_coverage else "--no-ensure-coverage",
        ]
        if args.out:
            out_path = Path(args.out)
            nsr_out = str(out_path.with_name(f"{out_path.stem}_nsr_guidance{out_path.suffix or '.txt'}"))
            nsr_args.extend(["--out", nsr_out])
        nsr_output = run_subprocess_capture(nsr_args)
        sys.stdout.write("\n### NSR_GUIDANCE_CONTEXT\n")
        sys.stdout.write(nsr_output)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Refresh BAAQMD rules, convert to JSON/MD, and maintain a RAG index.")
    parser.add_argument("--out-root", default=str(DEFAULT_OUT_ROOT))
    parser.add_argument("--source-url", default=rule_parser.CURRENT_RULES_URL)
    parser.add_argument("--timeout", type=int, default=45)
    parser.add_argument("--top-k", type=int, default=6)
    parser.add_argument("--use-dense", action="store_true", default=False)
    parser.add_argument("--ensure-coverage", action="store_true", default=True)

    sub = parser.add_subparsers(dest="command", required=True)

    p_check = sub.add_parser("check", help="Check the website for new/changed/removed rules.")
    p_check.set_defaults(func=cmd_check)

    p_refresh = sub.add_parser("refresh", help="Refresh PDFs, JSON, Markdown corpus, and RAG index.")
    p_refresh.set_defaults(func=cmd_refresh)

    p_query = sub.add_parser("query", help="Refresh the rule set, then run a RAG query.")
    p_query.add_argument("--question", required=True)
    p_query.add_argument("--out")
    p_query.add_argument("--nsr-guidance-folder", default=str(DEFAULT_NSR_GUIDANCE_DIR))
    p_query.add_argument("--refresh-first", action="store_true", default=True)
    p_query.set_defaults(func=cmd_query)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
