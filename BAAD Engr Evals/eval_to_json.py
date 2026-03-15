# #!/usr/bin/env python3
"""
Parse “Engineering Evaluation” PDFs into JSON (schema v1.1-barr-custom).

What it does (heuristics, editable at top):
- Segments the PDF where it sees “ENGINEERING EVALUATION” (or “EVALUATION REPORT”).
- Extracts verbatim BACKGROUND text.
- Detects equipment lines like “S-802 …” or “A-14 …” into id/description pairs.
- Builds EMISSIONS:
  • “common_fugitives” from the EMISSIONS text (counts & permitted totals when present)
  • “by_equipment” with short narratives for each ID mentioned
- Toxics: sets status “below_trigger” vs “above_trigger” from language like “not required / below trigger” vs “HRA required / exceeds…”.
- PERMIT CONDITIONS: parses numbered items and Basis: lines.
- OFFSETS: looks for a ratio (e.g., 1.15:1) and pollutant increases (POC, NOx, etc.), else leaves fields empty.
- PSD, CEQA, Statement of Compliance, Title V: captured as full text blocks (SoC into a General subsection if no subtypes found).

You can safely run it on the large Tesoro PDF; use --app 29401 to target that specific evaluation.
"""

import re, json, sys, os, argparse
from typing import List, Dict, Tuple, Optional
from collections import Counter

# ---- Adjustable section aliases (tweak to match your documents) ----
SECTION_ALIASES = {
    "BACKGROUND": ["BACKGROUND"],
    "EMISSIONS": ["EMISSIONS", "EMISSION CALCULATIONS", "EMISSION", "EMISSIONS CALCULATIONS"],
    "TOXICS": ["TOXIC RISK SCREEN", "TOXIC RISK SCREENING", "TOXIC RISK SCREENING ANALYSIS", "TOXICS"],
    "OFFSETS": ["OFFSETS", "OFFSET"],
    "PSD": ["PSD APPLICABILITY", "PSD APPLICABILITY ANALYSIS", "PSD", "PREVENTION OF SIGNIFICANT DETERIORATION"],
    "CEQA": ["CEQA"],
    "SOC": ["STATEMENT OF COMPLIANCE", "STATEMENT OF COMPLIANCE / APPLICABILITY", "COMPLIANCE"],
    "PERMIT_CONDITIONS": ["PERMIT CONDITIONS", "CONDITIONS"],
    "TITLEV": ["TITLE V PERMIT", "TITLE V", "TITLE V PERMIT MODIFICATIONS", "TITLE V MODIFICATION", "TITLE V CHANGES"],
    "RECOMMENDATION": ["RECOMMENDATION", "RECOMMENDATIONS"]
}

ALLCAPS_HEAD = re.compile(r'^\s*([A-Z][A-Z0-9&/().,\-\s]{2,})\s*$', re.MULTILINE)

TOP_LINES_FOR_START_DETECTION = 120
MIN_START_GAP_PAGES = 2

# ---- PDF extraction ----
try:
    from PyPDF2 import PdfReader
except Exception as e:
    PdfReader = None

def extract_pages(pdf_path: str) -> List[str]:
    if PdfReader is None:
        raise RuntimeError("PyPDF2 is not installed. Install with: pip install PyPDF2")
    reader = PdfReader(pdf_path)
    out = []
    for p in reader.pages:
        try:
            t = p.extract_text() or ""
        except Exception:
            t = ""
        t = t.replace("\r\n", "\n").replace("\r", "\n")
        out.append(t)
    return out

def top_chunk(text: str, top_lines: int) -> str:
    lines = text.splitlines()
    return "\n".join(lines[:top_lines])

