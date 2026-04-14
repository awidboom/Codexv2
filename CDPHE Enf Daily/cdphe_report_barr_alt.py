import csv
import html
import math
import re
from base64 import b64encode
from collections import defaultdict
from datetime import datetime
from pathlib import Path


REPO_DIR = Path(__file__).resolve().parent
DOWNLOAD_DIR = REPO_DIR / "downloads"
OUTPUT_DIR = REPO_DIR / "outputs"
ASSET_DIR = REPO_DIR / "assets"
INPUT_CSV = DOWNLOAD_DIR / "cdphe_enforcement_summary.csv"
OUTPUT_HTML = OUTPUT_DIR / "cdphe_enforcement_summary_report_barr_alt.html"
LOGO_PATH = ASSET_DIR / "barr_logo_primary_blue.svg"


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


def parse_money(value: str):
    cleaned = re.sub(r"[^0-9.\-]", "", (value or "").strip())
    if not cleaned:
        return None
    try:
        return float(cleaned)
    except ValueError:
        return None


def format_money(value: float) -> str:
    return f"${value:,.0f}"


def iso_date(value) -> str:
    return value.isoformat() if value else "Unknown"


def date_span(dates) -> str:
    cleaned = sorted(d for d in dates if d)
    if not cleaned:
        return "Unknown"
    if len(cleaned) == 1:
        return cleaned[0].isoformat()
    return f"{cleaned[0].isoformat()} to {cleaned[-1].isoformat()}"


def tally_split(values, fallback: str) -> dict[str, int]:
    counts: dict[str, int] = defaultdict(int)
    for value in values:
        parts = [part.strip() for part in (value or "").split(";") if part.strip()]
        if not parts:
            parts = [fallback]
        for part in parts:
            counts[part] += 1
    return counts


def top_n(counts: dict[str, int], limit: int) -> list[tuple[str, int]]:
    return sorted(counts.items(), key=lambda item: (-item[1], item[0].lower()))[:limit]


def label_for_case(row: dict[str, str]) -> str:
    return (row.get("case_number") or "").strip() or (row.get("file_name") or "").strip() or "Unknown"


def embed_logo() -> str:
    if not LOGO_PATH.exists():
        return ""
    encoded = b64encode(LOGO_PATH.read_bytes()).decode("ascii")
    return f'<img src="data:image/svg+xml;base64,{encoded}" alt="Barr logo" />'


def build_bar_rows(items: list[tuple[str, int]], max_value: int, color_var: str) -> str:
    if not items:
        return "<div class='empty-state'>No data available.</div>"

    rows = []
    safe_max = max(max_value, 1)
    for label, value in items:
        width = max(6.0, (value / safe_max) * 100.0) if value else 0.0
        rows.append(
            "<div class='metric-row'>"
            f"<div class='metric-label'>{html.escape(label)}</div>"
            "<div class='metric-track'>"
            f"<span class='metric-fill {color_var}' style='width:{width:.1f}%'></span>"
            "</div>"
            f"<div class='metric-value'>{value}</div>"
            "</div>"
        )
    return "".join(rows)


def build_table(headers: list[str], rows: list[list[str]]) -> str:
    if not rows:
        return "<div class='empty-state'>No rows available.</div>"
    head_html = "".join(f"<th>{html.escape(header)}</th>" for header in headers)
    body = []
    for row in rows:
        body.append("<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>")
    return (
        "<table class='data-table'>"
        f"<thead><tr>{head_html}</tr></thead>"
        f"<tbody>{''.join(body)}</tbody>"
        "</table>"
    )


def build_penalty_rows(rows: list[dict[str, str]]) -> list[tuple[str, str, str, float, str]]:
    by_case: dict[str, tuple[str, str, str, float, str]] = {}
    for row in rows:
        amount = parse_money(row.get("monetary_penalty", ""))
        if amount is None:
            continue
        case_key = label_for_case(row)
        existing = by_case.get(case_key)
        candidate = (
            row.get("document_date", ""),
            row.get("company", "") or "-",
            case_key,
            amount,
            row.get("pdf_url", ""),
        )
        if existing is None or amount > existing[3]:
            by_case[case_key] = candidate

    return sorted(
        by_case.values(),
        key=lambda item: (
            parse_date(item[0]) or datetime.max.date(),
            item[1].lower(),
            item[2].lower(),
        ),
    )


