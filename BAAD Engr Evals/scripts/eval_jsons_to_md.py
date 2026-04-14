#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path

from eval_rag_cli import json_eval_to_md


def convert_tree(in_root: Path, out_root: Path) -> int:
    if not in_root.exists():
        print(f"Input folder not found: {in_root}", file=sys.stderr)
        return 2

    out_root.mkdir(parents=True, exist_ok=True)
    written = 0

    for path in sorted(in_root.rglob("*.json")):
        try:
            obj = json.loads(path.read_text(encoding="utf-8-sig"))
        except Exception as exc:
            print(f"Skipping unreadable JSON: {path} ({exc})", file=sys.stderr)
            continue

        if obj.get("schema_version") not in {"v1.1-barr-custom", "v1.2-barr-custom"}:
            continue

        rel = path.relative_to(in_root)
        out_path = out_root / rel.with_suffix(".md")
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json_eval_to_md(obj, path), encoding="utf-8")
        written += 1

    print(f"Wrote {written} markdown files to {out_root}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Convert engineering evaluation JSON trees to Markdown trees.")
    parser.add_argument("input", help="Input folder containing evaluation JSON files")
    parser.add_argument("output", help="Output folder for Markdown files")
    args = parser.parse_args()
    return convert_tree(Path(args.input), Path(args.output))


if __name__ == "__main__":
    raise SystemExit(main())
