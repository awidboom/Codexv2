import argparse
import datetime as dt
import json
import re
import subprocess
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path

import pandas as pd


DEFAULT_SHEET = "Detailed Data Table"
PM_SHEET = "Detailed Data Table"


@dataclass(frozen=True)
class WeekWindow:
    week_posted: dt.date
    worked_start: dt.date
    worked_end: dt.date


def parse_date(value: str) -> dt.date:
    try:
        return dt.date.fromisoformat(value)
    except ValueError as exc:
        raise SystemExit(f"Invalid date: {value!r}. Expected YYYY-MM-DD.") from exc


def _log(message: str) -> None:
    ts = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[dashboard] {ts} {message}", file=sys.stderr, flush=True)


def week_window(week_posted: dt.date) -> WeekWindow:
    worked_end = week_posted - dt.timedelta(days=7)
    worked_start = worked_end - dt.timedelta(days=6)
    return WeekWindow(week_posted=week_posted, worked_start=worked_start, worked_end=worked_end)


def _clean_text(value) -> str | None:
    if value is None:
        return None
    if isinstance(value, float) and pd.isna(value):
        return None
    text = str(value).strip()
    if not text:
        return None
    if text.lower() in {"(blank)", "nan", "none"}:
        return None
    return text


def detect_header_row(workbook: Path, sheet: str, max_scan_rows: int = 200) -> int:
    raw = pd.read_excel(
        workbook, sheet_name=sheet, engine="openpyxl", header=None, nrows=max_scan_rows
    )
    for row_idx in range(len(raw)):
        row = raw.iloc[row_idx].astype(str)
        if row.str.contains("Week Posted", case=False, na=False).any() and row.str.contains(
            "Project", case=False, na=False
        ).any():
            return row_idx
    try:
        df0 = pd.read_excel(workbook, sheet_name=sheet, engine="openpyxl", header=0, nrows=0)
    except Exception:
        df0 = None
    if df0 is not None:
        cols = set(map(str, df0.columns))
        alt_required = {
            "ProjectName",
            "ProjDet_DatePostedWeekEndingDate",
            "ProjDet_TotalHours",
            "ProjDet_ExpenseDetailName",
        }
        if alt_required.issubset(cols):
            return 0
    raise SystemExit(
        f"Could not detect header row on sheet {sheet!r}. Try passing --header-row explicitly."
    )


def _workbook_lockfile_path(workbook: Path) -> Path:
    return workbook.with_name(f"~${workbook.name}")


def refresh_workbook_via_excel_com(workbook: Path, timeout_s: int = 900) -> None:
    if sys.platform != "win32":
        raise RuntimeError("Auto-refresh requires Windows + Excel.")

    lockfile = _workbook_lockfile_path(workbook)
    if lockfile.exists():
        raise RuntimeError(
            f"Workbook appears to be open (lock file exists): {lockfile.name!r}. Close Excel and retry."
        )

    ps = f"""
$ErrorActionPreference = 'Stop'
$path = '{str(workbook.resolve()).replace("'", "''")}'
$excel = New-Object -ComObject Excel.Application
$excel.Visible = $false
$excel.DisplayAlerts = $false
$excel.AskToUpdateLinks = $false
$excel.EnableEvents = $false
try {{
  $wb = $excel.Workbooks.Open($path, 0, $false)
  try {{
    foreach ($c in $wb.Connections) {{
      try {{ $c.RefreshWithRefreshAll = $true }} catch {{ }}
      try {{ $c.OLEDBConnection.BackgroundQuery = $false }} catch {{ }}
      try {{ $c.ODBCConnection.BackgroundQuery = $false }} catch {{ }}
    }}
  }} catch {{ }}
  try {{
    foreach ($ws in $wb.Worksheets) {{
      try {{
        foreach ($qt in $ws.QueryTables) {{ $qt.BackgroundQuery = $false }}
      }} catch {{ }}
    }}
  }} catch {{ }}
  $wb.RefreshAll() | Out-Null
  try {{ $excel.CalculateUntilAsyncQueriesDone() | Out-Null }} catch {{ }}
  $saved = $false
  for ($i=0; $i -lt 180; $i++) {{
    try {{
      $wb.Save() | Out-Null
      $saved = $true
      break
    }} catch {{
      Start-Sleep -Seconds 2
    }}
  }}
  if (-not $saved) {{ throw "Workbook save failed after refresh." }}
  $wb.Close($true) | Out-Null
}} finally {{
  try {{ $excel.Quit() | Out-Null }} catch {{ }}
  try {{ [System.Runtime.Interopservices.Marshal]::ReleaseComObject($excel) | Out-Null }} catch {{ }}
  [GC]::Collect()
  [GC]::WaitForPendingFinalizers()
}}
"""

    try:
        subprocess.run(
            ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", ps],
            check=True,
            timeout=timeout_s,
        )
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError(f"Timed out refreshing workbook after {timeout_s}s.") from exc
    except subprocess.CalledProcessError as exc:
        raise RuntimeError(f"Excel refresh failed (exit code {exc.returncode}).") from exc


