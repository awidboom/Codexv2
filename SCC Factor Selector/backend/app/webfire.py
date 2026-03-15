from __future__ import annotations

from typing import Dict, Any
import html
import re

import httpx

from .settings import SETTINGS


def _build_url() -> str:
    base = SETTINGS.webfire_base_url.rstrip("/")
    lower = base.lower()
    if "efwebsrv5.cfc" in lower:
        return base
    if lower.endswith("getefdata"):
        return base
    return f"{base}/getEFData"


def fetch_webfire_data(params: Dict[str, Any]) -> Dict[str, Any]:
    url = _build_url()
    payload = dict(params)
    if "efwebsrv5.cfc" in url.lower() and "method" not in payload:
        payload["method"] = "getEFData"
    headers = {"User-Agent": "SCCFactorSelector/0.1"}
    with httpx.Client(timeout=30.0) as client:
        response = client.get(url, params=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        if isinstance(data, list):
            return {"hits": len(data), "results": data}
        if isinstance(data, dict):
            nested = data.get("results")
            if isinstance(nested, list) and len(nested) == 1 and isinstance(nested[0], dict):
                inner = nested[0]
                if "results" in inner:
                    return {
                        "hits": int(inner.get("hits", len(inner.get("results", [])))),
                        "results": inner.get("results", []),
                    }
        return data


def _build_detail_url(factor_id: int) -> str:
    base = SETTINGS.webfire_detail_url.rstrip("/")
    if "?" in base:
        return f"{base}&fid={factor_id}"
    return f"{base}?fid={factor_id}"


def _strip_html(value: str) -> str:
    if not value:
        return ""
    cleaned = re.sub(r"<br\s*/?>", " ", value, flags=re.IGNORECASE)
    cleaned = re.sub(r"<[^>]+>", "", cleaned)
    cleaned = html.unescape(cleaned)
    cleaned = " ".join(cleaned.split())
    return cleaned.strip()


def fetch_webfire_reference(factor_id: int) -> str:
    url = _build_detail_url(factor_id)
    headers = {"User-Agent": "SCCFactorSelector/0.1"}
    try:
        with httpx.Client(timeout=30.0) as client:
            response = client.get(url, headers=headers)
            response.raise_for_status()
            html_text = response.text
    except httpx.HTTPError:
        return ""

    pattern = re.compile(
        r"<tr[^>]*>\s*<td[^>]*>\s*References\s*</td>\s*<td[^>]*>(.*?)</td>",
        re.IGNORECASE | re.DOTALL,
    )
    match = pattern.search(html_text)
    if not match:
        return ""
    return _strip_html(match.group(1))


def _extract_row_value(payload: str, label: str) -> str:
    pattern = re.compile(
        rf"<tr[^>]*>\s*<td[^>]*>\s*(?:<[^>]+>\s*)*{re.escape(label)}\s*(?:<[^>]+>\s*)*</td>\s*<td[^>]*>(.*?)</td>",
        re.IGNORECASE | re.DOTALL,
    )
    match = pattern.search(payload)
    if not match:
        return ""
    return _strip_html(match.group(1))


def _extract_pollutant_row(payload: str) -> tuple[str, str, str]:
    pattern = re.compile(
        r"<tr[^>]*>\s*<td[^>]*>.*?POLLUTANT.*?</td>\s*<td[^>]*>(.*?)</td>\s*<td[^>]*>(.*?)</td>",
        re.IGNORECASE | re.DOTALL,
    )
    match = pattern.search(payload)
    if not match:
        return "", "", ""
    pollutant = _strip_html(match.group(1))
    tail = _strip_html(match.group(2))
    nei_match = re.search(r"\bNEI\s+([A-Za-z0-9-]+)", tail)
    cas_match = re.search(r"\bCAS\s+([0-9-]+)", tail)
    nei = nei_match.group(1) if nei_match else ""
    cas = cas_match.group(1) if cas_match else ""
    return pollutant, nei, cas


def _extract_control(payload: str) -> str:
    row_pattern = re.compile(
        r"<tr[^>]*>\s*<td[^>]*>(.*?)</td>\s*</tr>",
        re.IGNORECASE | re.DOTALL,
    )
    for match in row_pattern.finditer(payload):
        cell_html = match.group(1)
        if re.search(r"Control\(s\)", cell_html, re.IGNORECASE):
            text = _strip_html(cell_html)
            text = re.sub(r"^Control\(s\)\s*:?", "", text, flags=re.IGNORECASE).strip()
            return text
    return ""


def _extract_emission_factor(payload: str) -> tuple[str, str, str]:
    pattern = re.compile(
        r"<tr[^>]*>\s*<td[^>]*>.*?Emission Factor.*?</td>\s*<td[^>]*>(.*?)</td>",
        re.IGNORECASE | re.DOTALL,
    )
    match = pattern.search(payload)
    if not match:
        return "", "", ""
    text = _strip_html(match.group(1)).replace("--", "").strip()
    if " per " in text:
        left, right = text.split(" per ", 1)
        left_parts = left.split()
        factor = left_parts[0] if left_parts else text
        unit = " ".join(left_parts[1:]).strip()
        activity = right.strip()
        return factor, unit, activity
    return text, "", ""


def _extract_quality(payload: str) -> str:
    raw = _extract_row_value(payload, "Quality")
    if not raw:
        return ""
    cleaned = raw.replace("--", "").strip()
    return cleaned.split()[0] if cleaned else ""


def fetch_webfire_detail(factor_id: int) -> dict[str, Any]:
    url = _build_detail_url(factor_id)
    headers = {"User-Agent": "SCCFactorSelector/0.1"}
    with httpx.Client(timeout=30.0) as client:
        response = client.get(url, headers=headers)
        response.raise_for_status()
        html_text = response.text

    scc = _extract_row_value(html_text, "SCC")
    level1 = _extract_row_value(html_text, "Level 1")
    level2 = _extract_row_value(html_text, "Level 2")
    level3 = _extract_row_value(html_text, "Level 3")
    level4 = _extract_row_value(html_text, "Level 4")
    levels = [level for level in (level1, level2, level3, level4) if level]
    scctext = " > ".join(levels)
    pollutant, nei, cas = _extract_pollutant_row(html_text)
    control = _extract_control(html_text)
    factor, unit, activity = _extract_emission_factor(html_text)
    quality = _extract_quality(html_text)
    references = _extract_row_value(html_text, "References")
    ap42section = _extract_row_value(html_text, "AP 42 Section")
    formula = _extract_row_value(html_text, "Formula")
    notes = _extract_row_value(html_text, "Notes")
    condition = _extract_row_value(html_text, "Condition")
    variable_definition = _extract_row_value(html_text, "Variable Definition")
    applicability = _extract_row_value(html_text, "Applicability")
    derivation = _extract_row_value(html_text, "Derivation")
    created = _extract_row_value(html_text, "Created")
    record_updated = _extract_row_value(html_text, "Record Updated")
    if not record_updated:
        record_updated = _extract_row_value(html_text, "Date Record Updated")

    return {
        "factorid": factor_id,
        "scc": scc,
        "scctext": scctext,
        "pollutant": pollutant,
        "nei_pollutant_code": nei,
        "cas": cas,
        "control_1": control,
        "factor": factor,
        "factor_text": factor,
        "unit": unit,
        "activity": activity,
        "quality": quality,
        "ap42section": ap42section,
        "formula": formula,
        "notes": notes,
        "condition": condition,
        "variable_definition": variable_definition,
        "applicability": applicability,
        "derivation": derivation,
        "references": references,
        "created": created,
        "date_record_updated": record_updated,
    }