def find_evaluation_ranges(pages: List[str]) -> List[Tuple[int,int]]:
    if not pages:
        return []

    # Primary signal: "BACKGROUND" heading (usually near the start of an evaluation)
    bg_pages: List[int] = []
    for i, t in enumerate(pages):
        top = top_chunk(t, TOP_LINES_FOR_START_DETECTION)
        if re.search(r'^\s*BACKGROUND\s*$', top, re.IGNORECASE | re.MULTILINE):
            bg_pages.append(i)

    starts: List[int] = []
    if bg_pages:
        for i in bg_pages:
            start = i
            if i > 0:
                prev_top = top_chunk(pages[i - 1], TOP_LINES_FOR_START_DETECTION)
                if re.search(r'\bENGINEERING EVALUATION\b', prev_top, re.IGNORECASE) or re.search(r'\bEVALUATION REPORT\b', prev_top, re.IGNORECASE):
                    start = i - 1
            starts.append(start)
    else:
        for i, t in enumerate(pages):
            top = top_chunk(t, TOP_LINES_FOR_START_DETECTION)
            if re.search(r'\bENGINEERING EVALUATION\b', top, re.IGNORECASE):
                starts.append(i)
            elif re.search(r'\bEVALUATION REPORT\b', top, re.IGNORECASE):
                starts.append(i)

    starts = sorted(set(starts))
    if not starts:
        return [(0, len(pages) - 1)]

    filtered: List[int] = []
    for s in starts:
        if not filtered or (s - filtered[-1]) >= MIN_START_GAP_PAGES:
            filtered.append(s)
    starts = filtered

    # If the start detector fired excessively (e.g., repeating headers), collapse to single-eval.
    if len(starts) > 1 and len(starts) >= max(3, int(len(pages) * 0.4)):
        return [(0, len(pages) - 1)]

    ranges = []
    for idx, s in enumerate(starts):
        e = (starts[idx + 1] if idx + 1 < len(starts) else len(pages)) - 1
        ranges.append((s, e))
    return ranges

PAGE_OF_PAT = re.compile(r"\bPage\s+\d+\s+of\s+\d+\b", re.I)
PLANT_PAT = re.compile(r"\bPlant\s*#\s*\d+\b", re.I)
APP_LINE_STRICT = re.compile(
    r"^\s*Application\s*(?:No\.|Number|#)?\s*[:\-]?\s*(\d{1,6})\b.*$",
    re.I | re.M,
)
APP_INLINE = re.compile(
    r"\bApplication\s*(?:No\.|Number|#)?\s*[:\-]?\s*(\d{1,6})\b",
    re.I,
)
APP_INLINE_COMPACT = re.compile(
    r"Application(?:No\.|Number|#)?[:\-]?(\d{1,6})\b",
    re.I,
)

def mode_then_max(nums: List[str]) -> Optional[str]:
    if not nums:
        return None
    c = Counter(nums)
    most = c.most_common()
    top_count = most[0][1]
    candidates = [n for n, cnt in most if cnt == top_count]
    if len(candidates) == 1:
        return candidates[0]
    try:
        return sorted(candidates, key=lambda x: int(x))[-1]
    except Exception:
        return candidates[-1]

def detect_app_number(txt: str) -> Optional[str]:
    """Best-effort app number detection (prefers 5-6 digit app numbers)."""
    lines = txt.splitlines()
    candidates: List[str] = []

    for line in lines[:TOP_LINES_FOR_START_DETECTION]:
        if PAGE_OF_PAT.search(line) or PLANT_PAT.search(line):
            continue
        m = APP_LINE_STRICT.match(line)
        if m:
            candidates.append(m.group(1))
            continue
        compact = re.sub(r"\s+", "", line)
        m2 = APP_INLINE_COMPACT.search(compact)
        if m2:
            candidates.append(m2.group(1))

    if candidates:
        return mode_then_max(candidates)

    candidates.extend(APP_INLINE.findall(txt))
    if candidates:
        return mode_then_max(candidates)
    return None


# ---- Section splitting ----
def alias_of(h: str) -> str:
    up = h.strip().upper()
    for key, arr in SECTION_ALIASES.items():
        for a in arr:
            if up.startswith(a):
                return key
    return ""

def find_headings_map(txt: str) -> list[tuple[str,int]]:
    found = []
    for m in ALLCAPS_HEAD.finditer(txt):
        h = m.group(1).strip()
        if len(h) < 4:
            continue
        found.append((h, m.start()))
    # Deduplicate accidental repeats
    dedup = []
    last = None
    for h, i in found:
        if last and last[0] == h and i - last[1] < 10:
            continue
        dedup.append((h, i))
        last = (h, i)
    return dedup

