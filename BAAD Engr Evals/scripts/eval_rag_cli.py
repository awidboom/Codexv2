#!/usr/bin/env python3
"""
Minimal CLI to:
  (a) Build a JSON -> Markdown style corpus (sectioned) from engineering-eval JSONs
  (b) Run the agentic-rag-indexer indexer on that corpus
  (c) Generate a new evaluation JSON skeleton + per-section prompt packs using retrieved exemplars

Default behavior is "prompt-only" generation (no LLM calls). It creates:
  - a schema-shaped JSON with empty section text
  - prompt files (one per section) that include Top-K exemplar chunks for that section
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple


SKILL_RAG_CLI = r"C:\Users\aaw\.codex\skills\agentic-rag-indexer\scripts\rag_cli.py"
SKILL_RAG_CORE = r"C:\Users\aaw\.codex\skills\agentic-rag-indexer\scripts\rag_core.py"


SECTION_ORDER: List[Tuple[str, str]] = [
    ("background", "$.background.text"),
    ("emission_calculations", "$.emission_calculations.text"),
    ("cumulative_increase", "$.cumulative_increase.text"),
    ("toxic_risk_screening_analysis", "$.toxic_risk_screening_analysis.narrative"),
    ("BACT", "$.BACT.text"),
    ("offsets", "$.offsets.narrative"),
    ("PSD_applicability", "$.PSD_applicability.narrative"),
    ("CEQA", "$.CEQA.narrative"),
    ("Statement_of_Compliance", "$.Statement_of_Compliance"),
    ("public_notification", "$.public_notification.text"),
    ("conditions", "$.conditions.text"),
    ("permit_conditions", "$.permit_conditions"),
    ("TitleV_permit", "$.TitleV_permit.narrative"),
    ("recommendation", "$.recommendation.text"),
]


def _read_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _safe_filename(name: str) -> str:
    s = re.sub(r"[^A-Za-z0-9._-]+", "_", name).strip("_")
    return s or "file"


def _unique_path(path: Path) -> Path:
    if not path.exists():
        return path
    base = path.with_suffix("")
    ext = path.suffix
    for i in range(1, 10000):
        cand = Path(f"{base}-{i}{ext}")
        if not cand.exists():
            return cand
    raise RuntimeError(f"Could not find a unique filename for: {path}")


def _norm_space(s: str) -> str:
    return re.sub(r"\s+", " ", s or "").strip()


def _json_get_text(obj: Dict[str, Any], key: str) -> str:
    v = obj.get(key)
    if v is None:
        return ""
    if isinstance(v, str):
        return v
    if isinstance(v, dict):
        if "text" in v and isinstance(v.get("text"), str):
            return v.get("text") or ""
        if "narrative" in v and isinstance(v.get("narrative"), str):
            return v.get("narrative") or ""
    return ""


def _render_statement_of_compliance(soc: Any) -> str:
    if not soc:
        return ""
    if isinstance(soc, str):
        return soc
    if isinstance(soc, dict):
        out: List[str] = []
        for section, payload in soc.items():
            out.append(f"### {section}")
            if isinstance(payload, dict):
                findings = payload.get("findings") or []
                if isinstance(findings, list):
                    for f in findings:
                        if isinstance(f, str) and f.strip():
                            out.append(f.strip())
            out.append("")
        return "\n".join(out).strip()
    return ""


def _render_permit_conditions(pc: Any) -> str:
    if not pc or not isinstance(pc, dict):
        return ""
    out: List[str] = []
    cond_no = pc.get("condition_number")
    if cond_no is not None:
        out.append(f"Condition number: {cond_no}")
    items = pc.get("items") or []
    if isinstance(items, list):
        for it in items:
            if not isinstance(it, dict):
                continue
            num = it.get("num")
            txt = it.get("text") or ""
            basis = it.get("basis") or []
            header = f"- Item {num}" if num is not None else "- Item"
            out.append(header)
            if isinstance(txt, str) and txt.strip():
                out.append(txt.strip())
            if isinstance(basis, list) and basis:
                out.append("Basis: " + ", ".join(str(b).strip() for b in basis if str(b).strip()))
            out.append("")
    return "\n".join(out).strip()


def json_eval_to_md(obj: Dict[str, Any], source_path: Path) -> str:
    app = str(obj.get("application_number") or "").strip()
    plant = obj.get("plant") or {}
    plant_id = plant.get("plant_id")
    plant_name = plant.get("name") or ""
    plant_address = plant.get("address") or ""
    eval_date = obj.get("evaluation_date")
    project_title = obj.get("project_title")
    source_pdf = ((obj.get("source") or {}).get("pdf")) or ""

    lines: List[str] = []
    lines.append("---")
    lines.append(f"application_number: {app or 'unknown'}")
    if plant_id is not None:
        lines.append(f"plant_id: {plant_id}")
    if plant_name:
        lines.append(f"plant_name: {plant_name}")
    if plant_address:
        lines.append(f"plant_address: {plant_address}")
    if eval_date:
        lines.append(f"evaluation_date: {eval_date}")
    if project_title:
        lines.append(f"project_title: {project_title}")
    if source_pdf:
        lines.append(f"source_pdf: {source_pdf}")
    lines.append(f"source_json: {source_path.as_posix()}")
    lines.append("---")
    lines.append("")
    lines.append(f"# Engineering Evaluation (Application {app or 'unknown'})")
    if project_title:
        lines.append(f"**Project Title**: {project_title}")
    if plant_id or plant_name:
        lines.append(f"**Plant**: {_norm_space(str(plant_id or ''))} {_norm_space(str(plant_name))}".strip())
    if plant_address:
        lines.append(f"**Address**: {_norm_space(str(plant_address))}")
    if eval_date:
        lines.append(f"**Evaluation Date**: {eval_date}")
    lines.append("")

    for section_key, jsonpath in SECTION_ORDER:
        lines.append(f"## {section_key}")
        lines.append(f"JSONPath: `{jsonpath}`")
        lines.append("")

        if section_key == "Statement_of_Compliance":
            txt = _render_statement_of_compliance(obj.get("Statement_of_Compliance"))
        elif section_key == "permit_conditions":
            txt = _render_permit_conditions(obj.get("permit_conditions"))
        else:
            txt = _json_get_text(obj, section_key)
        if txt.strip():
            lines.append(txt.strip())
        else:
            lines.append("(empty)")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def build_corpus(json_folders: List[Path], out_folder: Path) -> int:
    out_folder.mkdir(parents=True, exist_ok=True)
    written = 0
    skipped = 0

    for folder in json_folders:
        if not folder.exists():
            print(f"Folder not found: {folder}", file=sys.stderr)
            return 2
        for path in sorted(folder.rglob("*.json")):
            try:
                obj = _read_json(path)
            except Exception:
                continue
            if obj.get("schema_version") not in {"v1.1-barr-custom", "v1.2-barr-custom"}:
                continue
            if "application_number" not in obj:
                continue

            app = str(obj.get("application_number") or "unknown").strip() or "unknown"
            md_name = _safe_filename(f"application_{app}__eval.md")
            out_path = _unique_path(out_folder / md_name)
            out_path.write_text(json_eval_to_md(obj, path), encoding="utf-8")
            written += 1

    if written == 0 and skipped == 0:
        print("No matching v1.1-barr-custom or v1.2-barr-custom JSON files found.", file=sys.stderr)
        return 2

    print(f"Wrote {written} markdown files to: {out_folder}")
    return 0


def run_indexer(context_folder: Path, *, top_k: int, use_dense: bool, ensure_coverage: bool) -> int:
    if not Path(SKILL_RAG_CLI).exists():
        print(f"rag_cli.py not found: {SKILL_RAG_CLI}", file=sys.stderr)
        return 2
    args = [
        sys.executable,
        SKILL_RAG_CLI,
        "index",
        "--context-folder",
        str(context_folder),
        "--top-k",
        str(top_k),
        "--use-dense" if use_dense else "--no-use-dense",
        "--ensure-coverage" if ensure_coverage else "--no-ensure-coverage",
    ]
    p = subprocess.run(args, capture_output=True, text=True)
    if p.returncode != 0:
        sys.stderr.write(p.stderr or "")
        return int(p.returncode)
    sys.stdout.write(p.stdout or "")
    return 0


def _import_rag_core():
    import importlib.util

    core_path = Path(SKILL_RAG_CORE)
    if not core_path.exists():
        raise RuntimeError(f"rag_core.py not found: {core_path}")
    spec = importlib.util.spec_from_file_location("rag_core", core_path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # type: ignore
    return mod


@dataclass
class ProjectSpec:
    application_number: str
    plant_id: Optional[int]
    plant_name: str
    plant_address: str
    project_title: str
    project_description: str
    equipment_ids: List[str]
    project_context_files: List[str]


def _load_project_spec(path: Path) -> ProjectSpec:
    raw = path.read_text(encoding="utf-8")
    if path.suffix.lower() in {".yaml", ".yml"}:
        try:
            import yaml  # type: ignore
        except Exception as e:
            raise RuntimeError("PyYAML is required to read .yaml specs. Install: pip install pyyaml") from e
        data = yaml.safe_load(raw) or {}
    else:
        data = json.loads(raw)

    def get_str(key: str, default: str = "") -> str:
        v = data.get(key)
        return str(v).strip() if v is not None else default

    plant = data.get("plant") or {}
    pid = plant.get("plant_id") if isinstance(plant, dict) else None
    plant_addr = plant.get("address") if isinstance(plant, dict) else None
    try:
        pid_int = int(pid) if pid is not None and str(pid).strip() else None
    except Exception:
        pid_int = None

    eq = data.get("equipment_ids") or []
    if isinstance(eq, str):
        eq_ids = [e.strip() for e in eq.split(",") if e.strip()]
    elif isinstance(eq, list):
        eq_ids = [str(e).strip() for e in eq if str(e).strip()]
    else:
        eq_ids = []

    project_context_files = data.get("project_context_files") or []
    if isinstance(project_context_files, str):
        context_files = [project_context_files.strip()] if project_context_files.strip() else []
    elif isinstance(project_context_files, list):
        context_files = [str(p).strip() for p in project_context_files if str(p).strip()]
    else:
        context_files = []

    return ProjectSpec(
        application_number=get_str("application_number") or "unknown",
        plant_id=pid_int,
        plant_name=get_str("plant_name") or get_str("plant") if isinstance(data.get("plant"), str) else get_str("plant_name"),
        plant_address=str(plant_addr).strip() if plant_addr is not None else get_str("plant_address"),
        project_title=get_str("project_title"),
        project_description=get_str("project_description"),
        equipment_ids=eq_ids,
        project_context_files=context_files,
    )


def _section_question(spec: ProjectSpec, section_key: str) -> str:
    eq = ", ".join(spec.equipment_ids) if spec.equipment_ids else "none"
    pid = str(spec.plant_id) if spec.plant_id is not None else "unknown"
    return (
        f"Provide exemplar writing style and structure for the '{section_key}' section of a BAAD Engineering Evaluation. "
        f"Constraints: plant_id={pid}; equipment_ids={eq}; project_title='{spec.project_title}'. "
        "Write in BAAD staff review voice, using direct declarative statements suitable for BAAD review and finalization. "
        "Do not frame facts as applicant claims or submittal assertions. "
        "Avoid phrases such as 'the applicant states', 'the project description provided by the applicant states', "
        "'the applicant indicates', or similar attribution unless explicitly needed to identify disputed or unsupported information. "
        "Prefer formulations like 'Renewable propane production will not increase as a result of this action.' "
        "Return exemplars that sound like the permits in this corpus."
    )


def _norm_unit_id(unit: str) -> str:
    return re.sub(r"[^A-Za-z0-9]", "", str(unit or "").upper())


def _walk_titlev_nodes(obj: Any, path: str = "$") -> Iterable[Tuple[str, Any]]:
    if isinstance(obj, dict):
        yield path, obj
        for key, value in obj.items():
            yield from _walk_titlev_nodes(value, f"{path}.{key}")
    elif isinstance(obj, list):
        for idx, value in enumerate(obj):
            yield from _walk_titlev_nodes(value, f"{path}[{idx}]")


def _titlev_context_from_json(path: Path, equipment_ids: List[str]) -> str:
    obj = _read_json(path)
    targets = {_norm_unit_id(eid) for eid in equipment_ids if eid}
    if not targets:
        return ""

    lines: List[str] = []
    lines.append(f"## Project Context: {path.name}")

    front = obj.get("front_matter") or []
    if isinstance(front, list) and front:
        front_bits: List[str] = []
        for item in front[:12]:
            if isinstance(item, dict):
                txt = _norm_space(str(item.get("text") or ""))
                if txt:
                    front_bits.append(txt)
        if front_bits:
            lines.append("### Permit Front Matter")
            lines.extend(front_bits[:8])
            lines.append("")

    seen_rows: set[str] = set()
    seen_paras: set[str] = set()
    row_hits = 0
    para_hits = 0

    for node_path, node in _walk_titlev_nodes(obj.get("sections") or []):
        if not isinstance(node, dict):
            continue
        title = _norm_space(str(node.get("title") or ""))

        applicable_units = node.get("applicable_units")
        if isinstance(applicable_units, list):
            units_norm = {_norm_unit_id(u) for u in applicable_units}
            if units_norm & targets:
                txt = _norm_space(str(node.get("text") or ""))
                if txt and txt not in seen_paras and para_hits < 40:
                    seen_paras.add(txt)
                    lines.append(f"### Section Match: {title or node_path}")
                    lines.append(txt)
                    lines.append("")
                    para_hits += 1

        rows = node.get("rows_as_objects")
        if isinstance(rows, list):
            for row in rows:
                if not isinstance(row, dict):
                    continue
                row_text = " ".join(_norm_space(str(v)) for v in row.values() if str(v).strip())
                row_units = row.get("applicable_units") or []
                row_units_norm = {_norm_unit_id(u) for u in row_units} if isinstance(row_units, list) else set()
                row_direct_units = {
                    _norm_unit_id(row.get("unit_id") or ""),
                    _norm_unit_id(row.get("S-#") or ""),
                }
                if targets & (row_units_norm | row_direct_units) or any(t in _norm_unit_id(row_text) for t in targets):
                    sig = f"{title}|{row_text}"
                    if sig in seen_rows or row_hits >= 60:
                        continue
                    seen_rows.add(sig)
                    lines.append(f"### Table Match: {title or node_path}")
                    for key, value in row.items():
                        if key == "applicable_units":
                            continue
                        val = _norm_space(str(value))
                        if val:
                            lines.append(f"- {key}: {val}")
                    lines.append("")
                    row_hits += 1

        txt = _norm_space(str(node.get("text") or ""))
        if txt and any(t in _norm_unit_id(txt) for t in targets):
            if txt not in seen_paras and para_hits < 40:
                seen_paras.add(txt)
                lines.append(f"### Text Match: {title or node_path}")
                lines.append(txt)
                lines.append("")
                para_hits += 1

    if len(lines) <= 1:
        return ""
    return "\n".join(lines).strip() + "\n"


def _build_project_context(spec: ProjectSpec) -> str:
    chunks: List[str] = []
    for raw_path in spec.project_context_files:
        path = Path(raw_path)
        if not path.exists():
            continue
        if path.suffix.lower() == ".json":
            try:
                ctx = _titlev_context_from_json(path, spec.equipment_ids)
            except Exception:
                ctx = ""
            if ctx:
                chunks.append(ctx)
    return "\n".join(c.strip() for c in chunks if c.strip()).strip()


def generate_prompt_packs(
    context_folder: Path,
    spec: ProjectSpec,
    out_folder: Path,
    *,
    top_k: int,
    use_dense: bool,
    ensure_coverage: bool,
) -> Dict[str, Path]:
    rc = _import_rag_core()
    docs, cache = rc.load_documents_cached(str(context_folder), enable_ocr=False)
    embedder = rc.get_embedder(rc.DEFAULT_EMBEDDER_MODEL) if use_dense else None
    rc.ensure_embeddings(docs, cache, str(context_folder), embedder, embedder_model=rc.DEFAULT_EMBEDDER_MODEL)

    out_folder.mkdir(parents=True, exist_ok=True)
    prompts: Dict[str, Path] = {}
    project_context = _build_project_context(spec)

    for section_key, _jsonpath in SECTION_ORDER:
        q = _section_question(spec, section_key)

        if ensure_coverage and len(docs) > 0:
            selected_doc_idxs = list(range(len(docs)))
        else:
            doc_top_k = min(max(top_k * 4, 10), max(1, len(docs)))
            selected_doc_idxs = rc.retrieve_docs(docs, q, top_k=doc_top_k, embedder=embedder)

        chunks, chunk_embs = rc.build_chunk_index(
            docs, selected_doc_idxs, include_embeddings=embedder is not None
        )
        if ensure_coverage:
            selected = rc.retrieve_with_coverage(
                chunks,
                chunk_embs,
                q,
                top_k=top_k,
                embedder=embedder,
                min_per_doc=1,
            )
        else:
            selected = rc.retrieve_hybrid(chunks, chunk_embs, q, top_k=top_k, embedder=embedder)

        job_id = f"{spec.application_number}-{section_key}"
        prompt_txt = rc.build_query_txt(job_id, q, selected, str(context_folder))
        if project_context:
            prompt_txt = prompt_txt.rstrip() + "\n\n### PROJECT_CONTEXT\n" + project_context
        out_path = out_folder / f"{_safe_filename(section_key)}.prompt.txt"
        out_path.write_text(prompt_txt, encoding="utf-8")
        prompts[section_key] = out_path

    return prompts


def new_eval_json_skeleton(spec: ProjectSpec) -> Dict[str, Any]:
    now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    return {
        "schema_version": "v1.2-barr-custom",
        "source": {
            "type": "generated",
            "created_local": now,
        },
        "application_number": spec.application_number,
        "plant": {"name": spec.plant_name or "", "plant_id": spec.plant_id, "address": spec.plant_address or ""},
        "evaluation_date": None,
        "permit_date": None,
        "project_title": spec.project_title or None,
        "equipment": [{"id": e, "description": ""} for e in spec.equipment_ids],
        "background": {"text": ""},
        "emission_calculations": {"text": ""},
        "cumulative_increase": {"text": ""},
        "emissions": {
            "common_fugitives": {
                "narrative": "",
                "predicted_component_counts_table": {
                    "columns": ["Component Type", "Service", "Predicted Count"],
                    "rows": [],
                },
                "permitted_fugitive_totals": {
                    "units": {"lb_per_day": "lb/day", "tpy": "tons/year"},
                    "POC": {"lb_per_day": None, "tpy": None},
                },
            },
            "by_equipment": {},
        },
        "toxic_risk_screening_analysis": {"status": "unknown", "narrative": ""},
        "BACT": {"text": ""},
        "offsets": {
            "narrative": "",
            "table": {
                "columns": ["Pollutant", "Project Increase (tpy)", "Offset Ratio", "Required Offsets (tpy)"],
                "rows": [],
            },
        },
        "PSD_applicability": {"narrative": ""},
        "CEQA": {"narrative": ""},
        "Statement_of_Compliance": {"General": {"findings": []}},
        "public_notification": {"text": ""},
        "conditions": {"text": ""},
        "permit_conditions": {"condition_number": None, "items": []},
        "TitleV_permit": {"narrative": "", "revisions": [], "affected_sources": []},
        "recommendation": {"text": ""},
        "raw_sections": {"preamble": "", "blocks": [], "unmapped_blocks": []},
    }


def cmd_build_corpus(args: argparse.Namespace) -> int:
    folders = [Path(p) for p in (args.json_folder or [])]
    return build_corpus(folders, Path(args.out_folder))


def cmd_index(args: argparse.Namespace) -> int:
    return run_indexer(
        Path(args.context_folder),
        top_k=args.top_k,
        use_dense=args.use_dense,
        ensure_coverage=args.ensure_coverage,
    )


def cmd_generate(args: argparse.Namespace) -> int:
    context_folder = Path(args.context_folder)
    spec = _load_project_spec(Path(args.project_spec))
    out_dir = Path(args.out_folder)
    prompts_dir = out_dir / "_prompts"

    prompts = generate_prompt_packs(
        context_folder,
        spec,
        prompts_dir,
        top_k=args.top_k,
        use_dense=args.use_dense,
        ensure_coverage=args.ensure_coverage,
    )

    out_json = new_eval_json_skeleton(spec)
    out_json["source"]["style_context_folder"] = str(context_folder)
    out_json["source"]["prompt_files"] = {k: str(v) for k, v in prompts.items()}

    out_path = out_dir / f"application_{_safe_filename(spec.application_number)}__eval.json"
    out_path = _unique_path(out_path)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out_json, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(str(out_path))
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Engineering evaluation: JSON->MD corpus, RAG index, and draft generation.")
    sub = p.add_subparsers(dest="cmd", required=True)

    p_c = sub.add_parser("build-corpus", help="Convert evaluation JSONs into a sectioned Markdown style corpus.")
    p_c.add_argument("--json-folder", action="append", required=True, help="Folder containing evaluation JSON files.")
    p_c.add_argument("--out-folder", default="RAG/style_corpus_md", help="Output folder for .md corpus.")
    p_c.set_defaults(func=cmd_build_corpus)

    p_i = sub.add_parser("index", help="Run agentic-rag-indexer to index a context folder.")
    p_i.add_argument("--context-folder", default="RAG/style_corpus_md", help="Folder to index (default: corpus folder).")
    p_i.add_argument("--top-k", type=int, default=6, help="Top-K (passed through).")
    p_i.add_argument("--use-dense", action="store_true", default=False, help="Enable dense retrieval (embeddings).")
    p_i.add_argument("--ensure-coverage", action="store_true", default=True, help="Ensure cross-doc coverage.")
    p_i.set_defaults(func=cmd_index)

    p_g = sub.add_parser("generate", help="Generate a new eval JSON skeleton + per-section prompt packs from exemplars.")
    p_g.add_argument("--context-folder", default="RAG/style_corpus_md", help="Indexed corpus folder.")
    p_g.add_argument("--project-spec", required=True, help="Project spec .json or .yaml.")
    p_g.add_argument("--out-folder", default="generated", help="Output folder for JSON + prompts.")
    p_g.add_argument("--top-k", type=int, default=6, help="Top-K exemplar chunks per section.")
    p_g.add_argument("--use-dense", action="store_true", default=False, help="Enable dense retrieval (embeddings).")
    p_g.add_argument("--ensure-coverage", action="store_true", default=True, help="Ensure cross-doc coverage.")
    p_g.set_defaults(func=cmd_generate)

    return p


def main(argv: Optional[List[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
