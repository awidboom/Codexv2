# PICSummary - Project Goal

## Objective
Create an **agentic**, repeatable workflow that produces a **weekly summary** of work performed on AAW-owned projects from the Excel workbook in this folder (`Vantagepoint In Excel Workbook v3.0.xlsm`).

The output should be:
1) A **point-form** weekly summary grouped at a high level by **Project** and **Person**, with a short synthesized summary of the work descriptions.
2) A separate **hours summary table**: **Person** + **total hours** for the selected week.

## Data Source
- Workbook: `Vantagepoint In Excel Workbook v3.0.xlsm`
- Primary sheet/tab of interest: `Project Det With Timesheet Com`

### Columns of Interest (from `Project Det with Timesheet Com`)
- **Project**: Column **B** (`Project`)
- **Person**: Column **H** (`Expense Name`)
- **Work description**: Column **I** (`Description`)
- **Hours**: Column **J** (`Hours`)

## Current Manual Workflow (Baseline)
1) Open `Vantagepoint In Excel Workbook v3.0.xlsm`
2) On the `START HERE - Select Projects` tab, run **Step 2** to refresh data
3) Go to `Project Det with Timesheet Com`
4) Filter the table by **Week Posted**

## Week Selection Rules
The workbook includes a **Week Posted** filter on the table. Practically, the selected "Week Posted" corresponds to hours worked for the *prior* work-week window:
- **Saturday through Friday** (inclusive), ending **7 days before** the Week Posted date.

Example (clarify when using the tool):
- If filtering to **Week Posted = 2026-01-23 (Fri)**, the worked period is **Sat 2026-01-10 through Fri 2026-01-16**.

Note on "prior week":
- If "this week" is the week ending **2026-01-23**, then the **prior** week would typically be the one ending **2026-01-16**.

## Desired Output

### 1) Weekly Dashboard (Primary)
From a brief glance, answer:
- What did the team work on (projects + people)?
- Are there emerging/new issues (based on new keywords in descriptions)?
- Are hours trending up/down vs prior weeks?

Recommended output: a self-contained HTML dashboard in `outputs/dashboard.html`.

### 2) Point-form Weekly Summary (Secondary)
For the selected **Week Posted**:
- Group by **Project (col B)**
  - Under each project, group by **Person (col H)**
    - Provide a short, merged summary of **work descriptions (col I)**

Example format (illustrative):
- Project: `<Project B>`
  - `<Person H>`: `<1–3 bullets summarizing col I text>`

### 3) Hours Summary Table
For the same selected **Week Posted**:
- Table with:
  - **Person (col H)**
  - **Total hours (sum)** for that week

Open question to resolve before implementation:
- (Resolved) Sum `Hours` (col J) grouped by `Expense Name` (col H).

## Agentic / Skills-Oriented Approach (Target)
Implement an "agentic" workflow that can be run repeatedly each week:
- Identify the target **Week Posted** (explicit date input, or "prior week" relative to today).
- Extract rows from `Project Det with Timesheet Com` for that Week Posted.
- Generate:
  - Project/person point-form summary (with de-duplication and light clustering of similar descriptions).
  - Hours-by-person totals.
- Output as Markdown (and optionally CSV) into this repo (e.g., `outputs/weekly-summary-YYYY-MM-DD.md`).

## Current Automation (Initial)
HTML dashboard (refreshes workbook by default; close Excel first):
- Dashboard: `python scripts/dashboard.py --out outputs/dashboard.html`
- Skip refresh (not recommended): `python scripts/dashboard.py --no-refresh --out outputs/dashboard.html`

Weekly summary (MD/DOCX) (refreshes workbook by default; close Excel first):
- MD: `python scripts/weekly_summary.py --out outputs/weekly-summary-latest.md`
- DOCX + chart: `python scripts/weekly_summary.py --format docx --chart --out outputs/weekly-summary-latest.docx`

## Acceptance Criteria
- User can specify `Week Posted` (date) and get:
  - Project → Person → summarized work text (from col I).
  - Person → summed hours (for the same filtered rows).
- Output is Markdown, easy to paste into email/Teams.
- Handles missing/blank descriptions gracefully.
- Clearly reports the selected week range (Sat–Fri) at the top of the output.
