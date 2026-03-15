from __future__ import annotations

import csv
import io
import json
from datetime import datetime, timedelta
from typing import Any, Dict

from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import StreamingResponse
from sqlalchemy import select, text
from sqlalchemy.orm import Session

from .db import Base, engine, SessionLocal
from .models import QueryLog, SourceSnapshot, EmissionFactor, EmissionFactorSnapshot
from .schemas import SearchResult, FactorDetail, FactorHistoryItem, BulkExportRequest
from .settings import SETTINGS
from .scc import fetch_scc_data
from .ap42 import (
    fetch_ap42_sections,
    fetch_ap42_results,
    fetch_ap42_results_by_ids,
    fetch_ap42_factor_ids,
    fetch_ap42_search_html,
    parse_ap42_factor_ids,
)
from .webfire import fetch_webfire_data, fetch_webfire_reference

app = FastAPI(title="SCC Factor Selector")

EXPORT_FIELDS = [
    "FACTORID",
    "SCC",
    "LEVEL1",
    "LEVEL2",
    "LEVEL3",
    "LEVEL4",
    "DATA_CATEGORY",
    "MAP_TO",
    "POLLUTANT",
    "NEI_POLLUTANT_CODE",
    "CAS",
    "FACTOR",
    "FORMULA",
    "UNIT",
    "MEASURE",
    "MATERIAL",
    "ACTION",
    "EIS_ACTION_CODE",
    "EIS_NUMERATOR_CODE",
    "EIS_DENOMINATOR_CODE",
    "EIS_MATERIAL_CODE",
    "CONTROL_1",
    "CONTROLCODE_1",
    "CONTROL_2",
    "CONTROLCODE_2",
    "CONTROL_3",
    "CONTROLCODE_3",
    "CONTROL_4",
    "CONTROLCODE_4",
    "CONTROL_5",
    "CONTROLCODE_5",
    "REF_DESC",
    "NOTES",
    "QUALITY",
    "COMPOSITE_TEST_RATING",
    "CREATED",
    "REVOKED",
    "DUPCOUNT",
    "DUPREASON",
    "CONDITION",
    "VARIABLE_DEFINITION",
    "APPLICABILITY",
    "DERIVATION",
    "DATE_CSV_UPDATED",
    "DATE_RECORD_UPDATED",
    "RECORD_UPDATE_REASON",
    "BARR_WEBFIRE_ACCESSED_AT",
]


@app.on_event("startup")
def startup() -> None:
    Base.metadata.create_all(bind=engine)
    _ensure_factor_text_column()
    _ensure_references_column()


def _ensure_factor_text_column() -> None:
    if not SETTINGS.database_url.startswith("sqlite"):
        return
    with engine.begin() as connection:
        rows = connection.execute(text("PRAGMA table_info(emission_factor)")).fetchall()
        columns = {row[1] for row in rows}
        if "factor_text" not in columns:
            connection.execute(text("ALTER TABLE emission_factor ADD COLUMN factor_text TEXT"))


def _ensure_references_column() -> None:
    if not SETTINGS.database_url.startswith("sqlite"):
        return
    with engine.begin() as connection:
        rows = connection.execute(text("PRAGMA table_info(emission_factor)")).fetchall()
        columns = {row[1] for row in rows}
        if "references_text" not in columns:
            connection.execute(text("ALTER TABLE emission_factor ADD COLUMN references_text TEXT"))


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def _normalize_params(params: Dict[str, Any]) -> Dict[str, Any]:
    cleaned = {k: v for k, v in params.items() if v is not None and v != ""}
    return dict(sorted(cleaned.items()))


def _serialize_params(params: Dict[str, Any]) -> str:
    return json.dumps(params, sort_keys=True)


def _cache_ttl_cutoff() -> datetime:
    return datetime.utcnow() - timedelta(hours=SETTINGS.cache_ttl_hours)


def _get_latest_snapshot(db: Session, params_json: str) -> SourceSnapshot | None:
    stmt = (
        select(SourceSnapshot)
        .join(QueryLog)
        .where(QueryLog.query_params_json == params_json)
        .order_by(SourceSnapshot.fetched_at.desc())
        .limit(1)
    )
    return db.execute(stmt).scalars().first()


def _upsert_factor(db: Session, record: Dict[str, Any]) -> EmissionFactor:
    def _to_float(value: Any) -> float | None:
        try:
            return float(value)
        except (TypeError, ValueError):
            return None

    factor_id = record.get("factorid")
    stmt = select(EmissionFactor).where(EmissionFactor.factor_id == factor_id)
    factor = db.execute(stmt).scalars().first()
    if factor is None:
        factor = EmissionFactor(factor_id=factor_id)
        db.add(factor)

    factor.pollutant = record.get("pollutant")
    factor.scc = str(record.get("scc")) if record.get("scc") is not None else None
    factor.scctext = record.get("scctext")
    factor_value_raw = record.get("factor")
    factor.factor_value = _to_float(factor_value_raw)
    factor.factor_text = str(factor_value_raw) if factor_value_raw is not None else None
    factor.references_text = record.get("references") or record.get("reference")
    factor.unit = record.get("unit")
    factor.quality = record.get("quality")
    factor.factor_status = record.get("factor_status")
    factor.activity = record.get("activity")
    factor.ap42section = str(record.get("ap42section")) if record.get("ap42section") is not None else None
    factor.data_category = record.get("data_category")
    factor.control_1 = record.get("control_1")
    factor.control_2 = record.get("control_2")
    factor.control_3 = record.get("control_3")
    factor.control_4 = record.get("control_4")
    factor.control_5 = record.get("control_5")
    factor.created = record.get("created")
    factor.date_record_updated = record.get("date_record_updated")

    return factor


def _attach_snapshot(db: Session, factor: EmissionFactor, snapshot: SourceSnapshot) -> None:
    stmt = (
        select(EmissionFactorSnapshot)
        .where(EmissionFactorSnapshot.emission_factor_id == factor.id)
        .where(EmissionFactorSnapshot.valid_to.is_(None))
        .order_by(EmissionFactorSnapshot.valid_from.desc())
        .limit(1)
    )
    latest = db.execute(stmt).scalars().first()
    if latest is not None:
        latest.valid_to = snapshot.fetched_at

    link = EmissionFactorSnapshot(
        emission_factor_id=factor.id,
        source_snapshot_id=snapshot.id,
        valid_from=snapshot.fetched_at,
        valid_to=None,
    )
    db.add(link)


def _record_snapshot(db: Session, params: Dict[str, Any], data: Dict[str, Any]) -> SourceSnapshot:
    params_json = _serialize_params(params)
    base = SETTINGS.webfire_base_url.rstrip("/")
    source_url = f"{base}/getEFData"

    query_log = QueryLog(query_params_json=params_json, requested_at=datetime.utcnow(), source_url=source_url)
    db.add(query_log)
    db.flush()

    snapshot = SourceSnapshot(
        query_log_id=query_log.id,
        fetched_at=datetime.utcnow(),
        raw_payload_json=json.dumps(data),
        source_version=None,
    )
    db.add(snapshot)
    db.flush()

    for record in data.get("results", []):
        factor = _upsert_factor(db, record)
        db.flush()
        _attach_snapshot(db, factor, snapshot)

    db.commit()
    return snapshot


def _normalize_payload(data: Dict[str, Any]) -> Dict[str, Any]:
    if not isinstance(data, dict):
        return data
    results = data.get("results")
    if isinstance(results, list) and len(results) == 1 and isinstance(results[0], dict):
        inner = results[0]
        if "results" in inner:
            return {
                "hits": int(inner.get("hits", len(inner.get("results", [])))),
                "results": inner.get("results", []),
            }
    return data


def _safe_factor_id(value: Any) -> int | None:
    if value is None:
        return None
    try:
        return int(str(value).strip())
    except (TypeError, ValueError):
        return None


