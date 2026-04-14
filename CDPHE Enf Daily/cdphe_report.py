import runpy
from pathlib import Path

SKILL_REPORT = Path.home() / ".codex" / "skills" / "cdphe-enforcement-pipeline" / "scripts" / "cdphe_report.py"


if __name__ == "__main__":
    if not SKILL_REPORT.exists():
        raise SystemExit(f"Skill report script not found: {SKILL_REPORT}")
    runpy.run_path(str(SKILL_REPORT), run_name="__main__")
