# cdphe_report
import csv
import html
import json
import urllib.parse
from base64 import b64encode
from collections import defaultdict
from datetime import datetime
from pathlib import Path

DOWNLOAD_DIR = Path(__file__).resolve().parent / "downloads"
INPUT_CSV = DOWNLOAD_DIR / "cdphe_enforcement_summary.csv"
OUTPUT_HTML = DOWNLOAD_DIR / "cdphe_enforcement_summary_report.html"


def parse_date(value: str):
    value = (value or "").strip()
    if not value:
        return None
    for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%m/%d/%y"):
        try:
            return datetime.strptime(value, fmt).date()
        except ValueError:
            continue
    return None


def date_range(dates) -> str:
    cleaned = sorted([d for d in dates if d])
    if not cleaned:
        return "Unknown"
    if len(cleaned) == 1:
        return cleaned[0].isoformat()
    return f"{cleaned[0].isoformat()} to {cleaned[-1].isoformat()}"


def wrap_label(label: str, max_len: int = 22) -> list[str]:
    words = label.split()
    if not words:
        return [label]
    lines = []
    current = []
    for word in words:
        if len(" ".join(current + [word])) <= max_len or not current:
            current.append(word)
            continue
        lines.append(" ".join(current))
        current = [word]
    if current:
        lines.append(" ".join(current))
    if len(lines) > 2:
        lines = [lines[0], " ".join(lines[1:])]
    return lines


def build_bar_chart(title: str, items: list[tuple[str, int]], color: str, link_param: str | None = None) -> str:
    if not items:
        items = [("Unknown", 0)]
    max_count = max(count for _, count in items) or 1
    rows = []
    y = 32
    for idx, (label, count) in enumerate(items):
        lines = wrap_label(label)
        bar_width = 380.0 * (count / max_count)
        label_text = html.escape(label)
        link = ""
        label_markup = label_text
        if link_param:
            href = f"?{link_param}={urllib.parse.quote(label)}"
            link = f"<a href='{href}' class='chart-link'>"
            label_markup = f"{link}{label_text}</a>"
        label_lines = []
        for line_idx, line in enumerate(lines):
            escaped = html.escape(line)
            if link_param:
                escaped = f"{link}{escaped}</a>"
            if line_idx == 0:
                label_lines.append(f"<tspan x='12' dy='0'>{escaped}</tspan>")
            else:
                label_lines.append(f"<tspan x='12' dy='12'>{escaped}</tspan>")
        rows.append(
            f"<text x='12' y='{y + 14}' class='chart-label'>{''.join(label_lines)}</text>"
            f"<rect x='160' y='{y}' width='{bar_width:.1f}' height='16' rx='4' fill='{color}' />"
            f"<text x='{160 + bar_width + 6:.1f}' y='{y + 14}' class='chart-value'>{count}</text>"
        )
        y += 34 if len(lines) > 1 else 24
    height = y + 16
    return (
        "<svg viewBox='0 0 560 {height}' class='chart'>"
        "<text x='12' y='20' class='chart-title'>{title}</text>{rows}</svg>"
    ).format(height=height, title=html.escape(title), rows="".join(rows))


def build_pie_chart(title: str, items: list[tuple[str, int]], link_param: str | None = None) -> str:
    if not items:
        items = [("Unknown", 1)]
    total = sum(count for _, count in items) or 1
    colors = [
        "var(--pine)",
        "var(--sage)",
        "var(--sky)",
        "var(--rust)",
        "#5f7f8f",
        "#90a4ae",
        "#b0bec5",
        "#7aa6b6",
    ]
    center_x = 120
    center_y = 78
    radius = 56
    start_angle = -90.0
    slices = []
    legend = []
    for idx, (label, count) in enumerate(items):
        portion = count / total
        sweep = portion * 360.0
        end_angle = start_angle + sweep
        color = colors[idx % len(colors)]
        large_arc = 1 if sweep > 180 else 0
        start_x = center_x + radius * __import__("math").cos(__import__("math").radians(start_angle))
        start_y = center_y + radius * __import__("math").sin(__import__("math").radians(start_angle))
        end_x = center_x + radius * __import__("math").cos(__import__("math").radians(end_angle))
        end_y = center_y + radius * __import__("math").sin(__import__("math").radians(end_angle))
        path = (
            f"M {center_x} {center_y} "
            f"L {start_x:.2f} {start_y:.2f} "
            f"A {radius} {radius} 0 {large_arc} 1 {end_x:.2f} {end_y:.2f} Z"
        )
        slices.append(f"<path d='{path}' fill='{color}'></path>")
        pct = round(portion * 100)
        label_text = html.escape(label)
        if link_param:
            href = f"?{link_param}={urllib.parse.quote(label)}"
            label_text = f"<a href='{href}' class='legend-link'>{label_text}</a>"
        legend.append(
            f"<div class='legend-row'>"
            f"<span class='legend-swatch' style='background:{color}'></span>"
            f"<span class='legend-label'>{label_text}</span>"
            f"<span class='legend-value'>{count} ({pct}%)</span>"
            f"</div>"
        )
        start_angle = end_angle
    return (
        "<div class='pie-wrap'>"
        "<svg viewBox='0 0 260 156' class='pie'>"
        "<text x='12' y='18' class='chart-title'>{title}</text>"
        "<g>{slices}</g>"
        "</svg>"
        "<div class='legend'>{legend}</div>"
        "</div>"
    ).format(title=html.escape(title), slices="".join(slices), legend="".join(legend))


def tally_split(values, fallback: str) -> dict:
    counts = defaultdict(int)
    for value in values:
        parts = [p.strip() for p in (value or "").split(";") if p.strip()]
        if not parts:
            parts = [fallback]
        for part in parts:
            counts[part] += 1
    return counts


def top_n(counts: dict, n: int) -> list[tuple[str, int]]:
    return sorted(counts.items(), key=lambda x: (-x[1], x[0].lower()))[:n]