def build_recent_case_rows(rows: list[dict[str, str]], limit: int) -> list[list[str]]:
    sorted_rows = sorted(
        rows,
        key=lambda row: parse_date(row.get("document_date", "")) or datetime.min.date(),
        reverse=True,
    )
    recent = []
    seen: set[tuple[str, str]] = set()
    for row in sorted_rows:
        case_key = label_for_case(row)
        unique_key = (case_key, row.get("violation_id", "") or row.get("violation_description", ""))
        if unique_key in seen:
            continue
        seen.add(unique_key)
        case_label = html.escape(case_key)
        pdf_url = (row.get("pdf_url") or "").strip()
        if pdf_url:
            case_label = (
                f"<a href='{html.escape(pdf_url, quote=True)}' target='_blank' rel='noopener'>"
                f"{case_label}</a>"
            )
        recent.append(
            [
                html.escape(row.get("document_date", "") or "-"),
                html.escape(row.get("company", "") or "-"),
                case_label,
                html.escape(row.get("enforcement_type", "") or "-"),
                html.escape(row.get("category", "") or "-"),
                html.escape((row.get("violation_description", "") or "-")[:220]),
            ]
        )
        if len(recent) >= limit:
            break
    return recent


def build_radial_gauge(value: int, maximum: int, label: str) -> str:
    safe_max = max(maximum, 1)
    ratio = max(0.0, min(1.0, value / safe_max))
    circumference = 2 * math.pi * 52
    dash = circumference * ratio
    gap = circumference - dash
    return (
        "<div class='gauge'>"
        "<svg viewBox='0 0 140 140' aria-hidden='true'>"
        "<circle class='gauge-track' cx='70' cy='70' r='52'></circle>"
        f"<circle class='gauge-value' cx='70' cy='70' r='52' style='stroke-dasharray:{dash:.1f} {gap:.1f}'></circle>"
        "</svg>"
        f"<div class='gauge-number'>{value}</div>"
        f"<div class='gauge-label'>{html.escape(label)}</div>"
        "</div>"
    )


def main() -> None:
    if not INPUT_CSV.exists():
        raise SystemExit(f"Missing input CSV: {INPUT_CSV}")

    with INPUT_CSV.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))

    if not rows:
        raise SystemExit("No records found in summary CSV.")

    doc_dates = [parse_date(row.get("document_date", "")) for row in rows]
    case_ids = {label_for_case(row) for row in rows if label_for_case(row)}
    companies = {(row.get("company") or "").strip() for row in rows if (row.get("company") or "").strip()}
    penalties = build_penalty_rows(rows)
    total_penalty = sum(item[3] for item in penalties)

    enforcement_case_map: dict[str, set[str]] = defaultdict(set)
    company_counts: dict[str, int] = defaultdict(int)
    for row in rows:
        enforcement_type = (row.get("enforcement_type") or "").strip() or "Unknown"
        enforcement_case_map[enforcement_type].add(label_for_case(row))
        company = (row.get("company") or "").strip()
        if company:
            company_counts[company] += 1

    enforcement_counts = {key: len(value) for key, value in enforcement_case_map.items()}
    category_counts = tally_split((row.get("category", "") for row in rows), "uncategorized")
    source_counts = tally_split((row.get("source_type", "") for row in rows), "Unknown")
    equipment_counts = tally_split((row.get("equipment_type", "") for row in rows), "Unknown")

    top_enforcement = top_n(enforcement_counts, 6)
    top_categories = top_n(category_counts, 8)
    top_companies = top_n(company_counts, 8)
    top_sources = top_n(source_counts, 6)
    top_equipment = top_n(equipment_counts, 6)

    top_penalty_rows = []
    for document_date, company, case_key, amount, pdf_url in sorted(penalties, key=lambda item: (-item[3], item[1].lower()))[:8]:
        case_html = html.escape(case_key)
        if pdf_url:
            case_html = (
                f"<a href='{html.escape(pdf_url, quote=True)}' target='_blank' rel='noopener'>"
                f"{case_html}</a>"
            )
        top_penalty_rows.append(
            [
                html.escape(document_date or "-"),
                html.escape(company),
                case_html,
                format_money(amount),
            ]
        )

    recent_case_rows = build_recent_case_rows(rows, limit=12)
    newest_date = max((date for date in doc_dates if date), default=None)
    oldest_date = min((date for date in doc_dates if date), default=None)

    top_category_count = max((count for _, count in top_categories), default=1)
    top_enforcement_count = max((count for _, count in top_enforcement), default=1)
    top_company_count = max((count for _, count in top_companies), default=1)
    top_source_count = max((count for _, count in top_sources), default=1)
    top_equipment_count = max((count for _, count in top_equipment), default=1)

    narrative = (
        f"{len(rows):,} alleged violations across {len(case_ids):,} cases involving "
        f"{len(companies):,} companies. Reporting window: {date_span(doc_dates)}."
    )

    html_out = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>CDPHE Enforcement Summary | Barr Alternate</title>
