from __future__ import annotations

import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    webfire_base_url: str
    webfire_detail_url: str
    webfire_search_url: str
    cache_ttl_hours: int
    database_url: str
    scc_base_url: str
    scc_cache_ttl_hours: int


SETTINGS = Settings(
    webfire_base_url=os.getenv("WEBFIRE_BASE_URL", "https://cfpub.epa.gov/webfire/efwebservices/"),
    webfire_detail_url=os.getenv(
        "WEBFIRE_DETAIL_URL",
        "https://cfpub.epa.gov/webfire/SearchEmissionFactor/detail.cfm",
    ),
    webfire_search_url=os.getenv(
        "WEBFIRE_SEARCH_URL",
        "https://cfpub.epa.gov/webfire/SearchEmissionFactor/searchpage.cfm",
    ),
    cache_ttl_hours=int(os.getenv("WEBFIRE_CACHE_TTL_HOURS", "24")),
    database_url=os.getenv("DATABASE_URL", "sqlite:///./webfire_cache.db"),
    scc_base_url=os.getenv("SCC_BASE_URL", "https://sor-scc-api.epa.gov/sccwebservices/v1"),
    scc_cache_ttl_hours=int(os.getenv("SCC_CACHE_TTL_HOURS", "168")),
)