def split_sections(txt: str) -> Dict[str, str]:
    heads = find_headings_map(txt)
    sections: Dict[str, str] = {}
    if not heads:
        return sections
    for idx, (h, pos) in enumerate(heads):
        end = heads[idx+1][1] if idx+1 < len(heads) else len(txt)
        key = alias_of(h)
        if key:
            body = txt[pos + len(h):end].strip()
            sections.setdefault(key, "")
            sections[key] += (h + "\n" + body).strip()
    return sections

def split_sections_with_blocks(txt: str) -> Dict[str, object]:
    """
    Preserve *all* all-caps heading blocks (including unmapped ones) so content
    doesn't silently disappear from the JSON.
    """
    heads = find_headings_map(txt)
    if not heads:
        return {"preamble": txt.strip(), "blocks": [], "sections": {}, "unmapped_blocks": []}

    blocks: List[Dict[str, object]] = []
    sections: Dict[str, str] = {}
    for idx, (h, pos) in enumerate(heads):
        end = heads[idx + 1][1] if idx + 1 < len(heads) else len(txt)
        key = alias_of(h)
        body = txt[pos + len(h):end].strip()
        block_text = (h + "\n" + body).strip()
        blocks.append({"heading": h, "alias": key or None, "text": block_text})
        if key:
            sections.setdefault(key, "")
            sections[key] += block_text

    preamble = txt[:heads[0][1]].strip()
    unmapped = [b for b in blocks if not b.get("alias")]
    return {"preamble": preamble, "blocks": blocks, "sections": sections, "unmapped_blocks": unmapped}

def extract_table_like_blocks(text: str) -> List[str]:
    """
    Extract contiguous line blocks that *look* like tables (multi-column lines).
    This does not fully reconstruct tables, but preserves content that is often
    lost when converting PDFs to structured fields.
    """
    lines = text.splitlines()
    blocks: List[str] = []
    buf: List[str] = []

    def is_table_line(line: str) -> bool:
        if "|" in line:
            return True
        if re.search(r"\S\s{2,}\S", line):
            return True
        if re.search(r"[-_]{4,}", line):
            return True
        return False

    for line in lines:
        if is_table_line(line):
            buf.append(line.rstrip())
        else:
            if len(buf) >= 3:
                blocks.append("\n".join(buf).strip())
            buf = []
    if len(buf) >= 3:
        blocks.append("\n".join(buf).strip())
    return blocks

# ---- Field parsers ----
def parse_equipment(bg_text: str) -> list[dict]:
    eq = []
    for line in bg_text.splitlines():
        m = re.match(r'\s*([SA]-\d{1,5})\s+(.+)$', line.strip())
        if m:
            eq.append({"id": m.group(1), "description": m.group(2).strip()})
    # de-dupe
    seen = set(); out = []
    for e in eq:
        if e["id"] not in seen:
            out.append(e); seen.add(e["id"])
    return out

def toxics_status(text: str) -> tuple[str, str]:
    if not text:
        return ("below_trigger", "")
    t = text.lower()
    status = "below_trigger"
    if "above trigger" in t or "exceeds" in t or "health risk assessment is required" in t or "hra is required" in t:
        status = "above_trigger"
    if "not required" in t or "below trigger" in t or "does not exceed" in t:
        status = "below_trigger"
    return (status, text.strip())