def main() -> None:
    if not INPUT_CSV.exists():
        print(f"Missing input CSV: {INPUT_CSV}")
        return

    with INPUT_CSV.open("r", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))

    if not rows:
        print("No records found in CSV.")
        return

    case_ids = []
    doc_dates = []
    companies = set()
    enforcement_case_map = defaultdict(set)

    category_values = []
    source_values = []
    company_counts = defaultdict(int)
    equipment_values = []

    for row in rows:
        case_id = (row.get("case_number") or "").strip() or (row.get("file_name") or "").strip()
        if case_id:
            case_ids.append(case_id)
        doc_dates.append(parse_date(row.get("document_date")))
        company = (row.get("company") or "").strip()
        if company:
            companies.add(company)
            company_counts[company] += 1

        enforcement_type = (row.get("enforcement_type") or "").strip() or "Unknown"
        if case_id:
            enforcement_case_map[enforcement_type].add(case_id)

        category_values.append(row.get("category") or "")
        equipment_values.append(row.get("equipment_type") or "")
        source_values.append(row.get("source_type") or "Unknown")

    total_violations = len(rows)
    total_cases = len(set(case_ids))
    enforcement_counts = {k: len(v) for k, v in enforcement_case_map.items()}

    enforcement_items = top_n(enforcement_counts, 8)
    category_counts = tally_split(category_values, "uncategorized")
    source_counts = tally_split(source_values, "Unknown")
    category_items = sorted(category_counts.items(), key=lambda x: (-x[1], x[0].lower()))
    source_items = sorted(source_counts.items(), key=lambda x: (-x[1], x[0].lower()))[:10]
    company_items = top_n(company_counts, 6)
    equipment_items = top_n(tally_split(equipment_values, "Unknown"), 6)

    detail_rows = []
    for row in rows:
        detail_rows.append(
            {
                "file_name": row.get("file_name", ""),
                "document_date": row.get("document_date", ""),
                "pdf_url": row.get("pdf_url", ""),
                "company": row.get("company", ""),
                "case_number": row.get("case_number", ""),
                "enforcement_type": row.get("enforcement_type", ""),
                "monetary_penalty": row.get("monetary_penalty", ""),
                "category": row.get("category", ""),
                "source_type": row.get("source_type", ""),
                "equipment_type": row.get("equipment_type", ""),
                "rule_citation": row.get("rule_citation", ""),
                "violation_description": row.get("violation_description", ""),
            }
        )

    logo_svg_path = Path(__file__).resolve().parent / "assets" / "barr_logo_primary_blue.svg"
    logo_html = ""
    if logo_svg_path.exists():
        encoded = b64encode(logo_svg_path.read_bytes()).decode("ascii")
        logo_src = f"data:image/svg+xml;base64,{encoded}"
        logo_html = f'<img src="{logo_src}" alt="Barr logo" />'

    html_out = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>CDPHE Enforcement Summary</title>
