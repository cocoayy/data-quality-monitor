# data-quality-monitor

オープンデータ向けのデータ品質監視ツール

## 技術スタック
- Frontend: Next.js
- Backend: FastAPI
- Database: PostgreSQL
- Batch: Python

## 必要なもの
- Python
- Node.js
- PostgreSQL
- VS Code

## Backend起動
```bash
cd backend
python -m venv .venv
# macOS / Linux
source .venv/bin/activate
# Windows PowerShell
# .venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload