from __future__ import annotations

from datetime import datetime

from sqlalchemy import Column, DateTime, Float, Integer, String, Text, ForeignKey, Index
from sqlalchemy.orm import relationship

from .db import Base


class QueryLog(Base):
    __tablename__ = "query_log"

    id = Column(Integer, primary_key=True)
    query_params_json = Column(Text, nullable=False)
    requested_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    source_url = Column(String(512), nullable=False)

    snapshots = relationship("SourceSnapshot", back_populates="query_log")


class SourceSnapshot(Base):
    __tablename__ = "source_snapshot"

    id = Column(Integer, primary_key=True)
    query_log_id = Column(Integer, ForeignKey("query_log.id"), nullable=False)
    fetched_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    raw_payload_json = Column(Text, nullable=False)
    source_version = Column(String(128), nullable=True)

    query_log = relationship("QueryLog", back_populates="snapshots")
    factor_snapshots = relationship("EmissionFactorSnapshot", back_populates="source_snapshot")


class EmissionFactor(Base):
    __tablename__ = "emission_factor"

    id = Column(Integer, primary_key=True)
    factor_id = Column(Integer, nullable=True, index=True)
    pollutant = Column(String(128), nullable=True)
    scc = Column(String(32), nullable=True, index=True)
    scctext = Column(Text, nullable=True)
    factor_value = Column(Float, nullable=True)
    factor_text = Column(Text, nullable=True)
    references_text = Column(Text, nullable=True)
    unit = Column(String(64), nullable=True)
    quality = Column(String(8), nullable=True)
    factor_status = Column(String(32), nullable=True)
    activity = Column(String(256), nullable=True)
    ap42section = Column(String(32), nullable=True)
    data_category = Column(String(64), nullable=True)
    control_1 = Column(String(128), nullable=True)
    control_2 = Column(String(128), nullable=True)
    control_3 = Column(String(128), nullable=True)
    control_4 = Column(String(128), nullable=True)
    control_5 = Column(String(128), nullable=True)
    created = Column(String(64), nullable=True)
    date_record_updated = Column(String(64), nullable=True)

    snapshots = relationship("EmissionFactorSnapshot", back_populates="emission_factor")


class EmissionFactorSnapshot(Base):
    __tablename__ = "emission_factor_snapshot"

    id = Column(Integer, primary_key=True)
    emission_factor_id = Column(Integer, ForeignKey("emission_factor.id"), nullable=False)
    source_snapshot_id = Column(Integer, ForeignKey("source_snapshot.id"), nullable=False)
    valid_from = Column(DateTime, nullable=False)
    valid_to = Column(DateTime, nullable=True)

    emission_factor = relationship("EmissionFactor", back_populates="snapshots")
    source_snapshot = relationship("SourceSnapshot", back_populates="factor_snapshots")


Index("ix_snapshot_factor", EmissionFactorSnapshot.emission_factor_id, EmissionFactorSnapshot.source_snapshot_id)


class ApiCache(Base):
    __tablename__ = "api_cache"

    id = Column(Integer, primary_key=True)
    cache_key = Column(String(512), nullable=False, unique=True, index=True)
    source_url = Column(String(512), nullable=False)
    params_json = Column(Text, nullable=False)
    fetched_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    raw_payload_json = Column(Text, nullable=False)