def load_rows(workbook: Path, sheet: str, header_row: int) -> pd.DataFrame:
    primary_cols = ["Project", "Week Posted", "Expense Name", "Description", "Hours"]
    try:
        df = pd.read_excel(
            workbook,
            sheet_name=sheet,
            engine="openpyxl",
            header=header_row,
            usecols=primary_cols,
        )
    except Exception:
        df = None

    if df is None or not set(primary_cols).issubset(set(df.columns)):
        alt_cols = [
            "ProjectName",
            "ProjDet_DatePostedWeekEndingDate",
            "ProjDet_TotalHours",
            "ProjDet_ExpenseDetailName",
            "ProjDet_DescriptionSummary",
            "ProjDet_Description1",
            "ProjDet_Description2",
        ]
        try:
            df = pd.read_excel(
                workbook,
                sheet_name=sheet,
                engine="openpyxl",
                header=header_row,
                usecols=alt_cols,
            )
        except Exception as exc:
            raise SystemExit(f"Could not read expected columns from sheet {sheet!r}.") from exc

        missing = sorted(set(alt_cols[:4]).difference(set(map(str, df.columns))))
        if missing:
            raise SystemExit(
                f"Missing expected columns on {sheet!r}: {', '.join(missing)}. "
                f"Found: {', '.join(map(str, df.columns))}"
            )

        df = df.copy()
        df["Project"] = df["ProjectName"].map(_clean_text)
        df["Week Posted"] = pd.to_datetime(
            df["ProjDet_DatePostedWeekEndingDate"], errors="coerce", format="mixed"
        ).dt.date
        df["Expense Name"] = df["ProjDet_ExpenseDetailName"].map(_clean_text)
        desc_summary = df.get("ProjDet_DescriptionSummary")
        desc1 = df.get("ProjDet_Description1")
        desc2 = df.get("ProjDet_Description2")
        if desc_summary is not None:
            out_desc = desc_summary.map(_clean_text)
        else:
            out_desc = None
        if out_desc is None and desc1 is not None:
            out_desc = desc1.map(_clean_text)
        if out_desc is not None and desc2 is not None:
            out_desc = out_desc.fillna(desc2.map(_clean_text))
        df["Description"] = out_desc if out_desc is not None else None
        df["Hours"] = pd.to_numeric(df["ProjDet_TotalHours"], errors="coerce").fillna(0.0)
        df = df[primary_cols].copy()
    else:
        df = df.copy()
        df["Project"] = df["Project"].map(_clean_text)
        df["Expense Name"] = df["Expense Name"].map(_clean_text)
        df["Description"] = df["Description"].map(_clean_text)
        df["Week Posted"] = pd.to_datetime(df["Week Posted"], errors="coerce", format="mixed").dt.date
        df["Hours"] = pd.to_numeric(df["Hours"], errors="coerce").fillna(0.0)

    df = df.dropna(subset=["Week Posted"])
    df = df[df["Hours"] != 0.0]
    return df


def load_project_pm_map(workbook: Path) -> dict[str, str]:
    try:
        df = pd.read_excel(
            workbook,
            sheet_name=PM_SHEET,
            engine="openpyxl",
            header=0,
            usecols=["ProjectName", "PMName"],
        )
    except Exception:
        return {}

    df = df.copy()
    df["ProjectName"] = df["ProjectName"].map(_clean_text)
    df["PMName"] = df["PMName"].map(_clean_text)
    df = df[(df["ProjectName"].notna())]
    df["ProjectKey"] = df["ProjectName"].astype(str)
    # Many rows per project; keep the first non-null PMName.
    df = df.sort_values(["ProjectKey"])
    out: dict[str, str] = {}
    for key, pm in df[["ProjectKey", "PMName"]].itertuples(index=False, name=None):
        if key in out:
            continue
        if pm:
            out[key] = pm
    return out


def _format_hours(value: float) -> str:
    return f"{value:.1f}".rstrip("0").rstrip(".")


def _top_description_bullets(descriptions: list[str], max_items: int = 3) -> list[str]:
    counts = Counter([d for d in descriptions if d])
    if not counts:
        return []
    items = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0].lower()))
    bullets: list[str] = []
    for desc, n in items[:max_items]:
        suffix = f" (x{n})" if n > 1 else ""
        bullets.append(f"{desc}{suffix}")
    return bullets


_STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "in",
    "into",
    "is",
    "it",
    "of",
    "on",
    "or",
    "that",
    "the",
    "to",
    "was",
    "were",
    "with",
    "week",
    "project",
    "support",
    "internal",
    "meeting",
    "review",
    "call",
    "calls",
    "email",
    "emails",
    "update",
}


def extract_terms(descriptions: pd.Series) -> Counter:
    text = " ".join([d for d in descriptions.dropna().astype(str).tolist() if d])
    tokens = re.findall(r"[a-z0-9]{3,}", text.lower())
    tokens = [t for t in tokens if t not in _STOPWORDS]
    return Counter(tokens)


