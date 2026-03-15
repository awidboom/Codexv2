# Scripts

## `monitor_baaqmd.py`
Monitors the BAAQMD sources listed in `AGENTS.md`, tracks changes over time, and writes a digest.

Run:
- `python scripts/monitor_baaqmd.py`

Outputs:
- `outputs/baaqmd_digest.md` (human-readable summary)
- `outputs/baaqmd_digest.html` (self-contained HTML page)
- `data/monitor/baaqmd_state.json` (machine-readable last-seen state)

## Scheduling (Windows Task Scheduler)
Quick start (weekly, Monday 8:00 AM):
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/schedule_weekly.ps1`

Manual run wrapper (writes a log):
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/run_monitor.ps1`

If you can't run PowerShell scripts, use the BAT wrapper:
- `scripts\\run_monitor.bat`