def parse_offsets(text: str) -> Dict:
    if not text:
        return {"narrative": "", "table": {"columns": ["Pollutant", "Project Increase (tpy)", "Offset Ratio", "Required Offsets (tpy)"], "rows": []}}
    ratio = None
    m = re.search(r'(\d+(?:\.\d+)?)\s*:\s*(\d+(?:\.\d+)?)', text)
    if m:
        ratio = f"{m.group(1)} : {m.group(2)}"
    rows = []
    for pol in ["POC","NOx","NO2","SO2","PM10","PM2.5","CO","NH3","VOC"]:
        mm = re.search(pol + r'.{0,60}?(\d+(?:\.\d+)?)\s*(?:tpy|tons per year)?', text, re.IGNORECASE|re.DOTALL)
        if mm:
            try:
                inc = float(mm.group(1))
            except Exception:
                inc = None
            rows.append([pol, inc, ratio or "N/A", None])
    if not rows and ratio:
        rows = [["POC", None, ratio, None]]
    return {"narrative": text.strip(), "table": {"columns": ["Pollutant", "Project Increase (tpy)", "Offset Ratio", "Required Offsets (tpy)"], "rows": rows}}

def parse_permit_conditions(text: str) -> Dict:
    items = []
    cond_no = None
    m = re.search(r'Condition\s*(No\.|Number)?\s*[:\-]?\s*(\d+)', text, re.IGNORECASE)
    if m:
        try:
            cond_no = int(m.group(2))
        except Exception:
            cond_no = None
    for m in re.finditer(r'^\s*(\d+)\.\s*(.*?)(?=\n\s*\d+\.|\Z)', text, re.DOTALL|re.MULTILINE):
        num = int(m.group(1))
        body = m.group(2).strip()
        basis = []
        bm = re.search(r'Basis\s*:\s*(.*)$', body, re.IGNORECASE|re.DOTALL)
        if bm:
            basis_txt = bm.group(1).strip()
            basis = [b.strip() for b in re.split(r'[;,]\s*', basis_txt) if b.strip()]
            body = re.sub(r'Basis\s*:\s*.*$', '', body, flags=re.IGNORECASE|re.DOTALL).strip()
        items.append({"num": num, "text": body, "basis": basis})
    return {"condition_number": cond_no, "items": items}

def parse_common_fugitives(text: str) -> Dict:
    if not text:
        return {}
    rows = []
    comp_map = {
        "Valves":"Valves",
        "Pumps":"Pumps",
        "Pressure Relief Valves":"Pressure Relief Valves (PRVs)",
        "PRVs":"Pressure Relief Valves (PRVs)",
        "Connectors":"Connectors/Flanges",
        "Flanges":"Connectors/Flanges"
    }
    for key, display in comp_map.items():
        m = re.search(rf'({key}).{{0,20}}?(\d+)', text, re.IGNORECASE)
        if m:
            rows.append([display, "Light liquid", int(m.group(2))])
    lb_day = None; tpy = None
    md = re.search(r'(\d+(?:\.\d+)?)\s*lb/day', text, re.IGNORECASE)
    mt = re.search(r'(\d+(?:\.\d+)?)\s*(tpy|tons/year)', text, re.IGNORECASE)
    if md:
        try: lb_day = float(md.group(1))
        except Exception: lb_day = None
    if mt:
        try: tpy = float(mt.group(1))
        except Exception: tpy = None
    return {
        "narrative": text.strip(),
        "predicted_component_counts_table": {"columns": ["Component Type", "Service", "Predicted Count"], "rows": rows},
        "permitted_fugitive_totals": {"units": {"lb_per_day":"lb/day","tpy":"tons/year"}, "POC": {"lb_per_day": lb_day, "tpy": tpy}}
    }

def build_emissions_sections(equip_ids: List[str], emissions_text: str) -> Dict:
    by_eq = {}
    for eid in equip_ids:
        hits = []
        for m in re.finditer(rf'([^\n]*\b{re.escape(eid)}\b[^\n]*)', emissions_text):
            start = emissions_text.rfind('\n', 0, m.start())
            end = emissions_text.find('\n', m.end())
            snippet = emissions_text[start+1:end if end!=-1 else len(emissions_text)]
            hits.append(snippet.strip())
        narrative = "\n".join(sorted(set(hits))) if hits else ""
        by_eq[eid] = {
            "narrative": narrative or "No equipment-specific narrative found in EMISSIONS section.",
            "tables": [],
            "cumulative_increase_table": {
                "note": "Parsed heuristically; edit as needed.",
                "columns": ["Pollutant", "lb/hr", "lb/day", "lb/yr", "tpy"],
                "rows": [["POC", None, None, None, None]]
            }
        }
    return by_eq