def build_week_pack(
    df: pd.DataFrame,
    week_posted: dt.date,
    baseline_weeks: list[dt.date],
    top_n: int,
    project_pm: dict[str, str],
) -> dict:
    wk = df[df["Week Posted"] == week_posted].copy()
    window = week_window(week_posted)

    total_hours = float(wk["Hours"].sum())
    blank_person_hours = float(wk.loc[wk["Expense Name"].isna(), "Hours"].sum())
    blank_project_hours = float(wk.loc[wk["Project"].isna(), "Hours"].sum())
    blank_desc_hours = float(wk.loc[wk["Description"].isna(), "Hours"].sum())

    wk_filtered = wk[(wk["Project"].notna()) & (wk["Expense Name"].notna())]

    people_hours = (
        wk_filtered.groupby("Expense Name")["Hours"].sum().sort_values(ascending=False).reset_index()
    )
    project_hours = (
        wk_filtered.groupby("Project")["Hours"].sum().sort_values(ascending=False).reset_index()
    )
    project_hours_map = {
        p: float(h) for p, h in project_hours.itertuples(index=False, name=None)
    }

    people_top = people_hours.head(top_n)
    project_top = project_hours.head(top_n)

    baseline = df[df["Week Posted"].isin(baseline_weeks)] if baseline_weeks else df.iloc[0:0]
    new_people = []
    new_projects = []
    if not baseline.empty:
        base_people = set(baseline["Expense Name"].dropna().unique().tolist())
        base_projects = set(baseline["Project"].dropna().unique().tolist())
        new_people = sorted(
            [p for p in wk_filtered["Expense Name"].dropna().unique().tolist() if p not in base_people],
            key=str.lower,
        )
        new_projects = sorted(
            [p for p in wk_filtered["Project"].dropna().unique().tolist() if p not in base_projects],
            key=str.lower,
        )

    # Trend comparison (vs immediate previous available week).
    all_weeks_sorted = sorted(df["Week Posted"].unique().tolist())
    idx = all_weeks_sorted.index(week_posted) if week_posted in all_weeks_sorted else -1
    prev_week = all_weeks_sorted[idx - 1] if idx > 0 else None
    prev_total = (
        float(df.loc[df["Week Posted"] == prev_week, "Hours"].sum()) if prev_week is not None else None
    )
    delta = (total_hours - prev_total) if prev_total is not None else None
    pct = (delta / prev_total * 100.0) if prev_total not in (None, 0.0) else None

    # Emerging terms: compare to baseline average.
    current_terms = extract_terms(wk_filtered["Description"])
    baseline_terms = Counter()
    if not baseline.empty:
        baseline_terms = extract_terms(baseline["Description"])
    emerging: list[dict] = []
    if current_terms:
        for term, c in current_terms.most_common(200):
            b = baseline_terms.get(term, 0)
            score = c - (b / max(1, len(baseline_weeks)))
            if score <= 0:
                continue
            emerging.append({"term": term, "score": float(score), "count": int(c), "baseline": int(b)})
        emerging.sort(key=lambda x: (-x["score"], -x["count"], x["term"]))
        emerging = emerging[:20]

    # Details for top projects: project -> person -> bullets
    details: list[dict] = []
    for project in project_top["Project"].tolist():
        proj_rows = wk_filtered[wk_filtered["Project"] == project]
        people = defaultdict(list)
        for person, desc in proj_rows[["Expense Name", "Description"]].itertuples(index=False, name=None):
            if desc:
                people[person].append(desc)
            else:
                people[person]
        people_items = []
        for person in sorted(people.keys(), key=str.lower):
            bullets = _top_description_bullets(people[person])
            people_items.append({"person": person, "bullets": bullets})
        details.append(
            {
                "project": project,
                "pm": project_pm.get(project),
                "hours": project_hours_map.get(project, 0.0),
                "people": people_items,
            }
        )

    return {
        "week_posted": week_posted.isoformat(),
        "work_week_ending": window.worked_end.isoformat(),
        "work_week_start": window.worked_start.isoformat(),
        "kpis": {
            "total_hours": total_hours,
            "projects": int(wk_filtered["Project"].nunique(dropna=True)),
            "people": int(wk_filtered["Expense Name"].nunique(dropna=True)),
            "blank_person_hours": blank_person_hours,
            "blank_project_hours": blank_project_hours,
            "blank_desc_hours": blank_desc_hours,
        },
        "trend": {
            "prev_week_posted": prev_week.isoformat() if prev_week is not None else None,
            "prev_total_hours": prev_total,
            "delta_hours": delta,
            "delta_pct": pct,
        },
        "top_people_hours": [
            {"person": p, "hours": float(h)}
            for p, h in people_top.itertuples(index=False, name=None)
        ],
        "top_project_hours": [
            {"project": p, "hours": float(h)}
            for p, h in project_top.itertuples(index=False, name=None)
        ],
        "new_people": new_people[:25],
        "new_projects": new_projects[:25],
        "emerging_terms": emerging,
        "details": details,
        "_meta": {"top_n": top_n, "baseline_weeks": [d.isoformat() for d in baseline_weeks]},
    }


def build_dashboard_data(
    df: pd.DataFrame, weeks: int, top_n: int, baseline_weeks: int, project_pm: dict[str, str]
) -> dict:
    all_weeks = sorted(df["Week Posted"].unique().tolist())
    if not all_weeks:
        raise SystemExit("No Week Posted values found.")

    selected_weeks = list(reversed(all_weeks))[:weeks]
    selected_weeks = sorted(selected_weeks)

    hours_by_week = (
        df.groupby("Week Posted", as_index=False)["Hours"].sum().sort_values("Week Posted")
    )
    hours_by_week["Work Week Ending"] = hours_by_week["Week Posted"].map(lambda d: d - dt.timedelta(days=7))
    hours_trend = [
        {
            "week_posted": d.isoformat(),
            "work_week_ending": w.isoformat(),
            "hours": float(h),
        }
        for d, w, h in hours_by_week[["Week Posted", "Work Week Ending", "Hours"]].itertuples(
            index=False, name=None
        )
        if d in set(selected_weeks)
    ]

    packs: list[dict] = []
    for i, week_posted in enumerate(selected_weeks):
        baseline = selected_weeks[max(0, i - baseline_weeks) : i]
        packs.append(build_week_pack(df, week_posted, baseline, top_n=top_n, project_pm=project_pm))

    latest = selected_weeks[-1]
    return {
        "generated_at": dt.datetime.now().isoformat(timespec="seconds"),
        "latest_week_posted": latest.isoformat(),
        "weeks": packs,
        "trend": {"hours_by_week": hours_trend},
    }


def render_html(data: dict) -> str:
    data_json = json.dumps(data, ensure_ascii=False)
    # Prevent accidental termination of the JSON script tag if text contains "</script>".
    data_json = data_json.replace("</", "<\\/")

    latest_week_posted = data.get("latest_week_posted")
    latest = None
    for w in data.get("weeks", []):
        if w.get("week_posted") == latest_week_posted:
            latest = w
            break
    latest = latest or (data.get("weeks")[-1] if data.get("weeks") else None)

    def esc(s: str) -> str:
        return (
            str(s)
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
        )

    def pre_kpis_html(w: dict) -> str:
        k = w.get("kpis", {})
        trend = w.get("trend", {}) or {}
        delta = trend.get("delta_hours")
        pct = trend.get("delta_pct")
        if delta is None:
            delta_text = "—"
            delta_cls = "muted"
        else:
            sign = "+" if delta >= 0 else ""
            delta_text = f"{sign}{_format_hours(float(delta))}h"
            if pct is not None:
                delta_text += f" ({sign}{float(pct):.1f}%)"
            delta_cls = "good" if delta >= 0 else "bad"

        items = [
            ("Total Hours", f"{_format_hours(float(k.get('total_hours', 0.0)))}h", ""),
            ("Vs Prior Week", delta_text, delta_cls),
            ("People", str(k.get("people", 0)), ""),
            ("Projects", str(k.get("projects", 0)), ""),
        ]
        out = []
        for label, value, cls in items:
            out.append(
                f"<div class='kpi'><div class='kpi-label'>{esc(label)}</div>"
                f"<div class='kpi-value {cls}'>{esc(value)}</div></div>"
            )
        return "\n".join(out)

    def pre_terms_html(w: dict) -> str:
        terms = (w.get("emerging_terms") or [])[:16]
        if not terms:
            return "<span class='muted'>No emerging terms detected.</span>"
        chips = []
        for t in terms:
            term = t.get("term", "")
            score = t.get("score", 0.0)
            chips.append(f"<span class='chip'>{esc(term)} (+{_format_hours(float(score))})</span>")
        return "\n".join(chips)

    def pre_bar_list(items: list[dict], label_key: str, value_key: str, max_items: int = 25) -> str:
        top = items[:max_items]
        if not top:
            return "<div class='muted'>No data.</div>"
        max_v = max(float(x.get(value_key, 0.0)) for x in top) or 1.0
        rows = []
        for it in top:
            label = it.get(label_key, "")
            v = float(it.get(value_key, 0.0))
            pct = int(round((v / max_v) * 100))
            rows.append(
                "<div class='barrow'>"
                f"<div class='barlabel'>{esc(label)}</div>"
                "<div class='bartrack'>"
                f"<div class='barfill' style='width:{pct}%'></div>"
                f"<div class='barvalue'>{esc(_format_hours(v))}h</div>"
                "</div></div>"
            )
        return "\n".join(rows)

    def pre_trend_svg(trend_items: list[dict]) -> str:
        # Minimal static line chart in SVG (no JS).
        pts = trend_items[-12:]
        if not pts:
            return "<div class='muted'>No trend data.</div>"
        values = [float(p.get("hours", 0.0)) for p in pts]
        labels = [str(p.get("work_week_ending", ""))[5:] for p in pts]
        vmax = max(values) * 1.12 if max(values) > 0 else 1.0
        w, h = 1000, 320
        pad_l, pad_r, pad_t, pad_b = 60, 16, 18, 52
        plot_w, plot_h = w - pad_l - pad_r, h - pad_t - pad_b

        def x(i: int) -> float:
            return pad_l + (plot_w / 2 if len(values) == 1 else i * plot_w / (len(values) - 1))

        def y(v: float) -> float:
            return pad_t + (plot_h - (v / vmax) * plot_h)

        d = " ".join(
            [("M" if i == 0 else "L") + f"{x(i):.1f} {y(v):.1f}" for i, v in enumerate(values)]
        )

        step = 3 if len(labels) > 20 else (2 if len(labels) > 12 else 1)
        xlabels = []
        for i, lbl in enumerate(labels):
            if i % step != 0 and i != len(labels) - 1:
                continue
            xlabels.append(
                f"<text x='{x(i):.1f}' y='{pad_t+plot_h+30}' text-anchor='middle' "
                "fill='#1b2b34' font-size='12'>"
                f"{esc(lbl)}</text>"
            )

        circles = "\n".join(
            [
                f"<circle cx='{x(i):.1f}' cy='{y(v):.1f}' r='4' fill='#0072bc' />"
                for i, v in enumerate(values)
            ]
        )

        return f"""
<svg viewBox="0 0 1000 320" preserveAspectRatio="none">
  <line x1="{pad_l}" y1="{pad_t+plot_h}" x2="{pad_l+plot_w}" y2="{pad_t+plot_h}" stroke="#dfe6ea" stroke-width="2" />
  <line x1="{pad_l}" y1="{pad_t}" x2="{pad_l}" y2="{pad_t+plot_h}" stroke="#dfe6ea" stroke-width="2" />
  <path d="{d}" fill="none" stroke="#0072bc" stroke-width="3" />
  {circles}
  {"".join(xlabels)}
</svg>
""".strip()

    pre = ""
    if latest is not None:
        refresh = data.get("refresh") or {}
        refresh_note = None
        if refresh.get("attempted") and not refresh.get("ok"):
            refresh_note = "REFRESH FAILED (using last saved data)"
        elif refresh.get("attempted") and refresh.get("ok"):
            refresh_note = "refreshed"

        badges = [
            f"Generated {esc(data.get('generated_at', ''))}",
            f"Week Posted {esc(latest.get('week_posted',''))}",
            f"Worked {esc(latest.get('work_week_start',''))} -> {esc(latest.get('work_week_ending',''))}",
        ]
        if refresh_note:
            badges.append(refresh_note)
        badges_html = "".join([f"<span class='badge'>{b}</span>" for b in badges])

        pre = f"""
<noscript>
  <div class="badge-row">
    {badges_html}
  </div>

  <div class="kpis">
    {pre_kpis_html(latest)}
  </div>

    <div class="grid">
      <div class="card full-width">
        <h3 class="section-title">Hours Trend (work-week ending)</h3>
        {pre_trend_svg(((data.get("trend") or {}).get("hours_by_week") or []))}
      </div>
      <div class="card">
        <h3 class="section-title">Top People (hours)</h3>
        <div class="barlist">
          {pre_bar_list(latest.get("top_people_hours") or [], "person", "hours")}
      </div>
    </div>
    <div class="card">
      <h3 class="section-title">Top Projects (hours)</h3>
      <div class="barlist">
        {pre_bar_list(latest.get("top_project_hours") or [], "project", "hours")}
      </div>
    </div>
  </div>
</noscript>
""".strip()

    template = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>PICSummary Dashboard</title>
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
    .wrap {{ max-width: 1200px; margin: 0 auto; padding: 22px; }}
    header {{
      display:flex; gap:16px; align-items:flex-end; justify-content:space-between; flex-wrap:wrap;
      padding: 26px 22px 16px;
      background:
        linear-gradient(120deg, #ffffff 0%, #eef3f6 45%, #f5f8fa 100%),
        radial-gradient(circle at 90% 20%, rgba(31,111,139,0.18), rgba(31,111,139,0) 60%);
      border: 1px solid var(--line);
      border-radius: 14px;
      box-shadow: 0 8px 18px var(--shadow);
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
    header:after {{
      content: "";
      position: absolute;
      right: -40px;
      top: -30px;
      width: 220px;
      height: 220px;
      border-radius: 50%;
      background: radial-gradient(circle, rgba(31,111,139,0.25), rgba(31,111,139,0));
    }}
    header:before {{
      content: "";
      position: absolute;
      left: -60px;
      bottom: -120px;
      width: 240px;
      height: 240px;
      border-radius: 36% 64% 50% 50%;
      background: radial-gradient(circle, rgba(217,121,43,0.18), rgba(217,121,43,0));
    }}
    h1 {{ margin: 0; font-size: 28px; letter-spacing: 0.2px; position: relative; z-index: 1; }}
    .sub {{ color: var(--muted); font-size: 13px; margin-top: 8px; position: relative; z-index: 1; }}
    .controls {{ display:flex; gap:10px; align-items:center; }}
    select, input {{
      background: #ffffff;
      border: 1px solid var(--line);
      color: var(--ink);
      padding: 6px 10px;
      border-radius: 8px;
      font-size: 12px;
      outline: none;
    }}
    .grid {{ display:grid; grid-template-columns: 1fr; gap: 14px; margin-top: 14px; }}
    .full-width {{ grid-column: 1 / -1; }}
    .panel {{
      background: var(--card);
      border: 1px solid var(--line);
      border-radius: 14px;
      padding: 12px 14px;
      box-shadow: 0 8px 18px var(--shadow);
      position: relative;
      overflow: hidden;
    }}
    .panel:before {{
      content: "";
      position: absolute;
      right: -60px;
      top: -80px;
      width: 160px;
      height: 160px;
      border-radius: 50%;
      background: radial-gradient(circle, rgba(0,114,188,0.18), rgba(0,114,188,0));
    }}
    .kpis {{ display:grid; grid-template-columns: repeat(2, minmax(0,1fr)); gap: 10px; }}
    @media (min-width: 680px) {{ .kpis {{ grid-template-columns: repeat(4, minmax(0,1fr)); }} }}
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
    .kpi .label {{ font-size: 12px; color: var(--muted); text-transform: uppercase; letter-spacing: 0.08em; }}
    .kpi .value {{ font-size: 22px; margin-top: 4px; color: var(--ink); }}
    .row {{ display:flex; gap: 12px; flex-wrap:wrap; }}
    .row > .panel {{ flex: 1; min-width: 320px; }}
    .title {{ display:flex; align-items:baseline; justify-content:space-between; gap:12px; }}
    .title h2 {{ margin: 0; font-size: 14px; letter-spacing: 0.2px; }}
    .pill {{
      display:inline-block; padding: 6px 10px; border-radius: 999px;
      border: 1px solid var(--line); background: #f6fbfd;
      color: var(--muted); font-size: 11px; text-transform: uppercase; letter-spacing: 0.08em;
    }}
    svg {{ width: 100%; height: 280px; display:block; }}
    .bars svg {{ height: 320px; }}
    .muted {{ color: var(--muted); }}
    .good {{ color: var(--sky); }}
    .bad {{ color: var(--rust); }}
    .list {{ margin: 8px 0 0 0; padding-left: 18px; color: var(--ink); }}
    .chips {{ display:flex; flex-wrap:wrap; gap: 8px; margin-top: 10px; }}
    .chip {{
      border: 1px solid var(--line);
      padding: 6px 10px;
      border-radius: 999px;
      font-size: 11px;
      background: #ffffff;
      color: var(--muted);
      white-space: nowrap;
    }}
    .barlist {{ margin-top: 10px; display:flex; flex-direction:column; gap: 8px; }}
    .barrow {{ display:grid; grid-template-columns: 280px 1fr; gap: 12px; align-items:center; }}
    .barlabel {{ color: var(--muted); font-size: 13px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }}
    .bartrack {{
      position: relative;
      height: 18px;
      border-radius: 10px;
      border: 1px solid var(--line);
      background: #f6fbfd;
      overflow: hidden;
    }}
    .barfill {{
      height: 100%;
      background: rgba(0,114,188,0.45);
    }}
    .barvalue {{
      position: absolute;
      right: 8px;
      top: 50%;
      transform: translateY(-50%);
      color: var(--ink);
      font-size: 13px;
    }}
    details {{
      margin-top: 10px;
      border-top: 1px solid var(--line);
      padding-top: 10px;
    }}
    details > summary {{
      cursor: pointer;
      color: var(--ink);
      font-weight: 600;
      list-style: none;
    }}
    details summary::-webkit-details-marker {{ display:none; }}
    .proj {{
      margin-top: 10px;
      padding: 10px;
      border-radius: 14px;
      border: 1px solid var(--line);
      background: #ffffff;
    }}
    .proj h3 {{ margin: 0 0 6px 0; font-size: 13px; }}
    .person {{ margin: 6px 0; }}
    .person .name {{ font-weight: 600; }}
    .person ul {{ margin: 4px 0 0 18px; }}
    .footer {{ margin-top: 14px; color: var(--muted); font-size: 12px; }}
    .js-only { display: none; }
    .js .js-only { display: block; }
  </style>
  <script>document.documentElement.classList.add('js');</script>
</head>
<body>
  <div class="wrap">
    <header>
      <div class="header-band"></div>
      <div class="header-band secondary"></div>
      <div>
        <h1>PICSummary Dashboard</h1>
        <div class="sub" id="subtitle">If you are viewing this inside an IDE preview that blocks JavaScript, you'll still see a static snapshot below. Open in a browser for interactivity.</div>
      </div>
      <div class="controls">
        <label class="muted" for="weekSel">Week Posted</label>
        <select id="weekSel"></select>
        <input id="search" placeholder="Search project/person/description" />
      </div>
    </header>
    __PRE_RENDERED__

    <div class="js-only">
    <!-- Interactive (JS) containers -->
    <div class="panel">
      <div class="kpis" id="kpis"></div>
    </div>

      <div class="grid">
        <div class="panel full-width">
          <div class="title">
            <h2>Hours Trend (work-week ending)</h2>
            <span class="pill" id="trendPill"></span>
          </div>
          <svg id="trendSvg" viewBox="0 0 1000 320" preserveAspectRatio="none"></svg>
        </div>
      </div>

    <div class="row">
      <div class="panel bars">
        <div class="title">
          <h2>Top People (hours)</h2>
          <span class="pill" id="peoplePill"></span>
        </div>
        <svg id="peopleSvg" viewBox="0 0 1000 360" preserveAspectRatio="none"></svg>
      </div>
      <div class="panel bars">
        <div class="title">
          <h2>Top Projects (hours)</h2>
          <span class="pill" id="projPill"></span>
        </div>
        <svg id="projSvg" viewBox="0 0 1000 360" preserveAspectRatio="none"></svg>
      </div>
    </div>

    <div class="panel">
      <div class="title">
        <h2>Project / Person Details</h2>
        <span class="pill">top projects</span>
      </div>
      <details open>
        <summary>Show / hide details</summary>
        <div id="details"></div>
      </details>
    </div>

    <div class="footer" id="footer"></div>
    </div>
  </div>

  <script id="data" type="application/json">__DATA_JSON__</script>
  <script>
    const DATA = JSON.parse(document.getElementById('data').textContent);
    const weekSel = document.getElementById('weekSel');
    const search = document.getElementById('search');

    function fmtHours(x) {{
      if (x === null || x === undefined || Number.isNaN(x)) return '—';
      return (Math.round(x * 10) / 10).toString();
    }}

    function byLower(a,b) {{ return a.toLowerCase().localeCompare(b.toLowerCase()); }}

    function getWeek(weekPosted) {{
      return DATA.weeks.find(w => w.week_posted === weekPosted);
    }}

    function setSubtitle(w) {{
      const refreshNote = (DATA.refresh && DATA.refresh.attempted && !DATA.refresh.ok)
        ? ` · REFRESH FAILED (using last saved data)`
        : (DATA.refresh && DATA.refresh.attempted ? ` · refreshed` : '');
      document.getElementById('subtitle').textContent =
        `Generated ${DATA.generated_at}${refreshNote} · Week Posted ${w.week_posted} · Worked ${w.work_week_start} → ${w.work_week_ending}`;
      document.getElementById('footer').textContent =
        `Source: Vantagepoint workbook · Blank person hours: ${fmtHours(w.kpis.blank_person_hours)} · Blank description hours: ${fmtHours(w.kpis.blank_desc_hours)}`;
    }}

    function renderKpis(w) {{
      const k = w.kpis;
      const trend = w.trend || {{}};
      const delta = trend.delta_hours;
      const pct = trend.delta_pct;
      const deltaText = (delta === null || delta === undefined) ? '—' : `${delta >= 0 ? '+' : ''}${fmtHours(delta)}h`;
      const pctText = (pct === null || pct === undefined) ? '' : ` (${pct >= 0 ? '+' : ''}${pct.toFixed(1)}%)`;
      const deltaClass = (delta === null || delta === undefined) ? 'muted' : (delta >= 0 ? 'good' : 'bad');
      const el = document.getElementById('kpis');
      el.innerHTML = '';
      const items = [
        {{label:'Total Hours', value:`${fmtHours(k.total_hours)}h`}},
        {{label:'Vs Prior Week', value:`${deltaText}${pctText}`, cls:deltaClass}},
        {{label:'People', value:k.people}},
        {{label:'Projects', value:k.projects}},
      ];
      for (const it of items) {{
        const d = document.createElement('div');
        d.className = 'kpi';
        d.innerHTML = `<div class="label">${it.label}</div><div class="value ${it.cls||''}">${it.value}</div>`;
        el.appendChild(d);
      }}
    }}

    function drawLineChart(svgId, points, xKey, yKey, labelsKey) {{
      const svg = document.getElementById(svgId);
      svg.innerHTML = '';
      const W = 1000, H = 320;
      const pad = {{l: 60, r: 16, t: 18, b: 52}};
      const w = W - pad.l - pad.r, h = H - pad.t - pad.b;
      const xs = points.map((p,i) => i);
      const ys = points.map(p => p[yKey]);
      const yMax = Math.max(1, ...ys) * 1.12;

      function x(i) {{ return pad.l + (xs.length === 1 ? w/2 : (i * w / (xs.length - 1))); }}
      function y(v) {{ return pad.t + (h - (v / yMax) * h); }}

      // axes
      const axis = (x1,y1,x2,y2, stroke, sw) => {{
        const l = document.createElementNS('http://www.w3.org/2000/svg','line');
        l.setAttribute('x1', x1); l.setAttribute('y1', y1);
        l.setAttribute('x2', x2); l.setAttribute('y2', y2);
        l.setAttribute('stroke', stroke); l.setAttribute('stroke-width', sw);
        svg.appendChild(l);
      }};
      axis(pad.l, pad.t+h, pad.l+w, pad.t+h, '#dfe6ea', 2);
      axis(pad.l, pad.t, pad.l, pad.t+h, '#dfe6ea', 2);

      // grid + y labels
      for (let i=0; i<=4; i++) {{
        const v = (yMax * i / 4);
        const yy = y(v);
        axis(pad.l, yy, pad.l+w, yy, 'rgba(27,43,52,0.08)', 1);
        const t = document.createElementNS('http://www.w3.org/2000/svg','text');
        t.setAttribute('x', 6); t.setAttribute('y', yy+4);
        t.setAttribute('fill','#1b2b34');
        t.setAttribute('font-size','12');
        t.textContent = Math.round(v).toString();
        svg.appendChild(t);
      }}

      // path
      let d = '';
      points.forEach((p,i) => {{
        const xx = x(i), yy = y(p[yKey]);
        d += (i===0 ? 'M' : 'L') + xx + ' ' + yy + ' ';
      }});
      const path = document.createElementNS('http://www.w3.org/2000/svg','path');
      path.setAttribute('d', d.trim());
      path.setAttribute('fill','none');
      path.setAttribute('stroke','#0072bc');
      path.setAttribute('stroke-width','3');
      svg.appendChild(path);

      // markers + x labels
      const step = points.length > 20 ? 3 : (points.length > 12 ? 2 : 1);
      points.forEach((p,i) => {{
        const xx = x(i), yy = y(p[yKey]);
        const c = document.createElementNS('http://www.w3.org/2000/svg','circle');
        c.setAttribute('cx', xx); c.setAttribute('cy', yy); c.setAttribute('r', 4);
        c.setAttribute('fill','#0072bc');
        svg.appendChild(c);
        if (i % step === 0 || i === points.length - 1) {{
          const tx = document.createElementNS('http://www.w3.org/2000/svg','text');
          tx.setAttribute('x', xx); tx.setAttribute('y', pad.t+h+30);
          tx.setAttribute('text-anchor','middle');
          tx.setAttribute('fill','#1b2b34');
          tx.setAttribute('font-size','12');
          tx.textContent = p[labelsKey];
          svg.appendChild(tx);
        }}
      }});
    }}

    function drawBarChart(svgId, items, labelKey, valueKey, maxLabelLen) {{
      const svg = document.getElementById(svgId);
      svg.innerHTML = '';
      const W = 1000;
      const n = Math.min(items.length, 25);
      const H = Math.max(360, 24 * n + 80);
      svg.setAttribute('viewBox', `0 0 ${W} ${H}`);
      svg.style.height = `${Math.min(840, H)}px`;

      const pad = {{l: 320, r: 90, t: 18, b: 18}};
      const w = W - pad.l - pad.r, h = H - pad.t - pad.b;
      const top = items.slice(0,n);
      const maxV = Math.max(1, ...top.map(x => x[valueKey]));
      const barH = h / n;

      function trunc(s) {{
        if (s.length <= maxLabelLen) return s;
        return s.slice(0, maxLabelLen-1) + '…';
      }}

      top.forEach((it, i) => {{
        const y = pad.t + i*barH + 6;
        const v = it[valueKey];
        const bw = Math.round((v / maxV) * w);

        const bg = document.createElementNS('http://www.w3.org/2000/svg','rect');
        bg.setAttribute('x', pad.l); bg.setAttribute('y', y);
        bg.setAttribute('width', w); bg.setAttribute('height', barH-10);
        bg.setAttribute('rx', 8); bg.setAttribute('fill','#f6fbfd');
        svg.appendChild(bg);

        const r = document.createElementNS('http://www.w3.org/2000/svg','rect');
        r.setAttribute('x', pad.l); r.setAttribute('y', y);
        r.setAttribute('width', bw); r.setAttribute('height', barH-10);
        r.setAttribute('rx', 8); r.setAttribute('fill','rgba(0,114,188,0.45)');
        svg.appendChild(r);

        const t = document.createElementNS('http://www.w3.org/2000/svg','text');
        t.setAttribute('x', pad.l - 10); t.setAttribute('y', y + (barH-10)/2 + 4);
        t.setAttribute('text-anchor','end');
        t.setAttribute('fill','#1b2b34');
        t.setAttribute('font-size','14');
        t.textContent = trunc(it[labelKey]);
        svg.appendChild(t);

        const tv = document.createElementNS('http://www.w3.org/2000/svg','text');
        tv.setAttribute('x', W - 10); tv.setAttribute('y', y + (barH-10)/2 + 4);
        tv.setAttribute('text-anchor','end');
        tv.setAttribute('fill','#1b2b34');
        tv.setAttribute('font-size','14');
        tv.textContent = fmtHours(v) + 'h';
        svg.appendChild(tv);
      }});
    }}

    function renderDetails(w, q) {{
      const el = document.getElementById('details');
      el.innerHTML = '';
      const query = (q || '').trim().toLowerCase();
      const blocks = w.details || [];
      for (const proj of blocks) {{
        const projText = (proj.project + ' ' + (proj.pm || '')).toLowerCase();
        const projDiv = document.createElement('div');
        projDiv.className = 'proj';
        const h = document.createElement('h3');
        h.textContent = proj.project;
        projDiv.appendChild(h);

        const meta = document.createElement('div');
        meta.className = 'muted';
        meta.style.fontSize = '12px';
        const pm = proj.pm ? proj.pm : '—';
        const hrs = (proj.hours === null || proj.hours === undefined) ? '—' : fmtHours(proj.hours) + 'h';
        meta.textContent = `PM: ${pm} · Hours: ${hrs}`;
        projDiv.appendChild(meta);

        let any = false;
        for (const p of proj.people) {{
          const personText = p.person.toLowerCase();
          const bulletsText = (p.bullets || []).join(' ').toLowerCase();
          if (query && !(projText.includes(query) || personText.includes(query) || bulletsText.includes(query))) {{
            continue;
          }}
          any = true;
          const row = document.createElement('div');
          row.className = 'person';
          row.innerHTML = `<div class="name">${p.person}</div>`;
          const ul = document.createElement('ul');
          for (const b of (p.bullets || [])) {{
            const li = document.createElement('li');
            li.textContent = b;
            ul.appendChild(li);
          }}
          if (!(p.bullets || []).length) {{
            const li = document.createElement('li');
            li.className = 'muted';
            li.textContent = '(no description provided)';
            ul.appendChild(li);
          }}
          row.appendChild(ul);
          projDiv.appendChild(row);
        }}
        if (any) el.appendChild(projDiv);
      }}
      if (!el.children.length) {{
        el.innerHTML = '<div class="muted">No matching details.</div>';
      }}
    }}

    function renderAll() {{
      const w = getWeek(weekSel.value);
      setSubtitle(w);
      renderKpis(w);

      const trend = DATA.trend.hours_by_week.map(p => ({{...p, label: p.work_week_ending.slice(5)}}));
      drawLineChart('trendSvg', trend, 'work_week_ending', 'hours', 'label');
      document.getElementById('trendPill').textContent = `${trend.length} weeks`;

      drawBarChart('peopleSvg', w.top_people_hours, 'person', 'hours', 26);
      drawBarChart('projSvg', w.top_project_hours, 'project', 'hours', 32);
      document.getElementById('peoplePill').textContent = `Top ${w._meta.top_n}`;
      document.getElementById('projPill').textContent = `Top ${w._meta.top_n}`;

      renderDetails(w, search.value);
    }}

    function init() {{
      const opts = DATA.weeks.map(w => w.week_posted);
      for (const o of opts) {{
        const opt = document.createElement('option');
        opt.value = o; opt.textContent = o;
        weekSel.appendChild(opt);
      }}
      weekSel.value = DATA.latest_week_posted;
      weekSel.addEventListener('change', renderAll);
      search.addEventListener('input', () => renderDetails(getWeek(weekSel.value), search.value));
      renderAll();
    }}
    init();
  </script>
</body>
</html>
"""
    template = template.replace("{{", "{").replace("}}", "}")
    return template.replace("__DATA_JSON__", data_json).replace("__PRE_RENDERED__", pre)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate an HTML dashboard from the PICSummary workbook.")
    parser.add_argument(
        "--workbook",
        default="Vantagepoint In Excel Workbook v3.0.xlsm",
        help="Path to the Excel workbook (.xlsx/.xlsm).",
    )
    parser.add_argument("--sheet", default=DEFAULT_SHEET, help="Sheet name to read.")
    parser.add_argument(
        "--header-row",
        type=int,
        default=None,
        help="0-based row index to use as the header row. If omitted, attempts to auto-detect.",
    )
    parser.add_argument(
        "--weeks",
        type=int,
        default=12,
        help="Number of weeks to include in the dashboard trend.",
    )
    parser.add_argument(
        "--baseline-weeks",
        type=int,
        default=4,
        help="How many prior weeks to use for 'emerging' comparisons.",
    )
    parser.add_argument(
        "--top-n",
        type=int,
        default=25,
        help="Top-N people/projects and projects-for-details.",
    )
    parser.add_argument(
        "--no-refresh",
        action="store_true",
        help="Skip Excel refresh (not recommended).",
    )
    parser.add_argument(
        "--require-refresh",
        action="store_true",
        help="Fail the run if workbook refresh fails.",
    )
    parser.add_argument(
        "--out",
        default="outputs/dashboard.html",
        help="Output HTML path.",
    )
    args = parser.parse_args()

    workbook = Path(args.workbook)
    if not workbook.exists():
        raise SystemExit(f"Workbook not found: {str(workbook)!r}")

    _log(f"Workbook: {workbook.resolve()}")
    _log(f"Sheet: {args.sheet!r}")

    _log("Detecting header row...")
    header_row = args.header_row if args.header_row is not None else detect_header_row(workbook, args.sheet)
    _log(f"Header row: {header_row}")

    refresh = {"attempted": False, "ok": None, "error": None}
    if not args.no_refresh:
        refresh["attempted"] = True
        try:
            _log("Refreshing workbook via Excel COM...")
            refresh_workbook_via_excel_com(workbook)
            refresh["ok"] = True
            _log("Workbook refresh: OK")
        except Exception as exc:
            refresh["ok"] = False
            refresh["error"] = str(exc)
            _log(f"Workbook refresh: FAILED ({exc})")
            if args.require_refresh:
                raise SystemExit(str(exc)) from exc

    _log("Loading rows...")
    df = load_rows(workbook, args.sheet, header_row)
    _log(f"Loaded {len(df):,} rows")

    _log("Loading project PM map...")
    project_pm = load_project_pm_map(workbook)
    _log(f"Loaded {len(project_pm):,} project PM entries")

    _log("Building dashboard data...")
    data = build_dashboard_data(
        df,
        weeks=max(2, int(args.weeks)),
        top_n=max(5, int(args.top_n)),
        baseline_weeks=max(1, int(args.baseline_weeks)),
        project_pm=project_pm,
    )
    data["refresh"] = refresh

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    _log(f"Writing HTML: {out_path.resolve()}")
    out_path.write_text(render_html(data), encoding="utf-8")
    _log("Done")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
