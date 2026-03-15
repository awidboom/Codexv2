from __future__ import annotations

import html
import json
import re
from datetime import datetime, timedelta
from typing import Any

import httpx
from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import ApiCache
from .settings import SETTINGS
from .webfire import fetch_webfire_detail


def _cache_cutoff() -> datetime:
    return datetime.utcnow() - timedelta(hours=SETTINGS.cache_ttl_hours)


def _parse_sections(payload: str) -> list[dict[str, str]]:
    match = re.search(
        r'<select[^>]*name="sectionfromap42"[^>]*>(.*?)</select>',
        payload,
        flags=re.IGNORECASE | re.DOTALL,
    )
    if not match:
        return []
    options_html = match.group(1)
    options: list[dict[str, str]] = []
    for option in re.finditer(
        r'<option[^>]*value="([^"]*)"\s*>(.*?)</option>',
        options_html,
        flags=re.IGNORECASE | re.DOTALL,
    ):
        value = html.unescape(option.group(1)).strip()
        label = html.unescape(option.group(2)).strip()
        if value and value.lower() != "all ap 42 sections":
            options.append({"value": value, "label": label})
    return options


def _extract_token(payload: str) -> str:
    match = re.search(r'name="token"[^>]*value="([^"]+)"', payload, flags=re.IGNORECASE)
    return match.group(1) if match else ""


def _build_search_action_url() -> str:
    base = SETTINGS.webfire_search_url
    if base.lower().endswith("searchpage.cfm"):
        return base[:-len("searchpage.cfm")] + "factorSearch2.cfm"
    return "https://cfpub.epa.gov/webfire/SearchEmissionFactor/factorSearch2.cfm"


def parse_ap42_factor_ids(payload: str) -> list[int]:
    ids = {int(fid) for fid in re.findall(r"detail\.cfm\?fid=(\d+)", payload, flags=re.IGNORECASE)}
    if not ids:
        ids = {int(fid) for fid in re.findall(r"fid=(\d+)", payload, flags=re.IGNORECASE)}
    return sorted(ids)


def fetch_ap42_factor_ids(db: Session, section: str) -> list[int]:
    section = section.strip()
    if not section:
        return []
    url = _build_search_action_url()
    cache_key = f"ap42_fids|{section}"
    stmt = select(ApiCache).where(ApiCache.cache_key == cache_key)
    cached = db.execute(stmt).scalars().first()
    if cached and cached.fetched_at >= _cache_cutoff():
        cached_payload = json.loads(cached.raw_payload_json)
        if cached_payload:
            return cached_payload

    html_payload = fetch_ap42_search_html(section)
    factor_ids = parse_ap42_factor_ids(html_payload)

    if not factor_ids:
        return []

    payload_json = json.dumps(factor_ids)
    if cached is None:
        cached = ApiCache(
            cache_key=cache_key,
            source_url=url,
            params_json=json.dumps({"sectionfromap42": section}),
            fetched_at=datetime.utcnow(),
            raw_payload_json=payload_json,
        )
        db.add(cached)
    else:
        cached.fetched_at = datetime.utcnow()
        cached.raw_payload_json = payload_json

    db.commit()
    return factor_ids


def fetch_ap42_search_html(section: str) -> str:
    section = section.strip()
    if not section:
        return ""
    url = _build_search_action_url()
    headers = {"User-Agent": "SCCFactorSelector/0.1"}
    with httpx.Client(timeout=30.0, follow_redirects=True) as client:
        page = client.get(SETTINGS.webfire_search_url, headers=headers)
        page.raise_for_status()
        token = _extract_token(page.text)
        payload = {
            "sectionfromap42": section,
            "token": token,
            "Submit": "Submit Search",
            "revokedcriteria": "exclude",
        }
        post_headers = {
            **headers,
            "Referer": SETTINGS.webfire_search_url,
            "Origin": "https://cfpub.epa.gov",
        }
        response = client.post(url, data=payload, headers=post_headers)
        response.raise_for_status()
        return response.text


def fetch_ap42_sections(db: Session) -> list[dict[str, str]]:
    url = SETTINGS.webfire_search_url
    cache_key = f"ap42_sections|{url}"
    stmt = select(ApiCache).where(ApiCache.cache_key == cache_key)
    cached = db.execute(stmt).scalars().first()
    if cached and cached.fetched_at >= _cache_cutoff():
        cached_payload = json.loads(cached.raw_payload_json)
        if cached_payload:
            return cached_payload

    headers = {"User-Agent": "SCCFactorSelector/0.1"}
    with httpx.Client(timeout=30.0) as client:
        response = client.get(url, headers=headers)
        response.raise_for_status()
        sections = _parse_sections(response.text)

    payload = json.dumps(sections)
    if cached is None:
        cached = ApiCache(
            cache_key=cache_key,
            source_url=url,
            params_json=json.dumps({}),
            fetched_at=datetime.utcnow(),
            raw_payload_json=payload,
        )
        db.add(cached)
    else:
        cached.fetched_at = datetime.utcnow()
        cached.raw_payload_json = payload

    db.commit()
    return sections


def fetch_ap42_results(db: Session, section: str) -> list[dict[str, Any]]:
    factor_ids = fetch_ap42_factor_ids(db, section)
    results = []
    for factor_id in factor_ids:
        detail = fetch_webfire_detail(factor_id)
        if detail:
            results.append(detail)
    return results


def fetch_ap42_results_by_ids(factor_ids: list[int]) -> list[dict[str, Any]]:
    results = []
    for factor_id in factor_ids:
        detail = fetch_webfire_detail(factor_id)
        if detail:
            results.append(detail)
    return results