def _enrich_references(db: Session, results: list[dict[str, Any]]) -> None:
    factor_ids = {_safe_factor_id(row.get("factorid")) for row in results}
    factor_ids.discard(None)
    if not factor_ids:
        return

    stmt = select(EmissionFactor).where(EmissionFactor.factor_id.in_(factor_ids))
    factors = db.execute(stmt).scalars().all()
    factor_map = {factor.factor_id: factor for factor in factors if factor.factor_id is not None}

    updated = False
    for row in results:
        factor_id = _safe_factor_id(row.get("factorid"))
        if not factor_id:
            continue
        cached = factor_map.get(factor_id)
        reference = cached.references_text if cached and cached.references_text else ""
        if not reference:
            reference = fetch_webfire_reference(factor_id)
            if reference and cached:
                cached.references_text = reference
                updated = True
        if reference:
            row["references"] = reference

    if updated:
        db.commit()


def _enrich_factor_text(db: Session, results: list[dict[str, Any]]) -> None:
    factor_ids = {_safe_factor_id(row.get("factorid")) for row in results}
    factor_ids.discard(None)
    if not factor_ids:
        return
    stmt = select(EmissionFactor).where(EmissionFactor.factor_id.in_(factor_ids))
    factors = db.execute(stmt).scalars().all()
    factor_map = {factor.factor_id: factor for factor in factors if factor.factor_id is not None}
    for row in results:
        factor_id = _safe_factor_id(row.get("factorid"))
        if not factor_id:
            continue
        cached = factor_map.get(factor_id)
        if cached and cached.factor_text:
            row["factor_text"] = cached.factor_text


def _get_or_fetch_snapshot(db: Session, params: Dict[str, Any]) -> tuple[SourceSnapshot, Dict[str, Any]]:
    params_json = _serialize_params(params)
    latest = _get_latest_snapshot(db, params_json)

    if latest and latest.fetched_at >= _cache_ttl_cutoff():
        payload = json.loads(latest.raw_payload_json)
        return latest, _normalize_payload(payload)

    data = fetch_webfire_data(params)
    normalized = _normalize_payload(data)
    snapshot = _record_snapshot(db, params, normalized)
    return snapshot, normalized


def _add_facets(params: list[tuple[str, str]], name: str, value: str) -> None:
    params.append(("facetName[]", name))
    params.append(("facetValue[]", value))
    params.append(("facetQualifier[]", "exact"))
    params.append(("facetMatchType[]", "whole_phrase"))


def _scc_facets(sector: str | None, level1: str | None, level2: str | None, level3: str | None) -> list[tuple[str, str]]:
    params: list[tuple[str, str]] = []
    if sector:
        _add_facets(params, "Sector", sector)
    if level1:
        _add_facets(params, "SCC Level One", level1)
    if level2:
        _add_facets(params, "SCC Level Two", level2)
    if level3:
        _add_facets(params, "SCC Level Three", level3)
    return params


@app.get("/api/search", response_model=SearchResult)
def search(request: Request, db: Session = Depends(get_db)) -> SearchResult:
    params = dict(request.query_params)
    normalized = _normalize_params(params)
    if not normalized:
        raise HTTPException(status_code=400, detail="At least one query parameter is required.")

    snapshot, data = _get_or_fetch_snapshot(db, normalized)
    _normalize_results_scctext(db, data.get("results", []))
    _enrich_factor_text(db, data.get("results", []))
    _enrich_references(db, data.get("results", []))
    return SearchResult(
        hits=int(data.get("hits", 0)),
        results=data.get("results", []),
        snapshot_id=snapshot.id,
        fetched_at=snapshot.fetched_at,
    )


@app.get("/api/factors/{factor_id}", response_model=FactorDetail)
def factor_detail(factor_id: int, db: Session = Depends(get_db)) -> FactorDetail:
    factor = db.execute(select(EmissionFactor).where(EmissionFactor.id == factor_id)).scalars().first()
    if factor is None:
        raise HTTPException(status_code=404, detail="Factor not found.")

    history_items = []
    for snap in factor.snapshots:
        history_items.append(
            FactorHistoryItem(
                snapshot_id=snap.source_snapshot_id,
                fetched_at=snap.source_snapshot.fetched_at,
                valid_from=snap.valid_from,
                valid_to=snap.valid_to,
            )
        )

    return FactorDetail(
        id=factor.id,
        factor_id=factor.factor_id,
        pollutant=factor.pollutant,
        scc=factor.scc,
        scctext=factor.scctext,
        factor_value=factor.factor_value,
        references=factor.references_text,
        unit=factor.unit,
        quality=factor.quality,
        factor_status=factor.factor_status,
        activity=factor.activity,
        ap42section=factor.ap42section,
        data_category=factor.data_category,
        control_1=factor.control_1,
        control_2=factor.control_2,
        control_3=factor.control_3,
        control_4=factor.control_4,
        control_5=factor.control_5,
        created=factor.created,
        date_record_updated=factor.date_record_updated,
        history=history_items,
    )


