from __future__ import annotations

import csv
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
INPUT_DIR = ROOT / "data" / "permit_evaluations_json"
OUTPUT_DIR = ROOT / "outputs" / "permit_evaluation_json_audit"

MASTER_SECTIONS = [
    "background",
    "emission_calculations",
    "cumulative_increase",
    "toxic_risk_screening_analysis",
    "BACT",
    "offsets",
    "PSD_applicability",
    "CEQA",
    "Statement_of_Compliance",
    "public_notification",
    "conditions",
    "permit_conditions",
    "TitleV_permit",
    "recommendation",
]

RAW_ALIAS_TO_SECTION = {
    "BACKGROUND": ("background",),
    "EMISSIONS": ("emission_calculations",),
    "CUMULATIVE_INCREASE": ("cumulative_increase",),
    "TOXICS": ("toxic_risk_screening_analysis",),
    "BACT": ("BACT",),
    "OFFSETS": ("offsets",),
    "PSD": ("PSD_applicability",),
    "CEQA": ("CEQA",),
    "SOC": ("Statement_of_Compliance",),
    "PUBLIC_NOTIFICATION": ("public_notification",),
    "PERMIT_CONDITIONS": ("conditions", "permit_conditions"),
    "STANDARD_CONDITIONS": ("conditions", "permit_conditions"),
    "RECOMMENDATION": ("recommendation",),
    "TITLEV": ("TitleV_permit",),
}

UNMAPPED_HINTS = {
    "background": (
        "background",
        "project description",
        "authority to construct",
        "permit to operate",
    ),
    "emission_calculations": (
        "emission calculations",
        "potential to emit",
        "pte",
        "emission factor",
        "table 1",
        "table 2",
    ),
    "cumulative_increase": (
        "cumulative increase",
        "plant cumulative emissions",
        "facility cumulative",
        "table 3",
    ),
    "toxic_risk_screening_analysis": (
        "toxic",
        "health risk",
        "hra",
        "tbact",
        "tac",
    ),
    "BACT": (
        "best available control technology",
        "bact",
        "t-bact",
        "tbact",
    ),
    "offsets": ("offsets", "offset ratio", "required offsets"),
    "PSD_applicability": (
        "prevention of significant deterioration",
        "psd",
        "major source",
        "major facility",
    ),
    "CEQA": ("ceqa", "environmental quality act", "notice of exemption", "ministerial"),
    "Statement_of_Compliance": (
        "statement of compliance",
        "regulation 1",
        "regulation 2",
        "regulation 6",
        "regulation 8",
        "regulation 9",
    ),
    "public_notification": (
        "public notification",
        "regulation 2-1-412",
        "regulation 2 -1-412",
        "school notification",
        "public notice",
    ),
    "conditions": (
        "permit conditions",
        "condition number",
        "cond#",
    ),
    "permit_conditions": (
        "permit conditions",
        "condition number",
        "cond#",
    ),
    "TitleV_permit": (
        "title v",
        "major facility review",
        "synthetic minor",
    ),
    "recommendation": ("recommendation", "issue an authority to construct", "we recommend"),
}


@dataclass
class SectionEvidence:
    alias_hits: list[dict[str, str]]
    unmapped_hits: list[str]

    @property
    def has_candidate(self) -> bool:
        return bool(self.alias_hits or self.unmapped_hits)

    @property
    def has_alias_candidate(self) -> bool:
        return bool(self.alias_hits)

    @property
    def has_unmapped_candidate(self) -> bool:
        return bool(self.unmapped_hits)

    def sample(self, limit: int = 240) -> str:
        if self.alias_hits:
            first = self.alias_hits[0]
            text = first["text"]
            return f"alias:{first['alias']} heading={first['heading']} text={text[:limit]}"
        if self.unmapped_hits:
            return f"unmapped:{self.unmapped_hits[0][:limit]}"
        return ""


def clean_text(value: Any) -> str:
    if value is None:
        return ""
    return re.sub(r"\s+", " ", str(value)).strip()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def has_meaningful_text(value: str | None) -> bool:
    return bool(clean_text(value or ""))


