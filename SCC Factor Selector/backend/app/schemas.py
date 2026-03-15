from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class SearchResult(BaseModel):
    hits: int
    results: List[Dict[str, Any]]
    snapshot_id: int
    fetched_at: datetime


class FactorHistoryItem(BaseModel):
    snapshot_id: int
    fetched_at: datetime
    valid_from: datetime
    valid_to: Optional[datetime]


class FactorDetail(BaseModel):
    id: int
    factor_id: Optional[int]
    pollutant: Optional[str]
    scc: Optional[str]
    scctext: Optional[str]
    factor_value: Optional[float]
    references: Optional[str]
    unit: Optional[str]
    quality: Optional[str]
    factor_status: Optional[str]
    activity: Optional[str]
    ap42section: Optional[str]
    data_category: Optional[str]
    control_1: Optional[str]
    control_2: Optional[str]
    control_3: Optional[str]
    control_4: Optional[str]
    control_5: Optional[str]
    created: Optional[str]
    date_record_updated: Optional[str]
    history: List[FactorHistoryItem]


class BulkExportItem(BaseModel):
    scc: str
    pollutants: Optional[List[str]] = None


class BulkExportRequest(BaseModel):
    items: List[BulkExportItem]