@app.get("/api/export")
def export_csv(request: Request, db: Session = Depends(get_db)) -> StreamingResponse:
    params = dict(request.query_params)
    normalized = _normalize_params(params)
    if not normalized:
        raise HTTPException(status_code=400, detail="At least one query parameter is required.")

    snapshot, data = _get_or_fetch_snapshot(db, normalized)
    results = data.get("results", [])
    if not results:
        raise HTTPException(status_code=404, detail="No results to export.")
    _enrich_references(db, results)

    accessed_at = snapshot.fetched_at.isoformat()
    latest_update = _latest_record_update(results)
    latest_update_text = latest_update.isoformat() if latest_update else ""

    output = io.StringIO()
    levels_map = _normalize_results_scctext(db, results)
    writer = csv.DictWriter(output, fieldnames=EXPORT_FIELDS)
    writer.writeheader()
    for row in results:
        writer.writerow(_build_export_row(row, accessed_at, latest_update_text, levels_map))

    filename = f"webfire_export_{snapshot.id}.csv"
    output.seek(0)
    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )


def _filter_by_pollutants(results: list[dict[str, Any]], pollutants: list[str] | None) -> list[dict[str, Any]]:
    if not pollutants:
        return results
    allowed = {p.strip().lower() for p in pollutants if p.strip()}
    if not allowed:
        return results
    filtered = []
    for row in results:
        pollutant = str(row.get("pollutant", "")).strip().lower()
        if pollutant in allowed:
            filtered.append(row)
    return filtered


def _extract_reference(row: dict[str, Any]) -> str:
    for key in ("references", "reference", "ref"):
        value = row.get(key)
        if value:
            return str(value)
    return ""


def _parse_record_date(value: Any) -> datetime | None:
    if not value:
        return None
    text = str(value).strip()
    if not text:
        return None
    formats = [
        "%B, %d %Y %H:%M:%S",
        "%B %d %Y %H:%M:%S",
        "%m/%d/%Y",
        "%m/%d/%Y %H:%M:%S",
        "%Y-%m-%d",
    ]
    for fmt in formats:
        try:
            return datetime.strptime(text, fmt)
        except ValueError:
            continue
    return None


def _fetch_scc_levels(db: Session, scc: str) -> tuple[str, str, str, str] | None:
    if not scc:
        return None
    data = fetch_scc_data(db, f"/SCC/{scc}", [])
    item = data[0] if isinstance(data, list) and data else data
    if not isinstance(item, dict):
        return None
    attrs = item.get("attributes") or {}
    if not isinstance(attrs, dict):
        return None
    level1 = (attrs.get("scc level one") or {}).get("text", "").strip()
    level2 = (attrs.get("scc level two") or {}).get("text", "").strip()
    level3 = (attrs.get("scc level three") or {}).get("text", "").strip()
    level4 = (attrs.get("scc level four") or {}).get("text", "").strip()
    if not any([level1, level2, level3, level4]):
        return None
    return level1, level2, level3, level4


def _get_scc_levels_map(db: Session, results: list[dict[str, Any]]) -> dict[str, tuple[str, str, str, str]]:
    levels_map: dict[str, tuple[str, str, str, str]] = {}
    for row in results:
        scc = str(row.get("scc") or "").strip()
        if not scc or scc in levels_map:
            continue
        levels = _fetch_scc_levels(db, scc)
        if levels:
            levels_map[scc] = levels
    return levels_map


def _normalize_results_scctext(
    db: Session, results: list[dict[str, Any]]
) -> dict[str, tuple[str, str, str, str]]:
    if not results:
        return {}
    levels_map = _get_scc_levels_map(db, results)
    if not levels_map:
        return {}
    for row in results:
        scc = str(row.get("scc") or "").strip()
        levels = levels_map.get(scc)
        if levels:
            row["scctext"] = " > ".join([level for level in levels if level])
    return levels_map


