#!/usr/bin/env python
"""
Build a single-file version of viz/permits_dashboard.html by embedding a CSV as base64.

Example:
  python viz/build_single_file_dashboard.py --csv permits_all.csv

Notes:
  - The dashboard JS looks for <script id="embeddedPermitsCsvB64">...</script>.
  - We embed base64 (utf-8 bytes) to avoid HTML escaping issues.
"""

from __future__ import annotations

import argparse
import base64
import re
from pathlib import Path


MARKER_ID = "embeddedPermitsCsvB64"


def _embed_base64(html_text: str, b64: str) -> str:
    pattern = re.compile(
        rf'(<script\s+id="{re.escape(MARKER_ID)}"\s+type="text/plain"\s*>)(.*?)(</script>)',
        flags=re.IGNORECASE | re.DOTALL,
    )
    m = pattern.search(html_text)
    if not m:
        raise SystemExit(f"Could not find embed marker <script id=\"{MARKER_ID}\" ...></script> in HTML input.")
    return html_text[: m.start(2)] + b64 + html_text[m.end(2) :]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--html-in", default="viz/permits_dashboard.html", help="Path to the dashboard HTML template")
    ap.add_argument("--csv", required=True, help="Path to the permits CSV to embed")
    ap.add_argument(
        "--out",
        default="viz/permits_dashboard_single.html",
        help="Output path for the single-file dashboard HTML",
    )
    args = ap.parse_args()

    html_in = Path(args.html_in)
    csv_path = Path(args.csv)
    out_path = Path(args.out)

    html_text = html_in.read_text(encoding="utf-8")
    csv_bytes = csv_path.read_bytes()
    b64 = base64.b64encode(csv_bytes).decode("ascii")

    out_text = _embed_base64(html_text, b64)
    out_path.write_text(out_text, encoding="utf-8")
    print(f"Wrote {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