<style>
:root {{
  --dark-blue: #0486cc;
  --dark-blue-text: #047abe;
  --navy: #182836;
  --light-blue: #d7edf9;
  --white: #ffffff;
  --light-neutral: #eff1f3;
  --medium-neutral: #c3d2db;
  --neutral: #80959e;
  --dark-neutral: #596b7b;
  --orange: #fe734a;
  --green: #196759;
  --green-light: #a4cf45;
  --yellow: #ffa740;
  --red: #af3d18;
  --burgundy: #67014a;
  --shadow: 0 16px 40px rgba(24, 40, 54, 0.12);
  --rule: linear-gradient(90deg, var(--dark-blue), rgba(4, 134, 204, 0.18));
}}
* {{ box-sizing: border-box; }}
html {{ scroll-behavior: smooth; }}
body {{
  margin: 0;
  color: var(--navy);
  background:
    linear-gradient(180deg, #f8fbfd 0%, #eef4f7 42%, #ffffff 100%);
  font-family: Inter, "Avenir Next", "Segoe UI", Arial, sans-serif;
}}
a {{
  color: var(--dark-blue-text);
  text-decoration-thickness: 1px;
  text-underline-offset: 2px;
}}
.page {{
  min-height: 100vh;
}}
.hero {{
  position: relative;
  overflow: hidden;
  background:
    linear-gradient(135deg, rgba(24, 40, 54, 0.98), rgba(24, 40, 54, 0.9)),
    linear-gradient(90deg, rgba(4, 134, 204, 0.2), rgba(4, 134, 204, 0.02));
  color: var(--white);
}}
.hero::before {{
  content: "";
  position: absolute;
  inset: 0;
  background:
    repeating-linear-gradient(
      135deg,
      rgba(215, 237, 249, 0.12) 0 2px,
      rgba(215, 237, 249, 0) 2px 22px
    );
  opacity: 0.65;
}}
.hero::after {{
  content: "";
  position: absolute;
  right: -12vw;
  top: -6rem;
  width: min(34rem, 48vw);
  height: min(34rem, 48vw);
  background: radial-gradient(circle, rgba(4, 134, 204, 0.28), rgba(4, 134, 204, 0));
  border-radius: 50%;
}}
.bars {{
  position: absolute;
  left: 0;
  top: 0;
  width: min(22rem, 42vw);
  display: grid;
  gap: 0.55rem;
  padding: 1rem 0 0 1.5rem;
}}
.bars span {{
  display: block;
  height: 0.32rem;
  background: var(--light-blue);
  transform-origin: left center;
  animation: slide-in 780ms ease-out both;
}}
.bars span:nth-child(1) {{ width: 100%; animation-delay: 40ms; }}
.bars span:nth-child(2) {{ width: 78%; animation-delay: 120ms; }}
.bars span:nth-child(3) {{ width: 52%; animation-delay: 200ms; }}
.hero-inner {{
  position: relative;
  z-index: 1;
  max-width: 1280px;
  margin: 0 auto;
  padding: 2.5rem 1.5rem 3rem;
}}
.hero-top {{
  display: flex;
  justify-content: space-between;
  gap: 1.5rem;
  align-items: flex-start;
  margin-bottom: 3rem;
}}
.logo-lockup img {{
  display: block;
  width: 8.5rem;
  height: auto;
  background: var(--white);
  padding: 0.55rem 0.8rem;
  border-radius: 0.35rem;
}}
.eyebrow {{
  display: inline-block;
  margin-bottom: 0.8rem;
  color: var(--light-blue);
  font-size: 0.8rem;
  font-weight: 700;
  letter-spacing: 0.16em;
  text-transform: uppercase;
}}
.hero-grid {{
  display: grid;
  grid-template-columns: minmax(0, 1.25fr) minmax(18rem, 0.8fr);
  gap: 2rem;
  align-items: end;
}}
.hero-copy {{
  max-width: 44rem;
  animation: rise 680ms ease-out both;
}}
.hero-copy h1 {{
  margin: 0;
  font-family: "Korolev", "Franklin Gothic Demi Condensed", Arial, sans-serif;
  font-size: clamp(2.5rem, 5vw, 4.4rem);
  line-height: 0.95;
  letter-spacing: 0.01em;
}}
.hero-copy p {{
  margin: 1rem 0 0;
  max-width: 40rem;
  color: rgba(255, 255, 255, 0.82);
  font-size: 1rem;
  line-height: 1.65;
}}
.hero-meta {{
  display: grid;
  gap: 0.9rem;
  align-self: stretch;
  animation: rise 780ms ease-out both;
}}
.meta-block {{
  padding: 1rem 1.1rem;
  border: 1px solid rgba(255, 255, 255, 0.16);
  background: rgba(255, 255, 255, 0.06);
  backdrop-filter: blur(6px);
}}
.meta-label {{
  color: rgba(215, 237, 249, 0.88);
  text-transform: uppercase;
  letter-spacing: 0.12em;
  font-size: 0.72rem;
  font-weight: 700;
}}
.meta-value {{
  margin-top: 0.45rem;
  font-size: 1.05rem;
  line-height: 1.4;
}}
.main {{
  max-width: 1280px;
  margin: 0 auto;
  padding: 2rem 1.5rem 3rem;
}}
.section {{
  margin-bottom: 2.25rem;
}}
.section-heading {{
  display: grid;
  gap: 0.65rem;
  margin-bottom: 1rem;
}}
.section-heading h2 {{
  margin: 0;
  font-family: "Korolev", "Franklin Gothic Demi Condensed", Arial, sans-serif;
  font-size: clamp(1.6rem, 2.8vw, 2.2rem);
  line-height: 1;
  color: var(--navy);
}}
.section-heading p {{
  margin: 0;
  color: var(--dark-neutral);
  max-width: 52rem;
  line-height: 1.6;
}}
.section-rule {{
  width: min(16rem, 100%);
  height: 0.28rem;
  background: var(--rule);
}}
.kpi-band {{
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 1px;
  background: var(--medium-neutral);
  box-shadow: var(--shadow);
}}
.kpi {{
  background: var(--white);
  padding: 1.2rem 1.2rem 1.35rem;
}}
.kpi-label {{
  color: var(--dark-neutral);
  text-transform: uppercase;
  letter-spacing: 0.12em;
  font-size: 0.72rem;
  font-weight: 700;
}}
.kpi-value {{
  margin-top: 0.5rem;
  font-size: clamp(1.9rem, 3.3vw, 2.75rem);
  line-height: 1;
}}
.kpi-note {{
  margin-top: 0.5rem;
  color: var(--dark-neutral);
  font-size: 0.92rem;
}}
.story-grid {{
  display: grid;
  grid-template-columns: minmax(0, 1.2fr) minmax(18rem, 0.8fr);
  gap: 1.25rem;
}}
.story-panel {{
  background: var(--white);
  box-shadow: var(--shadow);
  padding: 1.4rem;
}}
.story-panel.alt {{
  background: linear-gradient(180deg, var(--light-blue), #f8fbfd);
}}
.story-panel h3 {{
  margin: 0;
  font-size: 1rem;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  color: var(--dark-neutral);
}}
.story-panel p {{
  margin: 0.75rem 0 0;
  line-height: 1.7;
  color: var(--navy);
}}
.gauge-row {{
  display: flex;
  gap: 1rem;
  align-items: center;
  justify-content: center;
  min-height: 100%;
}}
.gauge {{
  position: relative;
  width: 10rem;
  height: 10rem;
  display: grid;
  place-items: center;
}}
.gauge svg {{
  width: 100%;
  height: 100%;
  transform: rotate(-90deg);
}}
.gauge-track {{
  fill: none;
  stroke: rgba(4, 134, 204, 0.12);
  stroke-width: 12;
}}
.gauge-value {{
  fill: none;
  stroke: var(--dark-blue);
  stroke-width: 12;
  stroke-linecap: round;
  animation: draw-ring 1100ms ease-out both;
}}
.gauge-number {{
  position: absolute;
  font-size: 2rem;
  font-weight: 700;
  color: var(--navy);
}}
.gauge-label {{
  position: absolute;
  bottom: 1.1rem;
  width: 100%;
  text-align: center;
  color: var(--dark-neutral);
  font-size: 0.74rem;
  text-transform: uppercase;
  letter-spacing: 0.12em;
}}
.analytics-grid {{
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 1.25rem;
}}
.analytics-panel {{
  background: var(--white);
  box-shadow: var(--shadow);
  padding: 1.3rem 1.3rem 1.2rem;
}}
.analytics-panel h3 {{
  margin: 0 0 1rem;
  font-size: 0.95rem;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  color: var(--dark-neutral);
}}
.metric-list {{
  display: grid;
  gap: 0.8rem;
}}
.metric-row {{
  display: grid;
  grid-template-columns: minmax(7rem, 15rem) minmax(0, 1fr) auto;
  gap: 0.85rem;
  align-items: center;
}}
.metric-label {{
  font-size: 0.92rem;
  line-height: 1.35;
}}
.metric-track {{
  height: 0.72rem;
  background: var(--light-neutral);
  overflow: hidden;
}}
.metric-fill {{
  display: block;
  height: 100%;
  transform-origin: left center;
  animation: grow 900ms ease-out both;
}}
.metric-fill.blue {{ background: linear-gradient(90deg, var(--dark-blue), #60b7e6); }}
.metric-fill.green {{ background: linear-gradient(90deg, var(--green), var(--green-light)); }}
.metric-fill.orange {{ background: linear-gradient(90deg, var(--yellow), var(--orange)); }}
.metric-fill.red {{ background: linear-gradient(90deg, var(--red), var(--orange)); }}
.metric-fill.burgundy {{ background: linear-gradient(90deg, var(--burgundy), #9c4d77); }}
.metric-value {{
  font-weight: 700;
  color: var(--navy);
  white-space: nowrap;
}}
.table-panel {{
  background: var(--white);
  box-shadow: var(--shadow);
  overflow: hidden;
}}
.table-head {{
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  align-items: end;
  padding: 1.25rem 1.3rem 0.8rem;
}}
.table-head h3 {{
  margin: 0;
  font-size: 0.95rem;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  color: var(--dark-neutral);
}}
.table-head p {{
  margin: 0.35rem 0 0;
  color: var(--dark-neutral);
  font-size: 0.92rem;
}}
.table-wrap {{
  overflow-x: auto;
}}
.data-table {{
  width: 100%;
  border-collapse: collapse;
}}
.data-table th,
.data-table td {{
  padding: 0.8rem 1.3rem;
  text-align: left;
  vertical-align: top;
  border-top: 1px solid #e7edf1;
  font-size: 0.93rem;
  line-height: 1.45;
}}
.data-table th {{
  color: var(--dark-neutral);
  text-transform: uppercase;
  letter-spacing: 0.1em;
  font-size: 0.72rem;
  background: #fbfdfe;
}}
.data-table tbody tr:hover {{
  background: #f6fbfe;
}}
.footnote {{
  margin-top: 0.85rem;
  color: var(--dark-neutral);
  font-size: 0.84rem;
  line-height: 1.55;
}}
.footer {{
  padding: 0 1.5rem 2.5rem;
}}
.footer-inner {{
  max-width: 1280px;
  margin: 0 auto;
  padding-top: 1rem;
  border-top: 1px solid var(--medium-neutral);
  color: var(--dark-neutral);
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  flex-wrap: wrap;
  font-size: 0.84rem;
}}
.empty-state {{
  color: var(--dark-neutral);
  font-size: 0.92rem;
}}
@keyframes grow {{
  from {{ transform: scaleX(0); }}
  to {{ transform: scaleX(1); }}
}}
@keyframes slide-in {{
  from {{ transform: scaleX(0); opacity: 0; }}
  to {{ transform: scaleX(1); opacity: 1; }}
}}
@keyframes rise {{
  from {{ opacity: 0; transform: translateY(18px); }}
  to {{ opacity: 1; transform: translateY(0); }}
}}
@keyframes draw-ring {{
  from {{ stroke-dasharray: 0 999; }}
}}
@media (max-width: 1024px) {{
  .hero-grid,
  .story-grid,
  .analytics-grid {{
    grid-template-columns: 1fr;
  }}
  .kpi-band {{
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }}
}}
@media (max-width: 720px) {{
  .hero-inner,
  .main,
  .footer {{
    padding-left: 1rem;
    padding-right: 1rem;
  }}
  .hero-top {{
    margin-bottom: 2rem;
  }}
  .hero-copy h1 {{
    font-size: 2.4rem;
  }}
  .kpi-band {{
    grid-template-columns: 1fr;
  }}
  .metric-row {{
    grid-template-columns: 1fr;
    gap: 0.45rem;
  }}
  .table-head {{
    display: grid;
  }}
}}
</style>
</head>
<body>
<div class="page">
  <section class="hero">
    <div class="bars"><span></span><span></span><span></span></div>
    <div class="hero-inner">
      <div class="hero-top">
        <div class="logo-lockup">{embed_logo()}</div>
        <div class="meta-block">
          <div class="meta-label">Alternate Report</div>
          <div class="meta-value">Barr frontend concept for CDPHE enforcement reporting</div>
        </div>
      </div>
      <div class="hero-grid">
        <div class="hero-copy">
          <div class="eyebrow">Colorado Air Enforcement</div>
          <h1>CDPHE enforcement activity at a glance.</h1>
          <p>{html.escape(narrative)}</p>
        </div>
        <div class="hero-meta">
          <div class="meta-block">
            <div class="meta-label">Document window</div>
            <div class="meta-value">{html.escape(date_span(doc_dates))}</div>
          </div>
          <div class="meta-block">
            <div class="meta-label">Latest document date</div>
            <div class="meta-value">{html.escape(iso_date(newest_date))}</div>
          </div>
          <div class="meta-block">
            <div class="meta-label">Monetary penalties captured</div>
            <div class="meta-value">{html.escape(format_money(total_penalty))}</div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <main class="main">
    <section class="section">
      <div class="section-heading">
        <h2>Selected KPIs</h2>
        <div class="section-rule"></div>
      </div>
      <div class="kpi-band">
        <div class="kpi">
          <div class="kpi-label">Alleged violations</div>
          <div class="kpi-value">{len(rows):,}</div>
          <div class="kpi-note">Per-violation records in the summary CSV.</div>
        </div>
        <div class="kpi">
          <div class="kpi-label">Cases</div>
          <div class="kpi-value">{len(case_ids):,}</div>
          <div class="kpi-note">Case counts deduplicated by case number or file name.</div>
        </div>
        <div class="kpi">
          <div class="kpi-label">Companies</div>
          <div class="kpi-value">{len(companies):,}</div>
          <div class="kpi-note">Distinct company names present in the current dataset.</div>
        </div>
        <div class="kpi">
          <div class="kpi-label">Monetary penalties</div>
          <div class="kpi-value">{html.escape(format_money(total_penalty))}</div>
          <div class="kpi-note">Summed once per case using the largest penalty found per case.</div>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="section-heading">
        <h2>Storyline</h2>
        <div class="section-rule"></div>
      </div>
      <div class="story-grid">
        <div class="story-panel alt">
          <h3>What this view emphasizes</h3>
          <p>This alternate layout trims the interface down to a reporting surface: a single Barr-branded hero, a flat KPI band, ranked operating patterns, and detail tables for recent cases and penalties. The goal is faster scanning and cleaner narrative framing than the default interactive dashboard.</p>
          <p>The strongest signals in this dataset are enforcement type mix, recurring categories, source context, and where monetary penalties are concentrated. Those are surfaced first.</p>
        </div>
        <div class="story-panel">
          <div class="gauge-row">
            {build_radial_gauge(len(case_ids), max(len(rows), 1), "Cases vs. violations")}
          </div>
          <p>Earliest document date: <strong>{html.escape(iso_date(oldest_date))}</strong><br />Latest document date: <strong>{html.escape(iso_date(newest_date))}</strong></p>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="section-heading">
        <h2>Pattern View</h2>
        <div class="section-rule"></div>
        <p>Ranked summaries use Barr’s restrained data palette: blue for enforcement posture, green for category mix, orange for companies, and deeper tones for source and equipment context.</p>
      </div>
      <div class="analytics-grid">
        <div class="analytics-panel">
          <h3>Cases by enforcement type</h3>
          <div class="metric-list">{build_bar_rows(top_enforcement, top_enforcement_count, "blue")}</div>
        </div>
        <div class="analytics-panel">
          <h3>Most frequent categories</h3>
          <div class="metric-list">{build_bar_rows(top_categories, top_category_count, "green")}</div>
        </div>
        <div class="analytics-panel">
          <h3>Companies with most violations</h3>
          <div class="metric-list">{build_bar_rows(top_companies, top_company_count, "orange")}</div>
        </div>
        <div class="analytics-panel">
          <h3>Most common source types</h3>
          <div class="metric-list">{build_bar_rows(top_sources, top_source_count, "burgundy")}</div>
        </div>
        <div class="analytics-panel">
          <h3>Most common equipment tags</h3>
          <div class="metric-list">{build_bar_rows(top_equipment, top_equipment_count, "red")}</div>
        </div>
        <div class="analytics-panel">
          <h3>Reading note</h3>
          <p>Categories, source types, and equipment types are counted from semicolon-delimited fields. Enforcement type is counted once per case to avoid inflating case-based actions from multiple violation rows.</p>
          <p>Penalty totals are conservative at the case level: the report keeps the highest listed penalty per case rather than summing duplicate case rows.</p>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="table-panel">
        <div class="table-head">
          <div>
            <h3>Largest Monetary Penalties</h3>
            <p>Top case-level penalties, linked to the underlying CDPHE PDF when available.</p>
          </div>
        </div>
        <div class="table-wrap">
          {build_table(["Date", "Company", "Case", "Penalty"], top_penalty_rows)}
        </div>
      </div>
    </section>

    <section class="section">
      <div class="table-panel">
        <div class="table-head">
          <div>
            <h3>Recent Case Detail</h3>
            <p>Most recent enforcement rows, ordered by document date and trimmed for quick review.</p>
          </div>
        </div>
        <div class="table-wrap">
          {build_table(["Date", "Company", "Case", "Type", "Category", "Violation summary"], recent_case_rows)}
        </div>
        <div class="table-head">
          <div class="footnote">This alternate file is static HTML by design. It shares the same source CSV as the existing report but omits the heavier interactive filters in favor of a cleaner Barr-style presentation.</div>
        </div>
      </div>
    </section>
  </main>

  <footer class="footer">
    <div class="footer-inner">
      <div>Generated from <code>downloads/cdphe_enforcement_summary.csv</code></div>
      <div>Output: <code>outputs/cdphe_enforcement_summary_report_barr_alt.html</code></div>
    </div>
  </footer>
</div>
</body>
</html>
"""

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_HTML.write_text(html_out, encoding="utf-8")
    print(f"Wrote report {OUTPUT_HTML}")


if __name__ == "__main__":
    main()