def _split_scctext_levels(scctext: Any) -> tuple[str, str, str, str]:
    if not scctext:
        return "", "", "", ""
    parts = [part.strip() for part in str(scctext).split(">")]
    levels = [part for part in parts if part]
    padded = (levels + ["", "", "", ""])[:4]
    return padded[0], padded[1], padded[2], padded[3]


def _build_export_row(
    row: dict[str, Any],
    accessed_at: str,
    latest_update_text: str,
    levels_map: dict[str, tuple[str, str, str, str]] | None = None,
) -> dict[str, Any]:
    level1 = level2 = level3 = level4 = ""
    scc = str(row.get("scc") or "").strip()
    if levels_map and scc in levels_map:
        level1, level2, level3, level4 = levels_map[scc]
    else:
        level1, level2, level3, level4 = _split_scctext_levels(row.get("scctext"))
    factor_value = row.get("factor")
    if factor_value is None:
        factor_value = row.get("factor_text")
    revoked = row.get("revoked_date") or ""
    if not revoked and row.get("factor_status") == "Revoked":
        revoked = "Revoked"
    return {
        "FACTORID": row.get("factorid") or "",
        "SCC": scc,
        "LEVEL1": level1,
        "LEVEL2": level2,
        "LEVEL3": level3,
        "LEVEL4": level4,
        "DATA_CATEGORY": row.get("data_category") or "",
        "MAP_TO": row.get("map_to") or "",
        "POLLUTANT": row.get("pollutant") or "",
        "NEI_POLLUTANT_CODE": row.get("nei_pollutant_code") or "",
        "CAS": row.get("cas") or "",
        "FACTOR": factor_value if factor_value is not None else "",
        "FORMULA": row.get("formula") or "",
        "UNIT": row.get("unit") or "",
        "MEASURE": row.get("measure") or "",
        "MATERIAL": row.get("material") or "",
        "ACTION": row.get("action") or "",
        "EIS_ACTION_CODE": row.get("eis_action_code") or "",
        "EIS_NUMERATOR_CODE": row.get("eis_numerator_code") or "",
        "EIS_DENOMINATOR_CODE": row.get("eis_denominator_code") or "",
        "EIS_MATERIAL_CODE": row.get("eis_material_code") or "",
        "CONTROL_1": row.get("control_1") or "",
        "CONTROLCODE_1": row.get("controlcode_1") or "",
        "CONTROL_2": row.get("control_2") or "",
        "CONTROLCODE_2": row.get("controlcode_2") or "",
        "CONTROL_3": row.get("control_3") or "",
        "CONTROLCODE_3": row.get("controlcode_3") or "",
        "CONTROL_4": row.get("control_4") or "",
        "CONTROLCODE_4": row.get("controlcode_4") or "",
        "CONTROL_5": row.get("control_5") or "",
        "CONTROLCODE_5": row.get("controlcode_5") or "",
        "REF_DESC": _extract_reference(row),
        "NOTES": row.get("notes") or "",
        "QUALITY": row.get("quality") or "",
        "COMPOSITE_TEST_RATING": row.get("composite_test_rating") or "",
        "CREATED": row.get("created") or "",
        "REVOKED": revoked,
        "DUPCOUNT": row.get("dupcount") or "",
        "DUPREASON": row.get("dupreason") or "",
        "CONDITION": row.get("condition") or "",
        "VARIABLE_DEFINITION": row.get("variable_definition") or "",
        "APPLICABILITY": row.get("applicability") or "",
        "DERIVATION": row.get("derivation") or "",
        "DATE_CSV_UPDATED": latest_update_text or accessed_at,
        "DATE_RECORD_UPDATED": row.get("date_record_updated") or "",
        "RECORD_UPDATE_REASON": row.get("record_update_reason") or "",
        "BARR_WEBFIRE_ACCESSED_AT": accessed_at,
    }


