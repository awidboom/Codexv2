from __future__ import annotations

import json
from datetime import datetime, timedelta
from typing import Any, Iterable, List, Tuple

import httpx
from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import ApiCache
from .settings import SETTINGS


ParamList = List[Tuple[str, str]]


def _build_url(path: str) -> str:
    base = SETTINGS.scc_base_url.rstrip("/")
    return f"{base}/{path.lstrip('/')}"


def _serialize_params(params: Iterable[Tuple[str, str]]) -> str:
    return json.dumps(list(params), sort_keys=True)


def _cache_cutoff() -> datetime:
    return datetime.utcnow() - timedelta(hours=SETTINGS.scc_cache_ttl_hours)


def fetch_scc_data(db: Session, path: str, params: ParamList) -> Any:
    url = _build_url(path)
    params_json = _serialize_params(params)
    cache_key = f"{url}|{params_json}"

    stmt = select(ApiCache).where(ApiCache.cache_key == cache_key)
    cached = db.execute(stmt).scalars().first()
    if cached and cached.fetched_at >= _cache_cutoff():
        return json.loads(cached.raw_payload_json)

    headers = {"User-Agent": "SCCFactorSelector/0.1"}
    with httpx.Client(timeout=30.0) as client:
        response = client.get(url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()

    if cached is None:
        cached = ApiCache(
            cache_key=cache_key,
            source_url=url,
            params_json=params_json,
            fetched_at=datetime.utcnow(),
            raw_payload_json=json.dumps(data),
        )
        db.add(cached)
    else:
        cached.fetched_at = datetime.utcnow()
        cached.raw_payload_json = json.dumps(data)

    db.commit()
    return data
