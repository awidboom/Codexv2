from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

import fitz
from PyPDF2 import PdfReader

import permit_compare


ROOT = Path(__file__).resolve().parent
DATA_JS = ROOT / "permit_review_data.js"
ASSET_DIR = ROOT / "review_assets"
APPLICATION_DIR = ROOT / "Permit applications"

REQ_PATTERN = re.compile(r"^(\d+\.\d+\.\d+)\s+")
SPLIT_REQ_PATTERN = re.compile(r"^((?:\d+\.){2}\d)\s+(\d)\s+(.*)$")
IGNORE_PREFIXES = (
    "Permit Issued:",
    "Permit issued:",
    "Permit Expires:",
    "Permit expires:",
    "Requirement number",
    "Requirement n umber",
    "Requirement and citation",
    "Requirem ent and c itation",
    "Page ",
)
REQ_ID_FINDER = re.compile(r"\b\d+\.\d+\.\d+\b")

MANUAL_PAGE_MAP = {
    "Cover Page / Permit Overview": 1,
    "1. Permit applications table": 3,
    "3. Facility description": 5,
}

SUBJECT_OPTIONS = [
    "Administrative",
    "Facility Description",
    "Equipment List",
    "Emission Units",
    "Insignificant Activities",
    "Fugitive Emissions",
    "Emission Limits",
    "Operational Limits",
    "Fuel Requirements",
    "Throughput or Production Limits",
    "Control Equipment",
    "Monitoring",
    "Recordkeeping",
    "Reporting",
    "Testing",
    "Inspections",
    "Deviations",
    "Compliance Certification",
    "Startup Shutdown Malfunction",
    "Malfunction or Breakdown",
    "Performance Testing",
    "CAM",
    "NSPS",
    "NESHAP or MACT",
    "State Rule Requirement",
    "Modeling",
    "Ambient Conditions",
    "Stack Parameters",
    "Temporary or Construction Conditions",
    "General Conditions",
    "Definitions",
    "Permit Shield",
    "Compliance Schedule",
    "Other",
]

CONCLUSION_OPTIONS = [
    "No change",
    "Minor changes, likely acceptable",
    "Significant changes",
]

RISK_OPTIONS = ["Low", "Medium", "High"]
CHANGE_TYPE_OPTIONS = [
    "No change",
    "Addition",
    "Deletion",
    "Revision",
    "Possible relocation or renumbering",
]

PDF_INFO = {
    "old": {"path": permit_compare.OLD_PDF, "slug": "old"},
    "new": {"path": permit_compare.NEW_PDF, "slug": "new"},
}

CURRENT_MAJOR_APP = "Major Amendment DDGS BH Maintenance_2025.11.10.pdf"

APPLICATION_EXCERPTS = {
    "stru11_redline": {
        "applicationFile": CURRENT_MAJOR_APP,
        "page": 125,
        "mode": "redline",
        "evidenceType": "Attachment A redline",
    },
    "trea2_redline": {
        "applicationFile": CURRENT_MAJOR_APP,
        "page": 156,
        "mode": "redline",
        "evidenceType": "Attachment A redline",
    },
    "summary_request": {
        "applicationFile": CURRENT_MAJOR_APP,
        "page": 4,
        "mode": "support",
        "evidenceType": "Narrative application support",
        "text": (
            "Valero is requesting a change to permit conditions 5.46.1 and 5.57.1 to allow up to 100 hours "
            "per year when TREA 2 is down for maintenance and emissions from EQUI 243, 18, and 191 are routed to EQUI 218."
        ),
        "searchPhrases": [
            "permit conditions 5.46.1 and 5.57.1",
            "up to 100 hours per year",
            "routed to EQUI 218",
        ],
    },
}

APPLICATION_ROW_MAP = {
    "PC-001": "summary_request",
    "PC-002": "summary_request",
    "PC-003": "summary_request",
    "PC-011": "stru11_redline",
    "PC-012": "stru11_redline",
    "PC-014": "stru11_redline",
    "PC-017": "trea2_redline",
}