<style>
:root {{
  --ink: #1b2b34;
  --muted: #52616b;
  --barr-blue: #0072bc;
  --barr-blue-dark: #005a9c;
  --barr-blue-light: #a9d4f2;
  --pine: #0f4c5c;
  --sage: #1f6f8b;
  --rust: #d9792b;
  --sand: #eef2f3;
  --clay: #d7dee2;
  --sky: #2a9d8f;
  --card: #ffffff;
  --bg: #f4f7f9;
  --line: #dfe6ea;
  --shadow: rgba(14,35,46,0.08);
}}
* {{ box-sizing: border-box; }}
body {{
  margin: 0;
  font-family: "Avenir Next", "Segoe UI", "Helvetica Neue", Arial, sans-serif;
  color: var(--ink);
  background:
    radial-gradient(circle at 15% -10%, #ffffff 0%, var(--sand) 40%, var(--bg) 75%),
    linear-gradient(135deg, rgba(15,76,92,0.08), rgba(42,157,143,0.08)),
    repeating-linear-gradient(135deg, rgba(0,114,188,0.12) 0 2px, rgba(0,114,188,0) 2px 18px);
}}
.header {{
  padding: 34px 28px 20px;
  background:
    linear-gradient(120deg, #ffffff 0%, #eef3f6 45%, #f5f8fa 100%),
    radial-gradient(circle at 90% 20%, rgba(31,111,139,0.18), rgba(31,111,139,0) 60%);
  border-bottom: 1px solid var(--line);
  position: relative;
  overflow: hidden;
}}
.header-band {{
  position: absolute;
  left: 0;
  top: 0;
  width: 100%;
  height: 6px;
  background: linear-gradient(90deg, var(--barr-blue), var(--barr-blue-dark));
}}
.header-band.secondary {{
  top: 8px;
  height: 2px;
  opacity: 0.55;
  background: linear-gradient(90deg, var(--barr-blue-light), var(--barr-blue));
}}
.header:after {{
  content: "";
  position: absolute;
  right: -40px;
  top: -30px;
  width: 220px;
  height: 220px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(31,111,139,0.25), rgba(31,111,139,0));
}}
.header:before {{
  content: "";
  position: absolute;
  left: -60px;
  bottom: -120px;
  width: 240px;
  height: 240px;
  border-radius: 36% 64% 50% 50%;
  background: radial-gradient(circle, rgba(217,121,43,0.18), rgba(217,121,43,0));
}}
.title {{
  font-size: 30px;
  letter-spacing: 0.2px;
  margin: 0 0 6px 0;
  font-weight: 600;
}}
.logo {{
  display: inline-flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 10px;
}}
.logo img {{
  height: 28px;
  width: auto;
  display: block;
}}
.subtitle {{
  color: var(--muted);
  margin: 0;
  font-size: 14px;
}}
.container {{
  padding: 18px 24px 28px;
}}
.badge-row {{
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  margin: 10px 0 6px 0;
}}
.badge {{
  border: 1px solid var(--line);
  background: #f6fbfd;
  padding: 6px 10px;
  border-radius: 999px;
  font-size: 11px;
  color: var(--muted);
  text-transform: uppercase;
  letter-spacing: 0.08em;
}}
.kpis {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
  gap: 12px;
  margin-bottom: 18px;
}}
.kpi {{
  background: var(--card);
  border: 1px solid var(--line);
  border-radius: 12px;
  padding: 12px 14px;
  box-shadow: 0 8px 18px var(--shadow);
  position: relative;
  overflow: hidden;
}}
.kpi:after {{
  content: "";
  position: absolute;
  left: 0;
  top: 0;
  width: 100%;
  height: 3px;
  background: linear-gradient(90deg, var(--pine), var(--sky));
  opacity: 0.7;
}}
.kpi-label {{
  font-size: 12px;
  color: var(--muted);
  text-transform: uppercase;
  letter-spacing: 0.08em;
}}
.kpi-value {{
  font-size: 22px;
  margin-top: 4px;
}}
.grid {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 16px;
  margin-bottom: 16px;
}}
.card {{
  background: var(--card);
  border: 1px solid var(--line);
  border-radius: 14px;
  padding: 12px 14px;
  box-shadow: 0 8px 18px var(--shadow);
  position: relative;
  overflow: hidden;
}}
.card:before {{
  content: "";
  position: absolute;
  right: -60px;
  top: -80px;
  width: 160px;
  height: 160px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(0,114,188,0.18), rgba(0,114,188,0));
}}
.chart {{
  width: 100%;
  height: auto;
}}
.pie-wrap {{
  display: grid;
  grid-template-columns: 1fr;
  gap: 8px;
}}
.pie {{
  width: 100%;
  height: auto;
}}
.legend {{
  display: grid;
  gap: 6px;
  font-size: 11px;
}}
.legend-row {{
  display: grid;
  grid-template-columns: 12px 1fr auto;
  align-items: center;
  gap: 8px;
}}
.legend-swatch {{
  width: 10px;
  height: 10px;
  border-radius: 50%;
}}
.legend-label {{
  color: var(--muted);
}}
.legend-value {{
  color: var(--ink);
}}
.chart-title {{
  font-size: 12px;
  fill: var(--ink);
  font-weight: bold;
}}
.chart-label {{
  font-size: 11px;
  fill: var(--muted);
}}
.chart-link {{
  fill: var(--muted);
  text-decoration: underline;
}}
.legend-link {{
  color: var(--muted);
  text-decoration: underline;
}}
.chart-value {{
  font-size: 10px;
  fill: var(--ink);
}}
.table-wrap {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 16px;
}}
.full-width {{
  grid-column: 1 / -1;
}}
.trend-card {{
  padding: 12px 14px;
}}
.trend-controls {{
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  align-items: center;
  margin-bottom: 10px;
  font-size: 12px;
}}
.trend-controls label {{
  color: var(--muted);
  text-transform: uppercase;
  letter-spacing: 0.08em;
  font-size: 11px;
}}
.trend-controls select {{
  border: 1px solid var(--line);
  border-radius: 8px;
  padding: 4px 8px;
  font-size: 12px;
}}
.trend-chart {{
  width: 100%;
  overflow-x: auto;
}}
.trend-legend {{
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  font-size: 11px;
  color: var(--muted);
  margin-top: 8px;
}}
.legend-swatch {{
  display: inline-block;
  width: 10px;
  height: 10px;
  border-radius: 999px;
  margin-right: 6px;
}}
.table {{
  width: 100%;
  border-collapse: collapse;
  font-size: 12px;
}}
.table th {{
  text-align: left;
  padding: 8px 6px;
  border-bottom: 1px solid var(--line);
  color: var(--muted);
  text-transform: uppercase;
  letter-spacing: 0.06em;
}}
.table td {{
  padding: 6px;
  border-bottom: 1px solid #eef2f3;
}}
.detail {{
  margin-top: 18px;
}}
.detail-title {{
  font-size: 16px;
  margin: 0 0 6px 0;
}}
.detail-subtitle {{
  color: var(--muted);
  font-size: 12px;
  margin: 0 0 10px 0;
}}
.filters {{
  display: grid;
  gap: 12px;
  margin-bottom: 14px;
}}
.filters-header {{
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  align-items: center;
}}
.chip {{
  border: 1px solid var(--line);
  padding: 4px 10px;
  border-radius: 999px;
  font-size: 11px;
  background: #ffffff;
}}
.chip a {{
  color: var(--muted);
  text-decoration: none;
}}
.filter-group {{
  border: 1px solid var(--line);
  border-radius: 12px;
  padding: 10px 12px;
  background: #ffffff;
}}
.filter-title {{
  font-size: 12px;
  margin: 0 0 8px 0;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--muted);
}}
.filter-options {{
  display: grid;
  gap: 6px;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
}}
.filter-option {{
  display: flex;
  gap: 8px;
  align-items: center;
  font-size: 12px;
  color: var(--ink);
}}
.filter-option input {{
  accent-color: var(--barr-blue);
}}
.filter-count {{
  color: var(--muted);
  font-size: 11px;
}}
.filter-clear {{
  border: 1px solid var(--line);
  padding: 4px 10px;
  border-radius: 999px;
  font-size: 11px;
  background: #f8fafb;
  color: var(--muted);
  text-decoration: none;
}}
.date-range {{
  display: grid;
  gap: 8px;
}}
.date-range-row {{
  display: flex;
  gap: 10px;
  align-items: center;
  font-size: 12px;
}}
.date-range input[type="range"] {{
  flex: 1;
  accent-color: var(--barr-blue);
}}
.date-range input[type="date"] {{
  border: 1px solid var(--line);
  border-radius: 6px;
  padding: 4px 6px;
  font-size: 12px;
}}
.section-title {{
  font-size: 14px;
  margin: 12px 0 6px 0;
}}
.link {{
  color: var(--barr-blue);
  text-decoration: underline;
  font-size: 12px;
}}
.footer-note {{
  margin-top: 14px;
  font-size: 11px;
  color: var(--muted);
}}
@media (max-width: 720px) {{
  .header {{ padding: 24px 18px 14px; }}
  .container {{ padding: 14px 18px 22px; }}
  .title {{ font-size: 22px; }}
}}
</style>
</head>
<body>
  <div class="header">
    <div class="header-band"></div>
    <div class="header-band secondary"></div>
    <div class="logo">
      {logo_html}
    </div>
    <h1 class="title">CDPHE Enforcement Summary (Pilot)</h1>
  </div>

  <div class="container">
    <div class="kpis">
      <div class="kpi">
        <div class="kpi-label">Alleged Violations</div>
        <div class="kpi-value">{total_violations}</div>
      </div>
      <div class="kpi">
        <div class="kpi-label">Cases</div>
        <div class="kpi-value">{total_cases}</div>
      </div>
      <div class="kpi">
        <div class="kpi-label">Companies</div>
        <div class="kpi-value">{len(companies)}</div>
      </div>
      <div class="kpi">
        <div class="kpi-label">Document Dates</div>
        <div class="kpi-value">{date_range(doc_dates)}</div>
      </div>
    </div>

    <div class="grid">
      <div class="card">{build_pie_chart("Enforcement Types", enforcement_items, "enforcement_type")}</div>
      <div class="card">{build_bar_chart("Top Violation Categories", category_items, "var(--rust)", "category")}</div>
      <div class="card">{build_bar_chart("Top Source Types", source_items, "var(--barr-blue)", "source_type")}</div>
    </div>

    <div class="table-wrap">
      <div class="card full-width">
        <h3 style="margin:0 0 8px 0; font-size:14px;">Monetary Penalties (by case)</h3>
        <table class="table">
          <thead>
            <tr><th>Date</th><th>Company</th><th>Case</th><th>Penalty</th></tr>
          </thead>
          <tbody id="penalty-table"></tbody>
        </table>
      </div>
    </div>

    <!--DETAIL_SECTION-->

    <div class="footer-note">
      Enforcement types are counted by case to avoid double-counting line items.
    </div>
  </div>
  <!--DETAIL_SCRIPT-->