def _latest_record_update(results: list[dict[str, Any]]) -> datetime | None:
    latest: datetime | None = None
    for row in results:
        candidate = _parse_record_date(row.get("date_record_updated")) or _parse_record_date(
            row.get("created")
        )
        if candidate and (latest is None or candidate > latest):
            latest = candidate
    return latest


@app.post("/api/export/bulk")
def export_bulk(payload: BulkExportRequest, db: Session = Depends(get_db)) -> StreamingResponse:
    combined: list[dict[str, Any]] = []
    accessed_values: list[str] = []
    latest_updates: list[datetime] = []
    for item in payload.items:
        params = {"SCC": item.scc}
        snapshot, data = _get_or_fetch_snapshot(db, params)
        results = data.get("results", [])
        filtered = _filter_by_pollutants(results, item.pollutants)
        combined.extend(filtered)
        accessed_values.append(snapshot.fetched_at.isoformat())
        latest = _latest_record_update(results)
        if latest:
            latest_updates.append(latest)

    if not combined:
        raise HTTPException(status_code=404, detail="No results to export.")
    _enrich_references(db, combined)

    latest_update_text = max(latest_updates).isoformat() if latest_updates else ""
    accessed_at = max(accessed_values) if accessed_values else ""
    output = io.StringIO()
    levels_map = _normalize_results_scctext(db, combined)
    writer = csv.DictWriter(output, fieldnames=EXPORT_FIELDS)
    writer.writeheader()
    for row in combined:
        writer.writerow(_build_export_row(row, accessed_at, latest_update_text, levels_map))

    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    filename = f"webfire_bulk_export_{timestamp}.csv"
    output.seek(0)
    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )


@app.get("/api/scc/sectors")
def scc_sectors(db: Session = Depends(get_db)) -> list[dict[str, str]]:
    data = fetch_scc_data(db, "/LookupElement/Name/Sector", [])
    sectors = []
    for item in data or []:
        name = item.get("code") or ""
        attrs = item.get("attributes") or {}
        sector_code = ""
        if isinstance(attrs, dict):
            sector_code = (attrs.get("sector code") or {}).get("text", "")
        if name:
            sectors.append({"name": name, "sector_code": sector_code})
    return sorted(sectors, key=lambda x: x["name"].lower())


@app.get("/api/scc/hierarchy")
def scc_hierarchy(
    level: int,
    sector: str | None = None,
    level1: str | None = None,
    level2: str | None = None,
    level3: str | None = None,
    db: Session = Depends(get_db),
) -> list[str]:
    params = _scc_facets(sector, level1, level2, level3)
    params.append(("level[]", str(level)))
    data = fetch_scc_data(db, "/SCCHierarchyItem", params)
    names = sorted({item.get("name") for item in data or [] if item.get("name")})
    return names


@app.get("/api/scc/search")
def scc_search(
    sector: str | None = None,
    level1: str | None = None,
    level2: str | None = None,
    level3: str | None = None,
    level4: str | None = None,
    pageSize: int = 200,
    db: Session = Depends(get_db),
) -> list[dict[str, str]]:
    params = _scc_facets(sector, level1, level2, level3)
    if level4:
        _add_facets(params, "SCC Level Four", level4)
    params.append(("pageSize", str(pageSize)))
    data = fetch_scc_data(db, "/SCC", params)

    results = []
    for item in data or []:
        attrs = item.get("attributes") or {}
        code = item.get("code") or (attrs.get("code") or {}).get("text")
        short_name = (attrs.get("short name") or {}).get("text", "")
        level4_name = (attrs.get("scc level four") or {}).get("text", "")
        if code:
            results.append(
                {
                    "code": str(code),
                    "short_name": short_name,
                    "level4": level4_name,
                }
            )
    return results


@app.get("/api/scc/code-search")
def scc_code_search(query: str, limit: int = 25, db: Session = Depends(get_db)) -> list[dict[str, str]]:
    if not query.strip():
        return []
    params = [
        ("facetName[]", "Code"),
        ("facetValue[]", query.strip()),
        ("facetQualifier[]", "begins"),
        ("facetMatchType[]", "whole_phrase"),
        ("pageSize", str(limit)),
    ]
    data = fetch_scc_data(db, "/SCC", params)
    results = []
    for item in data or []:
        attrs = item.get("attributes") or {}
        code = item.get("code") or (attrs.get("code") or {}).get("text")
        level4 = (attrs.get("scc level four") or {}).get("text", "")
        sector = (attrs.get("sector") or {}).get("text", "")
        if code:
            results.append(
                {
                    "code": str(code),
                    "level4": level4,
                    "sector": sector,
                }
            )
    return results