def normalize_line(raw: str) -> str:
    line = re.sub(r"\s+", " ", raw.replace("\r", " ")).strip()
    split_match = SPLIT_REQ_PATTERN.match(line)
    if split_match:
        line = f"{split_match.group(1)}{split_match.group(2)} {split_match.group(3)}"
    return line


def extract_requirement_pages(pdf_path: Path) -> dict[str, int]:
    reader = PdfReader(str(pdf_path))
    req_pages: dict[str, int] = {}
    current_req: str | None = None

    for page_no, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        for raw in text.split("\n"):
            line = normalize_line(raw)
            if not line or any(line.startswith(prefix) for prefix in IGNORE_PREFIXES):
                continue
            match = REQ_PATTERN.match(line)
            if match:
                current_req = match.group(1)
                req_pages.setdefault(current_req, page_no)
    return req_pages


def first_req_id(section_label: str) -> str | None:
    if section_label in MANUAL_PAGE_MAP or section_label == "No direct equivalent":
        return None
    match = REQ_ID_FINDER.search(section_label)
    return match.group(0) if match else None


def page_for_section(section_label: str, page_map: dict[str, int]) -> int | None:
    if section_label in MANUAL_PAGE_MAP:
        return MANUAL_PAGE_MAP[section_label]
    req_id = first_req_id(section_label)
    if not req_id:
        return None
    return page_map.get(req_id)


def core_change(row) -> str:
    sentences = re.split(r"(?<=[.!?])\s+", row.initial_analysis.strip())
    return " ".join(sentences[:2]).strip()


def req_ids_from_text(text: str) -> list[str]:
    seen: list[str] = []
    for req_id in REQ_ID_FINDER.findall(text or ""):
        if req_id not in seen:
            seen.append(req_id)
    return seen


def render_page_asset(pdf_path: Path, page_number: int, output_path: Path) -> tuple[float, float]:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(pdf_path)
    page = doc.load_page(page_number - 1)
    matrix = fitz.Matrix(2.15, 2.15)
    pix = page.get_pixmap(matrix=matrix, alpha=False)
    pix.save(output_path)
    width = page.rect.width
    height = page.rect.height
    doc.close()
    return width, height


def search_phrase_rects(pdf_path: Path, page_number: int, phrases: list[str]) -> list[dict[str, float | str]]:
    if not pdf_path.exists() or not page_number or not phrases:
        return []
    doc = fitz.open(pdf_path)
    page = doc.load_page(page_number - 1)
    page_rect = page.rect
    highlights: list[dict[str, float | str]] = []
    seen_keys: set[tuple[int, int, int, int]] = set()
    for phrase in phrases:
        hits = page.search_for(phrase)
        if not hits:
            words = phrase.split()
            for size in (8, 6, 4):
                if len(words) >= size:
                    probe = " ".join(words[:size])
                    hits = page.search_for(probe)
                    if hits:
                        break
        for rect in hits[:3]:
            key = (round(rect.x0), round(rect.y0), round(rect.x1), round(rect.y1))
            if key in seen_keys:
                continue
            seen_keys.add(key)
            highlights.append(
                {
                    "reqId": phrase[:48],
                    "x": rect.x0 / page_rect.width,
                    "y": rect.y0 / page_rect.height,
                    "w": rect.width / page_rect.width,
                    "h": rect.height / page_rect.height,
                }
            )
    doc.close()
    return highlights


def redline_span_payload(pdf_path: Path, page_number: int) -> tuple[str, list[dict[str, float | str]]]:
    if not pdf_path.exists() or not page_number:
        return "", []
    doc = fitz.open(pdf_path)
    page = doc.load_page(page_number - 1)
    page_rect = page.rect
    text_parts: list[str] = []
    highlights: list[dict[str, float | str]] = []
    for block in page.get_text("dict").get("blocks", []):
        if block.get("type") != 0:
            continue
        for line in block.get("lines", []):
            line_text_parts: list[str] = []
            line_rects: list[tuple[float, float, float, float]] = []
            for span in line.get("spans", []):
                if span.get("color", 0) == 0:
                    continue
                text = span.get("text", "").strip()
                if not text:
                    continue
                line_text_parts.append(text)
                line_rects.append((span["bbox"][0], span["bbox"][1], span["bbox"][2], span["bbox"][3]))
            if line_text_parts and line_rects:
                text_parts.append(" ".join(line_text_parts))
                x0 = min(r[0] for r in line_rects)
                y0 = min(r[1] for r in line_rects)
                x1 = max(r[2] for r in line_rects)
                y1 = max(r[3] for r in line_rects)
                highlights.append(
                    {
                        "reqId": "Requested redline",
                        "x": x0 / page_rect.width,
                        "y": y0 / page_rect.height,
                        "w": (x1 - x0) / page_rect.width,
                        "h": (y1 - y0) / page_rect.height,
                    }
                )
    doc.close()
    return " ".join(text_parts).strip(), highlights