def titlev_from_text(text: str) -> Dict:
    if not text:
        return {"narrative": "", "revisions": [], "affected_sources": []}
    revisions = []
    for line in text.splitlines():
        if re.match(r'^\s*[-•*]\s+', line) or re.match(r'^\s*\(?[a-z0-9]\)\s+', line.strip(), re.IGNORECASE):
            revisions.append(line.strip(" -*•"))
    aff = sorted(set(re.findall(r'\b[SA]-\d{1,5}\b', text)))
    return {"narrative": text.strip(), "revisions": revisions, "affected_sources": aff}

# ---- JSON assembly ----
def to_json_for_section(txt: str, app_filter: str|None=None) -> Dict:
    app_no = detect_app_number(txt) or (app_filter if app_filter else None)

    # crude plant name scrape (refinery/company line)
    plant_name = ""
    m = re.search(r'([^\n]{10,120}Refinery[^\n]{0,120})', txt)
    if m: plant_name = m.group(1).strip()
    if not plant_name:
        m = re.search(r'([^\n]{10,120}Company[^\n]{0,120})', txt)
        plant_name = m.group(1).strip() if m else ""

    split = split_sections_with_blocks(txt)
    secs = split["sections"]

    # Background verbatim
    bg_text = ""
    for a in SECTION_ALIASES["BACKGROUND"]:
        if a in secs: bg_text = secs[a]; break
    if not bg_text:
        # fallback to a large paragraph beginning with “The …”
        m = re.search(r'(?s)(The .+?)(?:\n[A-Z][A-Z0-9&/().,\-\s]{2,}\n)', txt)
        if m: bg_text = m.group(1).strip()
    if not bg_text and split.get("preamble"):
        bg_text = str(split["preamble"]).strip()

    equip = parse_equipment(bg_text)

    em_text = ""
    for a in SECTION_ALIASES["EMISSIONS"]:
        if a in secs: em_text = secs[a]; break

    common_fug = parse_common_fugitives(em_text) if em_text else {
        "narrative": "",
        "predicted_component_counts_table": {"columns": ["Component Type","Service","Predicted Count"], "rows": []},
        "permitted_fugitive_totals": {"units": {"lb_per_day":"lb/day","tpy":"tons/year"}, "POC": {"lb_per_day": None, "tpy": None}}
    }
    by_eq = build_emissions_sections([e["id"] for e in equip], em_text) if equip else {}

    tox_text = ""
    for a in SECTION_ALIASES["TOXICS"]:
        if a in secs: tox_text = secs[a]; break
    tox_status_val, tox_narr = toxics_status(tox_text)

    off_text = ""
    for a in SECTION_ALIASES["OFFSETS"]:
        if a in secs: off_text = secs[a]; break
    offsets = parse_offsets(off_text)

    psd_text = ""
    for a in SECTION_ALIASES["PSD"]:
        if a in secs: psd_text = secs[a]; break
    ceqa_text = ""
    for a in SECTION_ALIASES["CEQA"]:
        if a in secs: ceqa_text = secs[a]; break
    soc_text = ""
    for a in SECTION_ALIASES["SOC"]:
        if a in secs: soc_text = secs[a]; break
    permt_text = ""
    for a in SECTION_ALIASES["PERMIT_CONDITIONS"]:
        if a in secs: permt_text = secs[a]; break
    titlev_text = ""
    for a in SECTION_ALIASES["TITLEV"]:
        if a in secs: titlev_text = secs[a]; break

    return {
        "schema_version": "v1.1-barr-custom",
        "source": {
            "pdf": None,
            "evaluation_page_range": None,
            "text_extraction": {
                "engine": "PyPDF2",
                "table_like_blocks": extract_table_like_blocks(txt),
            },
        },
        "application_number": app_no,
        "plant": {"name": plant_name or "", "plant_id": None},
        "evaluation_date": None,
        "permit_date": None,
        "project_title": None,
        "equipment": equip,
        "background": {"text": bg_text.strip() if bg_text else ""},
        "emissions": {
            "common_fugitives": common_fug,
            "by_equipment": by_eq
        },
        "toxic_risk_screening_analysis": {"status": tox_status_val, "narrative": tox_narr},
        "offsets": offsets,
        "PSD_applicability": {"narrative": psd_text.strip() if psd_text else ""},
        "CEQA": {"narrative": ceqa_text.strip() if ceqa_text else ""},
        "Statement_of_Compliance": {"General": {"findings": [soc_text.strip()] if soc_text else []}},
        "permit_conditions": parse_permit_conditions(permt_text) if permt_text else {"condition_number": None, "items": []},
        "TitleV_permit": titlev_from_text(titlev_text),
        "raw_sections": {
            "preamble": split["preamble"],
            "blocks": split["blocks"],
            "unmapped_blocks": split["unmapped_blocks"],
        },
    }