</body>
</html>
"""

    detail_section = """<div class="detail">
      <h2 class="detail-title">Drill-down Detail</h2>
      <p class="detail-subtitle">Click any item above to filter the detail below.</p>
      <div id="filters" class="filters"></div>

      <div class="kpis">
        <div class="kpi">
          <div class="kpi-label">Alleged Violations</div>
          <div class="kpi-value" id="kpi-violations">0</div>
        </div>
        <div class="kpi">
          <div class="kpi-label">Cases</div>
          <div class="kpi-value" id="kpi-cases">0</div>
        </div>
        <div class="kpi">
          <div class="kpi-label">Companies</div>
          <div class="kpi-value" id="kpi-companies">0</div>
        </div>
        <div class="kpi">
          <div class="kpi-label">Document Dates</div>
          <div class="date-range" id="date-range"></div>
          <div class="kpi-value" id="kpi-docdates">Unknown</div>
        </div>
      </div>

      <div class="table-wrap">
        <div class="card full-width trend-card">
          <div class="trend-controls">
            <label for="trend-dimension">Trend</label>
            <select id="trend-dimension">
              <option value="company">Company</option>
              <option value="category">Category</option>
              <option value="equipment_type">Equipment Type</option>
              <option value="source_type">Source Type</option>
              <option value="enforcement_type">Enforcement Type</option>
            </select>
          </div>
          <div class="trend-chart" id="trend-chart"></div>
          <div class="trend-legend" id="trend-legend"></div>
        </div>
        <div class="card">
          <h3 class="section-title">Enforcement Types (by case)</h3>
          <table class="table">
            <thead><tr><th>Type</th><th>Cases</th></tr></thead>
            <tbody id="enforcement-table"></tbody>
          </table>
        </div>
        <div class="card">
          <h3 class="section-title">Violation Categories</h3>
          <table class="table">
            <thead><tr><th>Category</th><th>Mentions</th></tr></thead>
            <tbody id="category-table"></tbody>
          </table>
        </div>
        <div class="card">
          <h3 class="section-title">Source Types</h3>
          <table class="table">
            <thead><tr><th>Source</th><th>Mentions</th></tr></thead>
            <tbody id="source-table"></tbody>
          </table>
        </div>
        <div class="card">
          <h3 class="section-title">Equipment Types</h3>
          <table class="table">
            <thead><tr><th>Equipment</th><th>Mentions</th></tr></thead>
            <tbody id="equipment-table"></tbody>
          </table>
        </div>
        <div class="card">
          <h3 class="section-title">Rule Citation(s)</h3>
          <table class="table">
            <thead><tr><th>Citation</th><th>Mentions</th></tr></thead>
            <tbody id="rule-table"></tbody>
          </table>
        </div>
        <div class="card">
          <h3 class="section-title">Top Companies</h3>
          <table class="table">
            <thead><tr><th>Company</th><th>Mentions</th></tr></thead>
            <tbody id="company-table"></tbody>
          </table>
        </div>
        <div class="card full-width">
          <h3 class="section-title">Violations Detail</h3>
          <table class="table">
            <thead>
              <tr>
                <th>Date</th>
                <th>Company</th>
                <th>Case</th>
                <th>Rule Citation(s)</th>
                <th>Violation</th>
              </tr>
            </thead>
            <tbody id="detail-table"></tbody>
          </table>
        </div>
      </div>
    </div>
"""

    detail_script = """<script>
 const DATA = __DATA__;

 let params = new URLSearchParams(window.location.search);
 const FILTER_CONFIG = [
   { key: "enforcement_type", label: "Enforcement Type" },
   { key: "category", label: "Category" },
   { key: "source_type", label: "Source Type" },
  { key: "equipment_type", label: "Equipment Type" },
  { key: "rule_citation", label: "Rule Citation(s)", limit: 25 },
   { key: "company", label: "Company", limit: 25 },
 ];

 function setSearchParams(nextParams) {
   params = nextParams;
   const nextString = nextParams.toString();
   try {
     const nextUrl = nextString ? `?${nextString}` : window.location.pathname;
     window.history.replaceState(null, "", nextUrl);
   } catch (err) {
     // ignore (some hosts restrict history APIs for local/embedded files)
   }
   summarize();
 }

 window.addEventListener("popstate", () => {
   params = new URLSearchParams(window.location.search);
   summarize();
 });

 document.addEventListener("click", (event) => {
   const anchor = event.target.closest("a");
   if (!anchor) return;
   const href = anchor.getAttribute("href") || "";
   if (!href.startsWith("?")) return;
   if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
   if (anchor.target === "_blank") return;
   event.preventDefault();
   const nextParams = new URLSearchParams(href.slice(1));
   setSearchParams(nextParams);
   if (anchor.classList.contains("chart-link")) {
     const detail = document.querySelector(".detail");
     if (detail) detail.scrollIntoView({ behavior: "smooth", block: "start" });
   }
 });

function normalize(value) {
  return (value || "").toLowerCase().trim();
}

function splitParts(value, fallback) {
  const parts = (value || "").split(";").map(p => p.trim()).filter(Boolean);
  return parts.length ? parts : [fallback];
}

function parseDate(value) {
  if (!value) return null;
  if (/\\d{4}-\\d{2}-\\d{2}/.test(value)) return new Date(value + "T00:00:00");
  const m = value.match(/(\\d{1,2})\\/(\\d{1,2})\\/(\\d{2,4})/);
  if (m) {
    const year = m[3].length === 2 ? 2000 + parseInt(m[3], 10) : parseInt(m[3], 10);
    return new Date(year, parseInt(m[1], 10) - 1, parseInt(m[2], 10));
  }
  return null;
}

