# Local Run Commands

Backend:
 cd "C:\Users\aer\Documents\PROJECTS\SCC Factor Selector\backend"
 .\.venv\Scripts\Activate.ps1
 uvicorn app.main:app --reload

Frontend:
cd "C:\Users\aer\Documents\PROJECTS\SCC Factor Selector\frontend"
npm run dev

Notes:
- If activation fails, run: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`
