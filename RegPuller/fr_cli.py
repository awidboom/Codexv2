import argparse
import json
import os
import re
import sys
from typing import Dict, List, Set

import download_regs


def parse_citations_from_text(text: str) -> List[str]:
    return re.findall(r"\b\d+\s+FR\s+\d+\b", text)


def load_citations(citations_arg: str, citations_file: str) -> List[str]:
    citations: Set[str] = set()
    if citations_arg:
        for item in parse_citations_from_text(citations_arg):
            citations.add(item)
    if citations_file:
        try:
            with open(citations_file, "r", encoding="utf-8") as f:
                for line in f:
                    for item in parse_citations_from_text(line):
                        citations.add(item)
        except OSError as exc:
            print(f"Failed to read citations file: {exc}", file=sys.stderr)
            return []
    return sorted(citations)


def main() -> int:
    parser = argparse.ArgumentParser(description="Federal Register CLI: download FR documents by citation.")
    parser.add_argument(
        "--citations",
        default="",
        help="Citations to download (e.g., \"60 FR 48399, 84 FR 36304\")",
    )
    parser.add_argument("--citations-file", default="", help="Text file with FR citations")
    parser.add_argument("--out-dir", default="data", help="Output directory (default: data)")
    parser.add_argument(
        "--date",
        default="",
        help="Optional publication date (YYYY-MM-DD) applied to all citations",
    )
    parser.add_argument("--role", default="custom", help="Role label for saved file names")
    parser.add_argument("--json", action="store_true", help="Print JSON output")
    args = parser.parse_args()

    citations = load_citations(args.citations, args.citations_file)
    if not citations:
        print("No citations provided.", file=sys.stderr)
        return 2
    iso_date = args.date.strip()
    downloads: List[Dict[str, str]] = []
    missing: List[str] = []
    for cite in citations:
        info = download_regs.download_fr_doc_by_citation(cite, args.role, args.out_dir, iso_date)
        if info:
            downloads.append(info)
        else:
            missing.append(cite)

    if args.json:
        print(json.dumps({"downloads": downloads, "missing": missing}, indent=2))
    else:
        print(f"Downloaded {len(downloads)} file(s).")
        for item in downloads:
            print(f"- {item.get('path')}")
        if missing:
            print("Missing:")
            for cite in missing:
                print(f"- {cite}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