function parseMoney(value) {
  if (!value) return null;
  const cleaned = String(value).trim();
  const m = cleaned.match(/\\$\\s*([\\d,]+(?:\\.\\d{2})?)/);
  if (!m) return null;
  const num = Number(m[1].replace(/,/g, ""));
  return Number.isFinite(num) ? num : null;
}

function formatDateInput(dateObj) {
  if (!dateObj) return "";
  const yyyy = dateObj.getFullYear();
  const mm = String(dateObj.getMonth() + 1).padStart(2, "0");
  const dd = String(dateObj.getDate()).padStart(2, "0");
  return `${yyyy}-${mm}-${dd}`;
}

function dateToDayIndex(dateObj) {
  return Math.floor(dateObj.getTime() / 86400000);
}

function dayIndexToDate(dayIndex) {
  return new Date(dayIndex * 86400000);
}

function caseId(row) {
  return (row.case_number || "").trim() || (row.file_name || "").trim();
}

function getParamValuesFrom(searchParams, key) {
  const values = searchParams.getAll(key).map(v => v.trim()).filter(Boolean);
  if (values.length) return values;
  const single = searchParams.get(key);
  if (!single) return [];
  return single.split(",").map(v => v.trim()).filter(Boolean);
}

function getActiveFilters(searchParams) {
  const active = {};
  for (const cfg of FILTER_CONFIG) {
    active[cfg.key] = getParamValuesFrom(searchParams, cfg.key);
  }
  return active;
}

function setParamValues(searchParams, key, values) {
  searchParams.delete(key);
  for (const value of values) {
    searchParams.append(key, value);
  }
}

function rowMatches(row) {
  const active = getActiveFilters(params);
  const fromParam = params.get("date_from");
  const toParam = params.get("date_to");
  const rowDate = parseDate(row.document_date);
  if (fromParam || toParam) {
    if (!rowDate) return false;
    const rowDay = dateToDayIndex(rowDate);
    if (fromParam) {
      const fromDay = dateToDayIndex(new Date(fromParam + "T00:00:00"));
      if (rowDay < fromDay) return false;
    }
    if (toParam) {
      const toDay = dateToDayIndex(new Date(toParam + "T00:00:00"));
      if (rowDay > toDay) return false;
    }
  }
  for (const cfg of FILTER_CONFIG) {
    const key = cfg.key;
    const values = active[key];
    if (!values || values.length === 0) continue;
    const targets = values.map(v => normalize(v));
    if (["category", "source_type", "equipment_type", "rule_citation"].includes(key)) {
      const parts = splitParts(row[key], key === "category" ? "uncategorized" : "Unknown")
        .map(p => normalize(p));
      if (!parts.some(p => targets.includes(p))) return false;
    } else {
      const rowValue = normalize((row[key] || "Unknown"));
      if (!targets.includes(rowValue)) return false;
    }
  }
  return true;
}

 function buildLink(key, value) {
   const next = new URLSearchParams(params);
   const current = getParamValuesFrom(next, key);
   const normalized = normalize(value);
  const has = current.some(v => normalize(v) === normalized);
  const remaining = current.filter(v => normalize(v) !== normalized);
  if (!has) remaining.push(value);
  setParamValues(next, key, remaining);
  const nextString = next.toString();
  return nextString ? `?${nextString}` : "?";
}

function fillTable(tableId, items, linkKey) {
  const tbody = document.getElementById(tableId);
  if (!tbody) return;
  tbody.innerHTML = "";
  for (const [label, count] of items) {
    const row = document.createElement("tr");
    const nameCell = document.createElement("td");
    const countCell = document.createElement("td");
    const link = document.createElement("a");
    link.href = buildLink(linkKey, label);
    link.textContent = label;
    nameCell.appendChild(link);
    countCell.textContent = count;
    row.appendChild(nameCell);
    row.appendChild(countCell);
    tbody.appendChild(row);
  }
}

function buildOptions(rows) {
  const options = {};
  for (const cfg of FILTER_CONFIG) {
    const counts = new Map();
    for (const row of rows) {
      if (["category", "source_type", "equipment_type", "rule_citation"].includes(cfg.key)) {
        const parts = splitParts(row[cfg.key], cfg.key === "category" ? "uncategorized" : "Unknown");
        for (const part of parts) {
          counts.set(part, (counts.get(part) || 0) + 1);
        }
      } else {
        const value = (row[cfg.key] || "Unknown").trim() || "Unknown";
        counts.set(value, (counts.get(value) || 0) + 1);
      }
    }
    const items = Array.from(counts.entries())
      .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]));
    options[cfg.key] = cfg.limit ? items.slice(0, cfg.limit) : items;
  }
  return options;
}

function buildCounts(rows) {
  const counts = {};
  for (const cfg of FILTER_CONFIG) {
    counts[cfg.key] = new Map();
  }
  for (const row of rows) {
    for (const cfg of FILTER_CONFIG) {
      if (["category", "source_type", "equipment_type", "rule_citation"].includes(cfg.key)) {
        const parts = splitParts(row[cfg.key], cfg.key === "category" ? "uncategorized" : "Unknown");
        for (const part of parts) {
          const map = counts[cfg.key];
          map.set(part, (map.get(part) || 0) + 1);
        }
      } else {
        const value = (row[cfg.key] || "Unknown").trim() || "Unknown";
        const map = counts[cfg.key];
        map.set(value, (map.get(value) || 0) + 1);
      }
    }
  }
  return counts;
}

const OPTIONS_BY_KEY = buildOptions(DATA);
const DATE_VALUES = DATA.map(r => parseDate(r.document_date)).filter(Boolean);
const DATE_MIN = DATE_VALUES.length ? new Date(Math.min(...DATE_VALUES.map(d => d.getTime()))) : null;
const DATE_MAX = DATE_VALUES.length ? new Date(Math.max(...DATE_VALUES.map(d => d.getTime()))) : null;
const TREND_CONFIG = [
  { key: "company", label: "Company", split: false, limit: 6 },
  { key: "category", label: "Category", split: true, limit: 6 },
  { key: "equipment_type", label: "Equipment Type", split: true, limit: 6 },
  { key: "source_type", label: "Source Type", split: true, limit: 6 },
  { key: "enforcement_type", label: "Enforcement Type", split: false, limit: 6 },
];
const TREND_COLORS = ["#0f4c5c", "#1f6f8b", "#2a9d8f", "#d9792b", "#5f7f8f", "#90a4ae"];
let trendWired = false;

function dateKey(dateObj) {
  return dateObj.toISOString().slice(0, 10);
}

function buildTrendSeries(rows, dimensionKey) {
  const cfg = TREND_CONFIG.find(item => item.key === dimensionKey) || TREND_CONFIG[0];
  const totals = new Map();
  const byDate = new Map();
  for (const row of rows) {
    const dateObj = parseDate(row.document_date);
    if (!dateObj) continue;
    const key = dateKey(dateObj);
    if (!byDate.has(key)) byDate.set(key, new Map());
    const dayMap = byDate.get(key);
    const values = cfg.split
      ? splitParts(row[cfg.key], cfg.key === "category" ? "uncategorized" : "Unknown")
      : [(row[cfg.key] || "Unknown").trim() || "Unknown"];
    for (const value of values) {
      totals.set(value, (totals.get(value) || 0) + 1);
      dayMap.set(value, (dayMap.get(value) || 0) + 1);
    }
  }
  const topValues = Array.from(totals.entries())
    .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
    .slice(0, cfg.limit)
    .map(([value]) => value);
  const dates = Array.from(byDate.keys()).sort();
  const series = topValues.map(value => ({
    value,
    points: dates.map(d => ({ date: d, count: byDate.get(d).get(value) || 0 })),
  }));
  return { dates, series };
}

function renderTrendChart(rows) {
  const chartEl = document.getElementById("trend-chart");
  const legendEl = document.getElementById("trend-legend");
  const selectEl = document.getElementById("trend-dimension");
  if (!chartEl || !legendEl || !selectEl) return;

  const dimensionKey = selectEl.value;
  const { dates, series } = buildTrendSeries(rows, dimensionKey);
  chartEl.innerHTML = "";
  legendEl.innerHTML = "";

  if (!dates.length || !series.length) {
    chartEl.textContent = "No trend data for the current filters.";
    return;
  }

  const width = 760;
  const height = 220;
  const padding = { top: 16, right: 24, bottom: 32, left: 36 };
  const maxCount = Math.max(1, ...series.flatMap(s => s.points.map(p => p.count)));

  const xForIndex = (idx) => {
    if (dates.length === 1) return padding.left + (width - padding.left - padding.right) / 2;
    const span = width - padding.left - padding.right;
    return padding.left + (span * idx) / (dates.length - 1);
  };
  const yForValue = (value) => {
    const span = height - padding.top - padding.bottom;
    return padding.top + span - (span * value) / maxCount;
  };

  const xLabels = [dates[0], dates[Math.floor(dates.length / 2)], dates[dates.length - 1]]
    .filter((v, i, arr) => arr.indexOf(v) === i);

  const lines = [];
  for (let i = 0; i < xLabels.length; i++) {
    const idx = dates.indexOf(xLabels[i]);
    if (idx === -1) continue;
    const x = xForIndex(idx);
    lines.push(`<line x1="${x}" y1="${padding.top}" x2="${x}" y2="${height - padding.bottom}" stroke="#eef2f3"/>`);
  }

  const grid = `<line x1="${padding.left}" y1="${padding.top}" x2="${padding.left}" y2="${height - padding.bottom}" stroke="#dfe6ea"/>
<line x1="${padding.left}" y1="${height - padding.bottom}" x2="${width - padding.right}" y2="${height - padding.bottom}" stroke="#dfe6ea"/>`;

  const pathLines = series.map((s, idx) => {
    const points = s.points.map((p, i) => `${xForIndex(i)},${yForValue(p.count)}`).join(" ");
    const color = TREND_COLORS[idx % TREND_COLORS.length];
    return `<polyline fill="none" stroke="${color}" stroke-width="2" points="${points}"/>`;
  }).join("");

  const yTicks = 4;
  const yLabels = [];
  for (let i = 0; i <= yTicks; i++) {
    const value = Math.round((maxCount * i) / yTicks);
    const y = yForValue(value);
    yLabels.push(`<text x="${padding.left - 6}" y="${y + 4}" text-anchor="end" font-size="10" fill="#52616b">${value}</text>`);
  }

  const xLabelNodes = xLabels.map((label) => {
    const idx = dates.indexOf(label);
    if (idx === -1) return "";
    const x = xForIndex(idx);
    return `<text x="${x}" y="${height - 10}" text-anchor="middle" font-size="10" fill="#52616b">${label}</text>`;
  }).join("");

  const svg = `
<svg viewBox="0 0 ${width} ${height}" class="chart">
  ${grid}
  ${lines.join("")}
  ${pathLines}
  ${yLabels.join("")}
  ${xLabelNodes}
  <text x="${padding.left}" y="${padding.top - 6}" text-anchor="start" font-size="10" fill="#52616b">Count</text>
  <text x="${(width - padding.right + padding.left) / 2}" y="${height - 2}" text-anchor="middle" font-size="10" fill="#52616b">Date</text>
</svg>`;
  chartEl.innerHTML = svg;

  const seriesLegend = document.createElement("div");
  seriesLegend.style.display = "flex";
  seriesLegend.style.flexWrap = "wrap";
  seriesLegend.style.gap = "10px";
  for (let i = 0; i < series.length; i++) {
    const item = document.createElement("div");
    const swatch = document.createElement("span");
    swatch.className = "legend-swatch";
    swatch.style.background = TREND_COLORS[i % TREND_COLORS.length];
    const label = document.createElement("span");
    label.textContent = series[i].value;
    item.appendChild(swatch);
    item.appendChild(label);
    seriesLegend.appendChild(item);
  }
  legendEl.appendChild(seriesLegend);
}

