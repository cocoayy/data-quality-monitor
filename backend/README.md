# backend

FastAPI ベースのバックエンドAPI。

## 起動方法

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload