# Project Log

## 2026-01-20
- **Summary:** Initialized project scaffold, wired WebFIRE API integration, SCC hierarchy search, and bulk download list.
- **Decisions:**
  - Using EPA WebFIRE `efwebsrv5.cfc` endpoint with 24h cache.
  - SCC metadata pulled from `sor-scc-api.epa.gov` with 7-day cache.
  - Bulk Download List is client-side for now.
- **Open Questions:**
  - Should bulk list persist across sessions?
  - Should SCC Level 1-4 be shown in factor details modal?
  - Certain PM EFs for example will select multiple pollutant rows when only clicking one. Need to      assess this. 
- **Next Steps:**
  - Confirm SCC dropdowns meet user needs.
  - Consider CSV schema (include selected pollutants list / SCC metadata).
  - Figure out hosting/sharing

## Template
- **Summary:**
- **Decisions:**
- **Open Questions:**
- **Next Steps:**