def recursive_has_content(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return has_meaningful_text(value)
    if isinstance(value, (int, float, bool)):
        return True
    if isinstance(value, list):
        return any(recursive_has_content(item) for item in value)
    if isinstance(value, dict):
        return any(recursive_has_content(item) for item in value.values())
    return False


def table_has_rows(table: Any) -> bool:
    if not isinstance(table, dict):
        return False
    rows = table.get("rows", [])
    if not isinstance(rows, list):
        return False
    for row in rows:
        if isinstance(row, list) and any(recursive_has_content(cell) for cell in row):
            return True
        if isinstance(row, dict) and recursive_has_content(row):
            return True
    return False


def section_is_populated(section: str, value: Any) -> bool:
    if section in {
        "background",
        "emission_calculations",
        "cumulative_increase",
        "BACT",
        "public_notification",
        "conditions",
        "recommendation",
    }:
        return has_meaningful_text((value or {}).get("text")) if isinstance(value, dict) else False

    if section == "toxic_risk_screening_analysis":
        if not isinstance(value, dict):
            return False
        status = clean_text(value.get("status"))
        narrative = clean_text(value.get("narrative"))
        return bool(status or narrative)

    if section == "offsets":
        if not isinstance(value, dict):
            return False
        return has_meaningful_text(value.get("narrative")) or table_has_rows(value.get("table"))

    if section == "PSD_applicability":
        return has_meaningful_text((value or {}).get("narrative")) if isinstance(value, dict) else False

    if section == "CEQA":
        return has_meaningful_text((value or {}).get("narrative")) if isinstance(value, dict) else False

    if section == "Statement_of_Compliance":
        return recursive_has_content(value)

    if section == "permit_conditions":
        if not isinstance(value, dict):
            return False
        if has_meaningful_text(value.get("condition_number")):
            return True
        items = value.get("items", [])
        if not isinstance(items, list):
            return False
        return any(
            isinstance(item, dict) and recursive_has_content(item.get("text"))
            for item in items
        )

    if section == "TitleV_permit":
        if not isinstance(value, dict):
            return False
        return (
            has_meaningful_text(value.get("narrative"))
            or recursive_has_content(value.get("revisions"))
            or recursive_has_content(value.get("affected_sources"))
        )

    return recursive_has_content(value)


def gather_raw_evidence(raw_sections: dict[str, Any]) -> dict[str, SectionEvidence]:
    evidence = {
        section: SectionEvidence(alias_hits=[], unmapped_hits=[])
        for section in MASTER_SECTIONS
    }

    for block in raw_sections.get("blocks", []):
        text = clean_text(block.get("text", ""))
        if not text:
            continue
        alias = block.get("alias")
        heading = clean_text(block.get("heading", ""))
        for section in RAW_ALIAS_TO_SECTION.get(alias, ()):
            evidence[section].alias_hits.append(
                {"alias": alias or "", "heading": heading, "text": text}
            )

    for block in raw_sections.get("unmapped_blocks", []):
        if isinstance(block, dict):
            block_text = clean_text(" ".join(str(v) for v in block.values() if v is not None))
        else:
            block_text = clean_text(str(block))
        if not block_text:
            continue
        lower = block_text.lower()
        for section, hints in UNMAPPED_HINTS.items():
            if any(hint in lower for hint in hints):
                evidence[section].unmapped_hits.append(block_text)

    return evidence


def build_row(path: Path) -> dict[str, Any]:
    obj = load_json(path)
    raw_sections = obj.get("raw_sections", {})
    raw_evidence = gather_raw_evidence(raw_sections)

    row: dict[str, Any] = {
        "relative_path": path.relative_to(ROOT).as_posix(),
        "file_name": path.name,
        "application_number": obj.get("application_number"),
        "plant_name": ((obj.get("plant") or {}).get("name") if isinstance(obj.get("plant"), dict) else None),
        "evaluation_date": obj.get("evaluation_date"),
        "raw_block_count": len(raw_sections.get("blocks", [])),
        "raw_unmapped_block_count": len(raw_sections.get("unmapped_blocks", [])),
    }

    missing_count = 0
    missing_with_raw_count = 0
    missing_with_alias_raw_count = 0

    for section in MASTER_SECTIONS:
        populated = section_is_populated(section, obj.get(section))
        evidence = raw_evidence[section]
        raw_candidate = (not populated) and evidence.has_candidate
        raw_alias_candidate = (not populated) and evidence.has_alias_candidate
        raw_unmapped_candidate = (not populated) and evidence.has_unmapped_candidate
        row[f"{section}__populated"] = "yes" if populated else "no"
        row[f"{section}__raw_candidate"] = "yes" if raw_candidate else "no"
        row[f"{section}__raw_alias_candidate"] = "yes" if raw_alias_candidate else "no"
        row[f"{section}__raw_unmapped_candidate"] = "yes" if raw_unmapped_candidate else "no"
        row[f"{section}__raw_alias_hits"] = len(evidence.alias_hits)
        row[f"{section}__raw_unmapped_hits"] = len(evidence.unmapped_hits)
        row[f"{section}__raw_sample"] = evidence.sample()
        if not populated:
            missing_count += 1
            if raw_candidate:
                missing_with_raw_count += 1
            if raw_alias_candidate:
                missing_with_alias_raw_count += 1

    row["missing_master_section_count"] = missing_count
    row["missing_sections_with_raw_candidates"] = missing_with_raw_count
    row["missing_sections_with_alias_raw_candidates"] = missing_with_alias_raw_count
    return row


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        return
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def build_summary(rows: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], str]:
    total = len(rows)
    section_rows: list[dict[str, Any]] = []
    lines: list[str] = []

    lines.append("# Permit Evaluation JSON Audit")
    lines.append("")
    lines.append(f"- JSON files audited: {total}")
    lines.append(f"- Input folder: `{INPUT_DIR}`")
    lines.append(f"- Generated from: `scripts/audit_permit_evaluation_jsons.py`")
    lines.append("")
    lines.append("## Section Summary")
    lines.append("")

    for section in MASTER_SECTIONS:
        populated = sum(1 for row in rows if row[f"{section}__populated"] == "yes")
        missing = total - populated
        raw_candidates = sum(1 for row in rows if row[f"{section}__raw_candidate"] == "yes")
        alias_candidates = sum(1 for row in rows if row[f"{section}__raw_alias_candidate"] == "yes")
        unmapped_only_candidates = sum(
            1
            for row in rows
            if row[f"{section}__raw_candidate"] == "yes"
            and row[f"{section}__raw_alias_candidate"] == "no"
            and row[f"{section}__raw_unmapped_candidate"] == "yes"
        )
        section_rows.append(
            {
                "section": section,
                "populated_count": populated,
                "missing_count": missing,
                "raw_candidate_count_when_missing": raw_candidates,
                "alias_candidate_count_when_missing": alias_candidates,
                "unmapped_only_candidate_count_when_missing": unmapped_only_candidates,
                "population_rate": round(populated / total, 4) if total else 0,
            }
        )
        lines.append(
            f"- `{section}`: populated {populated}/{total}, missing {missing}, "
            f"missing-with-raw-candidate {raw_candidates}, "
            f"alias-backed {alias_candidates}, unmapped-only {unmapped_only_candidates}"
        )

    lines.append("")
    lines.append("## Highest Priority Files")
    lines.append("")

    priority_rows = sorted(
        rows,
        key=lambda row: (
            -int(row["missing_sections_with_alias_raw_candidates"]),
            -int(row["missing_sections_with_raw_candidates"]),
            -int(row["missing_master_section_count"]),
            -int(row["raw_unmapped_block_count"]),
            row["relative_path"],
        ),
    )[:25]

    for row in priority_rows:
        lines.append(
            f"- `{row['relative_path']}`: missing {row['missing_master_section_count']} master sections; "
            f"{row['missing_sections_with_raw_candidates']} of those have raw candidates "
            f"({row['missing_sections_with_alias_raw_candidates']} alias-backed); "
            f"{row['raw_unmapped_block_count']} unmapped raw blocks"
        )

    lines.append("")
    lines.append("## Backfill Notes")
    lines.append("")
    lines.append("- The `*_raw_candidate` columns only turn `yes` when the master section is empty and relevant raw text exists.")
    lines.append("- `*_raw_alias_candidate` is the high-confidence signal: the parser already isolated a raw block into a matching section alias.")
    lines.append("- `*_raw_unmapped_candidate` is a weaker signal from keyword matches in `raw_sections.unmapped_blocks`.")
    lines.append("- For `conditions` and `permit_conditions`, the same raw alias can support both the narrative section and structured item extraction.")
    lines.append("- Review the per-file CSV first, then sort by `missing_sections_with_raw_candidates` to prioritize manual or scripted backfill work.")
    lines.append("")

    return section_rows, "\n".join(lines)


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    paths = sorted(INPUT_DIR.rglob("*.json"))
    rows = [build_row(path) for path in paths]

    detail_path = OUTPUT_DIR / "permit_evaluation_json_section_audit.csv"
    summary_csv_path = OUTPUT_DIR / "permit_evaluation_json_section_summary.csv"
    summary_md_path = OUTPUT_DIR / "permit_evaluation_json_audit_summary.md"

    write_csv(detail_path, rows)
    summary_rows, summary_md = build_summary(rows)
    write_csv(summary_csv_path, summary_rows)
    summary_md_path.write_text(summary_md, encoding="utf-8")

    print(f"Wrote {detail_path}")
    print(f"Wrote {summary_csv_path}")
    print(f"Wrote {summary_md_path}")


if __name__ == "__main__":
    main()
