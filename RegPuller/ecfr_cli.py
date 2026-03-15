import argparse
import json
import os
import sys
from typing import Dict, List, Tuple

import download_regs


def extract_precedents(xml_text: str) -> Tuple[List[str], Dict[str, str], List[Dict[str, str]]]:
    return download_regs.extract_fr_citations_from_ecfr_xml_with_provenance(xml_text)


def load_rule_xml(rule_url: str, out_dir: str, rule_title: str = "") -> Dict[str, str]:
    rule_html, title, rule_dir, rule_path = download_regs.download_rule(rule_url, out_dir)
    if rule_title:
        title = rule_title
    hierarchy = download_regs.parse_ecfr_hierarchy(rule_url)
    ecfr_date = ""
    if hierarchy.get("title"):
        ecfr_date = download_regs.get_ecfr_title_date(hierarchy["title"]) or ""
    return {
        "rule_url": rule_url,
        "rule_title": title,
        "rule_dir": rule_dir,
        "rule_file": rule_path,
        "ecfr_date": ecfr_date,
    }


def read_xml(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def print_precedents(citations: List[str], dates: Dict[str, str]) -> None:
    for cite in citations:
        date_str = dates.get(cite, "")
        suffix = f" | {date_str}" if date_str else ""
        print(f"{cite}{suffix}")


def main() -> int:
    parser = argparse.ArgumentParser(description="eCFR CLI: download rule XML or extract FR precedents.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    download_parser = subparsers.add_parser("download", help="Download eCFR rule XML")
    download_parser.add_argument("--url", required=True, help="eCFR rule URL")
    download_parser.add_argument("--out-dir", default="data", help="Output directory (default: data)")
    download_parser.add_argument("--rule-title", default="", help="Optional override for rule title")
    download_parser.add_argument("--json", action="store_true", help="Print result JSON to stdout")

    prec_parser = subparsers.add_parser("precedents", help="Extract FR precedents from eCFR XML")
    prec_parser.add_argument("--rule-xml", default="", help="Path to rule XML")
    prec_parser.add_argument("--url", default="", help="Rule URL (downloads XML first)")
    prec_parser.add_argument("--out-dir", default="data", help="Output directory (default: data)")
    prec_parser.add_argument("--rule-title", default="", help="Optional override for rule title")
    prec_parser.add_argument("--json", action="store_true", help="Print JSON output")
    prec_parser.add_argument("--out", default="", help="Write output to a file")

    args = parser.parse_args()

    if args.command == "download":
        result = load_rule_xml(args.url, args.out_dir, args.rule_title)
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"Rule title: {result.get('rule_title')}")
            print(f"Rule file: {result.get('rule_file')}")
            if result.get("ecfr_date"):
                print(f"eCFR date: {result.get('ecfr_date')}")
        return 0

    if args.command == "precedents":
        rule_xml_path = args.rule_xml
        if not rule_xml_path and args.url:
            result = load_rule_xml(args.url, args.out_dir, args.rule_title)
            rule_xml_path = result.get("rule_file", "")
        if not rule_xml_path:
            print("Provide --rule-xml or --url for precedents.", file=sys.stderr)
            return 2
        if not os.path.exists(rule_xml_path):
            print(f"Rule XML not found: {rule_xml_path}", file=sys.stderr)
            return 2
        xml_text = read_xml(rule_xml_path)
        citations, dates, provenance = extract_precedents(xml_text)
        payload = {"citations": citations, "dates": dates, "provenance": provenance}
        if args.out:
            with open(args.out, "w", encoding="utf-8") as f:
                if args.json or args.out.lower().endswith(".json"):
                    json.dump(payload, f, indent=2)
                else:
                    for cite in citations:
                        date_str = dates.get(cite, "")
                        suffix = f" | {date_str}" if date_str else ""
                        f.write(f"{cite}{suffix}\n")
        if args.json:
            print(json.dumps(payload, indent=2))
        else:
            print_precedents(citations, dates)
        return 0

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