function summarize() {
  const filtered = DATA.filter(rowMatches);
  const countsByKey = buildCounts(filtered);
  const violationsEl = document.getElementById("kpi-violations");
  if (violationsEl) violationsEl.textContent = filtered.length;

  const caseSet = new Set(filtered.map(caseId));
  const casesEl = document.getElementById("kpi-cases");
  if (casesEl) casesEl.textContent = caseSet.size;

  const companySet = new Set(filtered.map(r => r.company).filter(Boolean));
  const companiesEl = document.getElementById("kpi-companies");
  if (companiesEl) companiesEl.textContent = companySet.size;

  const dates = filtered.map(r => parseDate(r.document_date)).filter(Boolean).sort((a,b) => a-b);
  const dateLabel = dates.length
    ? `${dates[0].toISOString().slice(0,10)} to ${dates[dates.length-1].toISOString().slice(0,10)}`
    : "Unknown";
  const docEl = document.getElementById("kpi-docdates");
  if (docEl) docEl.textContent = dateLabel;

  const dateRangeEl = document.getElementById("date-range");
  if (dateRangeEl && DATE_MIN && DATE_MAX) {
    dateRangeEl.innerHTML = "";
    const minDay = dateToDayIndex(DATE_MIN);
    const maxDay = dateToDayIndex(DATE_MAX);
    const fromValue = params.get("date_from") || formatDateInput(DATE_MIN);
    const toValue = params.get("date_to") || formatDateInput(DATE_MAX);
    const fromDay = dateToDayIndex(new Date(fromValue + "T00:00:00"));
    const toDay = dateToDayIndex(new Date(toValue + "T00:00:00"));

    const fromRow = document.createElement("div");
    fromRow.className = "date-range-row";
    const fromLabel = document.createElement("span");
    fromLabel.textContent = "From";
    const fromRange = document.createElement("input");
    fromRange.type = "range";
    fromRange.min = String(minDay);
    fromRange.max = String(maxDay);
    fromRange.value = String(fromDay);
    const fromInput = document.createElement("input");
    fromInput.type = "date";
    fromInput.value = fromValue;
    fromRow.appendChild(fromLabel);
    fromRow.appendChild(fromRange);
    fromRow.appendChild(fromInput);

    const toRow = document.createElement("div");
    toRow.className = "date-range-row";
    const toLabel = document.createElement("span");
    toLabel.textContent = "To";
    const toRange = document.createElement("input");
    toRange.type = "range";
    toRange.min = String(minDay);
    toRange.max = String(maxDay);
    toRange.value = String(toDay);
    const toInput = document.createElement("input");
    toInput.type = "date";
    toInput.value = toValue;
    toRow.appendChild(toLabel);
    toRow.appendChild(toRange);
    toRow.appendChild(toInput);

     const syncAndNavigate = (nextFrom, nextTo) => {
      const next = new URLSearchParams(params);
      next.set("date_from", nextFrom);
      next.set("date_to", nextTo);
      setSearchParams(next);
     };

    const clampAndSync = () => {
      let currentFrom = dateToDayIndex(new Date(fromInput.value + "T00:00:00"));
      let currentTo = dateToDayIndex(new Date(toInput.value + "T00:00:00"));
      if (currentFrom > currentTo) {
        currentFrom = currentTo;
        fromInput.value = toInput.value;
        fromRange.value = String(currentFrom);
      }
      syncAndNavigate(fromInput.value, toInput.value);
    };

    fromRange.addEventListener("change", () => {
      const day = parseInt(fromRange.value, 10);
      fromInput.value = formatDateInput(dayIndexToDate(day));
      clampAndSync();
    });
    toRange.addEventListener("change", () => {
      const day = parseInt(toRange.value, 10);
      toInput.value = formatDateInput(dayIndexToDate(day));
      clampAndSync();
    });
    fromInput.addEventListener("change", () => {
      const day = dateToDayIndex(new Date(fromInput.value + "T00:00:00"));
      fromRange.value = String(day);
      clampAndSync();
    });
    toInput.addEventListener("change", () => {
      const day = dateToDayIndex(new Date(toInput.value + "T00:00:00"));
      toRange.value = String(day);
      clampAndSync();
    });

    dateRangeEl.appendChild(fromRow);
    dateRangeEl.appendChild(toRow);
  }

  const enforcementMap = new Map();
  for (const row of filtered) {
    const key = row.enforcement_type || "Unknown";
    if (!enforcementMap.has(key)) enforcementMap.set(key, new Set());
    enforcementMap.get(key).add(caseId(row));
  }
  const enforcementItems = Array.from(enforcementMap.entries())
    .map(([k, v]) => [k, v.size])
    .sort((a,b) => b[1] - a[1] || a[0].localeCompare(b[0]));
  fillTable("enforcement-table", enforcementItems, "enforcement_type");

  const categoryCounts = new Map();
  for (const row of filtered) {
    for (const part of splitParts(row.category, "uncategorized")) {
      categoryCounts.set(part, (categoryCounts.get(part) || 0) + 1);
    }
  }
  const categoryItems = Array.from(categoryCounts.entries())
    .sort((a,b) => b[1] - a[1] || a[0].localeCompare(b[0]));
  fillTable("category-table", categoryItems, "category");

  const sourceCounts = new Map();
  for (const row of filtered) {
    for (const part of splitParts(row.source_type, "Unknown")) {
      sourceCounts.set(part, (sourceCounts.get(part) || 0) + 1);
    }
  }
  const sourceItems = Array.from(sourceCounts.entries())
    .sort((a,b) => b[1] - a[1] || a[0].localeCompare(b[0]));
  fillTable("source-table", sourceItems.slice(0, 10), "source_type");

  const equipmentCounts = new Map();
  for (const row of filtered) {
    for (const part of splitParts(row.equipment_type, "Unknown")) {
      equipmentCounts.set(part, (equipmentCounts.get(part) || 0) + 1);
    }
  }
  const equipmentItems = Array.from(equipmentCounts.entries())
    .sort((a,b) => b[1] - a[1] || a[0].localeCompare(b[0]));
  fillTable("equipment-table", equipmentItems, "equipment_type");

  const ruleCounts = new Map();
  for (const row of filtered) {
    const parts = (row.rule_citation || "").split(";").map(p => p.trim()).filter(Boolean);
    for (const part of parts) {
      ruleCounts.set(part, (ruleCounts.get(part) || 0) + 1);
    }
  }
  const ruleItems = Array.from(ruleCounts.entries())
    .sort((a,b) => b[1] - a[1] || a[0].localeCompare(b[0]))
    .slice(0, 25);
  fillTable("rule-table", ruleItems, "rule_citation");

  const companyCounts = new Map();
  for (const row of filtered) {
    const key = row.company || "Unknown";
    companyCounts.set(key, (companyCounts.get(key) || 0) + 1);
  }
  const companyItems = Array.from(companyCounts.entries())
    .sort((a,b) => b[1] - a[1] || a[0].localeCompare(b[0]))
    .slice(0, 20);
  fillTable("company-table", companyItems, "company");

  const penaltyTbody = document.getElementById("penalty-table");
  if (penaltyTbody) {
    const byCase = new Map();
    for (const row of filtered) {
      const amount = parseMoney(row.monetary_penalty);
      if (amount === null) continue;
      const key = caseId(row);
      const existing = byCase.get(key);
      if (!existing || amount > existing.amount) {
        byCase.set(key, {
          amount,
          penalty: row.monetary_penalty,
          document_date: row.document_date || "",
          company: row.company || "",
          case_number: row.case_number || "",
          pdf_url: row.pdf_url || "",
        });
      }
    }
    const items = Array.from(byCase.values())
      .sort((a, b) => b.amount - a.amount || String(a.company).localeCompare(String(b.company)));

    penaltyTbody.innerHTML = "";
    if (!items.length) {
      const tr = document.createElement("tr");
      const td = document.createElement("td");
      td.colSpan = 4;
      td.className = "filter-count";
      td.textContent = "No monetary penalties in the current filters.";
      tr.appendChild(td);
      penaltyTbody.appendChild(tr);
    } else {
      for (const item of items) {
        const tr = document.createElement("tr");
        const dateCell = document.createElement("td");
        dateCell.textContent = item.document_date;
        tr.appendChild(dateCell);

        const companyCell = document.createElement("td");
        companyCell.textContent = item.company;
        tr.appendChild(companyCell);

        const caseCell = document.createElement("td");
        if (item.pdf_url) {
          const link = document.createElement("a");
          link.href = item.pdf_url;
          link.textContent = item.case_number;
          link.target = "_blank";
          link.rel = "noopener";
          caseCell.appendChild(link);
        } else {
          caseCell.textContent = item.case_number;
        }
        tr.appendChild(caseCell);

        const penCell = document.createElement("td");
        penCell.textContent = item.penalty;
        tr.appendChild(penCell);

        penaltyTbody.appendChild(tr);
      }
    }
  }

  renderTrendChart(filtered);

        const detailTbody = document.getElementById("detail-table");
        if (detailTbody) {
            detailTbody.innerHTML = "";
            const detailRows = filtered.slice().sort((a, b) => {
                const da = parseDate(a.document_date);
                const db = parseDate(b.document_date);
                if (!da && !db) return 0;
                if (!da) return 1;
                if (!db) return -1;
                return db - da;
            });
            const limit = 200;
            for (const row of detailRows.slice(0, limit)) {
                const tr = document.createElement("tr");
                const dateCell = document.createElement("td");
                dateCell.textContent = row.document_date || "";
                tr.appendChild(dateCell);

                const companyCell = document.createElement("td");
                companyCell.textContent = row.company || "";
                tr.appendChild(companyCell);

                const caseCell = document.createElement("td");
                if (row.pdf_url) {
                    const link = document.createElement("a");
                    link.href = row.pdf_url;
                    link.textContent = row.case_number || "";
                    link.target = "_blank";
                    link.rel = "noopener";
                    caseCell.appendChild(link);
                } else {
                    caseCell.textContent = row.case_number || "";
                }
                tr.appendChild(caseCell);

                const ruleCell = document.createElement("td");
                ruleCell.textContent = row.rule_citation || "";
                tr.appendChild(ruleCell);

                const violationCell = document.createElement("td");
                violationCell.textContent = row.violation_description || "";
                tr.appendChild(violationCell);
                detailTbody.appendChild(tr);
            }
        }

        const filters = document.getElementById("filters");
        if (!filters) return;
        filters.innerHTML = "";
        const active = getActiveFilters(params);
        const hasActive = Object.values(active).some(values => values.length > 0);

        const header = document.createElement("div");
        header.className = "filters-header";
        const status = document.createElement("div");
        status.className = "chip";
        status.textContent = hasActive ? "Active filters" : "No filters applied";
        header.appendChild(status);

        if (hasActive) {
            const clearAll = document.createElement("a");
            clearAll.className = "filter-clear";
            clearAll.href = "?";
            clearAll.textContent = "Clear all";
            header.appendChild(clearAll);

            for (const cfg of FILTER_CONFIG) {
                for (const value of active[cfg.key]) {
                    const chip = document.createElement("div");
                    chip.className = "chip";
                    const link = document.createElement("a");
                    link.href = buildLink(cfg.key, value);
                    link.textContent = `${cfg.label}: ${value}`;
                    chip.appendChild(link);
                    header.appendChild(chip);
                }
            }
        }
        filters.appendChild(header);

        for (const cfg of FILTER_CONFIG) {
            const group = document.createElement("div");
            group.className = "filter-group";
            const title = document.createElement("div");
            title.className = "filter-title";
            title.textContent = cfg.label;
            group.appendChild(title);

            const list = document.createElement("div");
            list.className = "filter-options";
            const options = OPTIONS_BY_KEY[cfg.key] || [];
            const selected = active[cfg.key].map(v => normalize(v));

            for (const [label, _] of options) {
                const countMap = countsByKey[cfg.key] || new Map();
                const count = countMap.get(label) || 0;
                const option = document.createElement("label");
                option.className = "filter-option";

                const input = document.createElement("input");
                input.type = "checkbox";
                input.checked = selected.includes(normalize(label));
                 input.addEventListener("change", () => {
                    const next = new URLSearchParams(params);
                    const current = getParamValuesFrom(next, cfg.key);
                    const normalized = normalize(label);
                    const remaining = current.filter(v => normalize(v) !== normalized);
                    if (input.checked) remaining.push(label);
                    setParamValues(next, cfg.key, remaining);
                    setSearchParams(next);
                 });

                const name = document.createElement("span");
                name.textContent = label;

                const countEl = document.createElement("span");
                countEl.className = "filter-count";
                countEl.textContent = `(${count})`;

                option.appendChild(input);
                option.appendChild(name);
                option.appendChild(countEl);
                list.appendChild(option);
            }

            group.appendChild(list);
            filters.appendChild(group);
        }

        if (!trendWired) {
            const selectEl = document.getElementById("trend-dimension");
            if (selectEl) {
                selectEl.addEventListener("change", () => renderTrendChart(filtered));
            }
            trendWired = true;
        }
}

summarize();
</script>"""

    html_out = html_out.replace("<!--DETAIL_SECTION-->", detail_section)
    html_out = html_out.replace("<!--DETAIL_SCRIPT-->", detail_script)
    html_out = html_out.replace("__DATA__", json.dumps(detail_rows, ensure_ascii=True))

    OUTPUT_HTML.write_text(html_out, encoding="utf-8")
    print(f"Wrote report {OUTPUT_HTML}")


if __name__ == "__main__":
    main()