def normalized_rects(pdf_path: Path, page_number: int, req_ids: list[str]) -> list[dict[str, float | str]]:
    if not req_ids:
        return []
    doc = fitz.open(pdf_path)
    page = doc.load_page(page_number - 1)
    page_rect = page.rect
    highlights: list[dict[str, float | str]] = []
    for req_id in req_ids:
        hits = page.search_for(req_id)
        if not hits:
            continue
        rect = hits[0]
        highlights.append(
            {
                "reqId": req_id,
                "x": rect.x0 / page_rect.width,
                "y": rect.y0 / page_rect.height,
                "w": rect.width / page_rect.width,
                "h": rect.height / page_rect.height,
            }
        )
    doc.close()
    return highlights


def build_page_assets(rows: list[dict]) -> dict[tuple[str, int], dict]:
    assets: dict[tuple[str, int], dict] = {}
    page_refs = set()
    for row in rows:
        if row["oldPage"]:
            page_refs.add(("old", row["oldPage"]))
        if row["newPage"]:
            page_refs.add(("new", row["newPage"]))
        if row.get("applicationFile") and row.get("applicationPage") and row.get("applicationMode") == "redline":
            page_refs.add((row["applicationFile"], row["applicationPage"]))

    for side, page_number in sorted(page_refs):
        if side in PDF_INFO:
            slug = PDF_INFO[side]["slug"]
            pdf_path = PDF_INFO[side]["path"]
        else:
            slug = re.sub(r"[^a-z0-9]+", "_", Path(side).stem.lower()).strip("_")
            pdf_path = APPLICATION_DIR / side
        output_path = ASSET_DIR / slug / f"page_{page_number:03d}.png"
        width, height = render_page_asset(pdf_path, page_number, output_path)
        assets[(side, page_number)] = {
            "asset": output_path.relative_to(ROOT).as_posix(),
            "width": width,
            "height": height,
        }
    return assets