@app.get("/api/ap42/sections")
def ap42_sections(db: Session = Depends(get_db)) -> list[dict[str, str]]:
    return fetch_ap42_sections(db)


@app.get("/api/ap42/search", response_model=SearchResult)
def ap42_search(section: str, db: Session = Depends(get_db)) -> SearchResult:
    results = fetch_ap42_results(db, section)
    _normalize_results_scctext(db, results)
    _enrich_factor_text(db, results)
    return SearchResult(
        hits=len(results),
        results=results,
        snapshot_id=0,
        fetched_at=datetime.utcnow(),
    )


@app.get("/api/ap42/debug")
def ap42_debug(section: str, db: Session = Depends(get_db)) -> dict[str, Any]:
    ids = fetch_ap42_factor_ids(db, section)
    return {
        "section": section,
        "count": len(ids),
        "sample_ids": ids[:10],
    }


@app.get("/api/ap42/debug-html")
def ap42_debug_html(section: str) -> dict[str, Any]:
    html_payload = fetch_ap42_search_html(section)
    factor_ids = parse_ap42_factor_ids(html_payload)
    detail_index = html_payload.lower().find("detail.cfm")
    fid_index = html_payload.lower().find("fid=")
    detail_snippet = ""
    fid_snippet = ""
    if detail_index != -1:
        detail_snippet = html_payload[detail_index:detail_index + 300]
    if fid_index != -1:
        fid_snippet = html_payload[fid_index:fid_index + 200]
    return {
        "section": section,
        "length": len(html_payload),
        "snippet": html_payload[:2000],
        "fid_count": len(factor_ids),
        "fid_sample": factor_ids[:10],
        "detail_count": html_payload.lower().count("detail.cfm"),
        "fid_literal_count": html_payload.lower().count("fid="),
        "detail_snippet": detail_snippet,
        "fid_snippet": fid_snippet,
    }


@app.get("/api/ap42/export")
def ap42_export(section: str, db: Session = Depends(get_db)) -> StreamingResponse:
    results = fetch_ap42_results(db, section)
    levels_map = _normalize_results_scctext(db, results)
    _enrich_factor_text(db, results)
    if not results:
        raise HTTPException(status_code=404, detail="No results to export.")

    accessed_at = datetime.utcnow().isoformat()
    latest_update = _latest_record_update(results)
    latest_update_text = latest_update.isoformat() if latest_update else ""

    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=EXPORT_FIELDS)
    writer.writeheader()
    for row in results:
        writer.writerow(_build_export_row(row, accessed_at, latest_update_text, levels_map))

    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    filename = f"webfire_ap42_export_{timestamp}.csv"
    output.seek(0)
    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )


@app.post("/api/ap42/export/selected")
def ap42_export_selected(payload: dict[str, Any]) -> StreamingResponse:
    raw_ids = payload.get("factor_ids") or []
    factor_ids = []
    for value in raw_ids:
        try:
            factor_ids.append(int(value))
        except (TypeError, ValueError):
            continue

    if not factor_ids:
        raise HTTPException(status_code=400, detail="No factor IDs provided.")

    results = fetch_ap42_results_by_ids(factor_ids)
    levels_map = _normalize_results_scctext(db, results)
    _enrich_factor_text(db, results)
    if not results:
        raise HTTPException(status_code=404, detail="No results to export.")

    accessed_at = datetime.utcnow().isoformat()
    latest_update = _latest_record_update(results)
    latest_update_text = latest_update.isoformat() if latest_update else ""

    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=EXPORT_FIELDS)
    writer.writeheader()
    for row in results:
        writer.writerow(_build_export_row(row, accessed_at, latest_update_text, levels_map))

    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    filename = f"webfire_ap42_selected_export_{timestamp}.csv"
    output.seek(0)
    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )
