from fastapi import APIRouter

from app.db.connection import get_connection

router = APIRouter(prefix="/api/v1/datasets", tags=["datasets"])


@router.get("")
def list_datasets() -> dict:
    query = """
        SELECT
            d.id,
            d.organization_id,
            d.title,
            d.source_type,
            d.last_updated,
            d.monitoring_enabled,
            d.excluded_from_scoring,
            d.created_at,
            d.updated_at
        FROM datasets d
        ORDER BY d.created_at DESC
        LIMIT 100
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()

    items = []
    for row in rows:
        items.append(
            {
                "datasetId": str(row["id"]),
                "organizationId": str(row["organization_id"]),
                "title": row["title"],
                "sourceType": row["source_type"],
                "lastUpdated": row["last_updated"].isoformat() if row["last_updated"] else None,
                "monitoringEnabled": row["monitoring_enabled"],
                "excludedFromScoring": row["excluded_from_scoring"],
                "createdAt": row["created_at"].isoformat() if row["created_at"] else None,
                "updatedAt": row["updated_at"].isoformat() if row["updated_at"] else None,
            }
        )

    return {"items": items}