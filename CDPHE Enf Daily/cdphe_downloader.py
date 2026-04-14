import runpy
from pathlib import Path
SKILL_DOWNLOADER = Path.home() / ".codex" / "skills" / "cdphe-downloader" / "scripts" / "cdphe_downloader.py"


if __name__ == "__main__":
    if not SKILL_DOWNLOADER.exists():
        raise SystemExit(f"Skill downloader script not found: {SKILL_DOWNLOADER}")
    runpy.run_path(str(SKILL_DOWNLOADER), run_name="__main__")
