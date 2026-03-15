# SCC Factor Selector

Local-first scaffolding for an internal emission factor search tool using the EPA WebFIRE API.

## Structure
- `backend/`: FastAPI service, caching, and history tracking.
- `frontend/`: React/Vite UI scaffold.

## Quick start (backend)
1) `cd backend`
2) Create a virtualenv and install deps:
   - `python -m venv .venv`
   - `./.venv/Scripts/activate`
   - `pip install -r requirements.txt`
3) Run the API:
   - `uvicorn app.main:app --reload`

## Quick start (frontend)
1) `cd frontend`
2) Install deps:
   - `npm install`
3) Run dev server:
   - `npm run dev`

## Notes
- The backend caches WebFIRE responses for 24 hours by default.
- Every response is stored as a snapshot with raw payload for audit/history.
- CSV export uses the latest cached snapshot for a query.