def _safe_stem(p: str) -> str:
    stem = os.path.splitext(os.path.basename(p))[0]
    stem = re.sub(r"[^A-Za-z0-9._-]+", "_", stem).strip("_")
    return stem or "pdf"

def _unique_path(path: str) -> str:
    if not os.path.exists(path):
        return path
    base, ext = os.path.splitext(path)
    for i in range(1, 10000):
        candidate = f"{base}-{i}{ext}"
        if not os.path.exists(candidate):
            return candidate
    raise RuntimeError(f"Could not find unique filename for: {path}")

def build_from_pdf(
    pdf_path: str,
    outdir: str,
    app_filter: str|None=None,
    include_raw_pages: bool=False,
    single_eval: bool=False,
) -> list[str]:
    pages = extract_pages(pdf_path)
    evals = [(0, len(pages) - 1)] if (single_eval and pages) else find_evaluation_ranges(pages)
    saved = []
    source_stem = _safe_stem(pdf_path)
    m_hint = re.search(r"\bapplication_(\d{5,6})\b", os.path.basename(pdf_path), re.IGNORECASE)
    app_hint = m_hint.group(1) if m_hint else None
    for idx, (s, e) in enumerate(evals, start=1):
        txt = "\n".join(pages[s:e+1])
        app_no = detect_app_number(txt)
        if app_filter and app_no != app_filter:
            continue
        data = to_json_for_section(txt, app_filter=app_filter)
        data["source"]["pdf"] = os.path.abspath(pdf_path)
        data["source"]["evaluation_page_range"] = {"start_page": s, "end_page": e}
        data["source"]["application_number_detected"] = data.get("application_number")
        data["source"]["application_number_from_filename"] = app_hint
        if app_hint and (not data.get("application_number") or data.get("application_number") != app_hint):
            data["application_number"] = app_hint
        if include_raw_pages:
            data["source"]["pages"] = pages[s:e+1]

        app_part = data["application_number"] or "unknown"
        name = f"{source_stem}__application_{app_part}__eval_{idx:02d}.json"
        op = _unique_path(os.path.join(outdir, name))
        os.makedirs(outdir, exist_ok=True)
        with open(op, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        saved.append(op)
    return saved

def main():
    ap = argparse.ArgumentParser(description="Parse an Engineering Evaluation PDF into v1.1-barr-custom JSON.")
    ap.add_argument("pdf", help="Path to PDF")
    ap.add_argument("--outdir", default="out_json", help="Output folder")
    ap.add_argument("--app", help="Optional application number to extract (e.g., 29401)")
    ap.add_argument("--single-eval", action="store_true", help="Treat input PDF as a single evaluation (no segmentation).")
    ap.add_argument("--include-raw-pages", action="store_true", help="Include extracted page text in output JSON.")
    args = ap.parse_args()
    paths = build_from_pdf(
        args.pdf,
        args.outdir,
        app_filter=args.app,
        include_raw_pages=args.include_raw_pages,
        single_eval=args.single_eval,
    )
    if not paths:
        print("No evaluations saved (check --app or PDF content).", file=sys.stderr)
    else:
        print("\n".join(paths))

if __name__ == "__main__":
    main()
