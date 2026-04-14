import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
CONFIG_PATH = BASE_DIR / "tool_config.json"
INPUT_DIR = BASE_DIR / "input"

DEFAULT_CONFIG = {
    "facility_name": "New Facility",
    "client_name": "Client Name",
    "project_name": "SI Quick Reference",
    "si_workbook": "",
    "baseline_workbook": "",
    "lookup_title": "Emission Unit Detail Lookup",
    "baseline_title": "Emission Calculation Dashboard",
}

def load_config():
    config = DEFAULT_CONFIG.copy()
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, "r", encoding="utf-8") as handle:
            config.update(json.load(handle))
    return config

def _resolve_candidate(path_value):
    if not path_value:
        return None
    candidate = Path(path_value)
    if not candidate.is_absolute():
        candidate = BASE_DIR / candidate
    return candidate if candidate.exists() else None

def _scan_for_file(keywords, extensions):
    for root in (INPUT_DIR, BASE_DIR):
        if not root.exists():
            continue
        for path in root.iterdir():
            if not path.is_file() or path.suffix.lower() not in extensions:
                continue
            name = path.name.lower()
            if all(keyword in name for keyword in keywords):
                return path
    return None

def resolve_si_workbook(config=None):
    config = config or load_config()
    explicit = _resolve_candidate(config.get("si_workbook"))
    if explicit:
        return explicit
    extensions = {".xlsx", ".xlsm", ".xls"}
    for keywords in (["subject", "item"], ["subject", "details"], ["si"], ["emission"]):
        candidate = _scan_for_file(keywords, extensions)
        if candidate:
            return candidate
    excel_files = []
    for root in (INPUT_DIR, BASE_DIR):
        if not root.exists():
            continue
        excel_files.extend(
            path for path in root.iterdir() if path.is_file() and path.suffix.lower() in extensions
        )
    if len(excel_files) == 1:
        return excel_files[0]
    raise FileNotFoundError("No SI workbook found. Put it in input/ and set si_workbook in tool_config.json.")

def resolve_baseline_workbook(config=None):
    config = config or load_config()
    explicit = _resolve_candidate(config.get("baseline_workbook"))
    if explicit:
        return explicit
    for keywords in (["calcs"], ["pte"]):
        candidate = _scan_for_file(keywords, {".xlsx", ".xlsm", ".xls"})
        if candidate:
            return candidate
    raise FileNotFoundError("No baseline workbook found. Put it in input/ and set baseline_workbook in tool_config.json.")