def build_payload() -> dict:
    old_pages = extract_requirement_pages(permit_compare.OLD_PDF)
    new_pages = extract_requirement_pages(permit_compare.NEW_PDF)
    applications = []
    for name, relevance, summary, note in permit_compare.APPLICATION_FILES:
        applications.append(
            {
                "file": name,
                "path": (Path("Permit applications") / name).as_posix(),
                "amendmentType": "Major Amendment" if "major amendment" in name.lower() else "Minor Amendment",
                "relevance": relevance,
                "summary": summary,
                "note": note,
            }
        )
    rows = []
    for row in permit_compare.build_rows():
        old_text = row.old_text_getter()
        new_text = row.new_text_getter()
        old_page = page_for_section(row.old_section, old_pages)
        new_page = page_for_section(row.new_section, new_pages)
        request_status, application_source, application_basis, review_priority = permit_compare.request_meta(row.comparison_id)
        validation_basis, evidence_confidence = permit_compare.summarize_validation(row)
        app_ref = APPLICATION_EXCERPTS.get(APPLICATION_ROW_MAP.get(row.comparison_id, ""))
        rows.append(
            {
                "id": row.comparison_id,
                "oldSection": row.old_section,
                "newSection": row.new_section,
                "subjectPrimary": row.subject_primary,
                "subjectSecondary": row.subject_secondary,
                "oldText": old_text,
                "newText": new_text,
                "changeType": row.change_type,
                "initialAnalysis": row.initial_analysis,
                "regulatoryImpact": row.regulatory_impact,
                "operationalImpact": row.operational_impact,
                "riskLevel": row.risk_level,
                "recommendedFollowUp": row.follow_up,
                "consultantConclusion": row.conclusion,
                "requestedChangeStatus": request_status,
                "applicationSource": application_source,
                "applicationBasis": application_basis,
                "reviewPriority": review_priority,
                "validationBasis": validation_basis,
                "evidenceConfidence": evidence_confidence,
                "applicationFile": app_ref["applicationFile"] if app_ref else None,
                "applicationText": app_ref.get("text", "") if app_ref else "",
                "applicationPage": app_ref["page"] if app_ref else None,
                "applicationSearchPhrases": app_ref.get("searchPhrases", []) if app_ref else [],
                "applicationMode": app_ref.get("mode", "search") if app_ref else None,
                "applicationEvidenceType": app_ref.get("evidenceType") if app_ref else None,
                "importanceRank": row.importance_rank,
                "coreChange": core_change(row),
                "oldPage": old_page,
                "newPage": new_page,
                "oldReqIds": req_ids_from_text(old_text),
                "newReqIds": req_ids_from_text(new_text),
            }
        )
    assets = build_page_assets(rows)
    for row in rows:
        old_asset = assets.get(("old", row["oldPage"])) if row["oldPage"] else None
        new_asset = assets.get(("new", row["newPage"])) if row["newPage"] else None
        row["oldAsset"] = old_asset["asset"] if old_asset else None
        row["newAsset"] = new_asset["asset"] if new_asset else None
        row["oldHighlightRects"] = normalized_rects(
            permit_compare.OLD_PDF, row["oldPage"], row["oldReqIds"]
        ) if row["oldPage"] else []
        row["newHighlightRects"] = normalized_rects(
            permit_compare.NEW_PDF, row["newPage"], row["newReqIds"]
        ) if row["newPage"] else []
        app_asset = assets.get((row["applicationFile"], row["applicationPage"])) if row.get("applicationFile") and row.get("applicationPage") else None
        row["applicationAsset"] = app_asset["asset"] if app_asset and row.get("applicationMode") == "redline" else None
        row["applicationPdf"] = (Path("Permit applications") / row["applicationFile"]).as_posix() if row.get("applicationFile") else None
        if row.get("applicationFile") and row.get("applicationPage"):
            app_pdf_path = APPLICATION_DIR / row["applicationFile"]
            if row.get("applicationMode") == "redline":
                redline_text, redline_rects = redline_span_payload(app_pdf_path, row["applicationPage"])
                if redline_text:
                    row["applicationText"] = redline_text
                row["applicationHighlightRects"] = redline_rects
            elif row.get("applicationMode") == "search":
                row["applicationHighlightRects"] = search_phrase_rects(
                    app_pdf_path,
                    row["applicationPage"],
                    row.get("applicationSearchPhrases", []),
                )
            else:
                row["applicationHighlightRects"] = []
        else:
            row["applicationHighlightRects"] = []
    return {
        "meta": {
            "title": "Permit Comparison QAQC Review",
            "oldPdf": permit_compare.OLD_PDF.name,
            "newPdf": permit_compare.NEW_PDF.name,
            "rowCount": len(rows),
            "workflowUseNote": permit_compare.WORKFLOW_USE_NOTE,
            "generatedAt": datetime.now().isoformat(timespec="seconds"),
        },
        "options": {
            "subjectTags": SUBJECT_OPTIONS,
            "conclusions": CONCLUSION_OPTIONS,
            "riskLevels": RISK_OPTIONS,
            "changeTypes": CHANGE_TYPE_OPTIONS,
            "requestedStatuses": [
                "Requested",
                "Related to requested change",
                "Not identified in application",
                "Legacy or structural only",
            ],
            "evidenceConfidences": sorted({row["evidenceConfidence"] for row in rows}),
        },
        "applications": applications,
        "qaSpotChecks": permit_compare.MANUAL_QA_FINDINGS,
        "rows": rows,
    }


def main() -> None:
    payload = build_payload()
    DATA_JS.write_text(
        "window.PERMIT_REVIEW_DATA = "
        + json.dumps(payload, indent=2)
        + ";\n",
        encoding="utf-8",
    )
    print(DATA_JS.resolve())


if __name__ == "__main__":
    main()
