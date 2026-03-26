from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from psycopg import connect

from app.api.v1.dashboard import router as dashboard_router
from app.api.v1.datasets import router as datasets_router
from app.api.v1.organizations import router as organizations_router
from app.config import settings
from app.api.v1.alerts import router as alerts_router

app = FastAPI(
    title="Data Quality Monitor API",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(datasets_router)
app.include_router(organizations_router)
app.include_router(dashboard_router)
app.include_router(alerts_router)


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Data Quality Monitor API"}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/health/db")
def health_db() -> dict[str, str]:
    with connect(settings.database_url) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT 1;")
            cur.fetchone()

    return {"status": "ok"}