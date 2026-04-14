import runpy
from pathlib import Path

SKILL_PROCESSOR = Path.home() / ".codex" / "skills" / "cdphe-enforcement-parser" / "scripts" / "cdphe_processor.py"


if __name__ == "__main__":
    if not SKILL_PROCESSOR.exists():
        raise SystemExit(f"Skill processor script not found: {SKILL_PROCESSOR}")
    runpy.run_path(str(SKILL_PROCESSOR), run_name="__main__")
