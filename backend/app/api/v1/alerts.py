from fastapi import APIRouter, HTTPException

from app.db.connection import get_connection

router = APIRouter(prefix="/api/v1/alerts", tags=["alerts"])


@router.get("")
def list_alerts() -> dict:
    query = """
        SELECT
            a.id,
            a.dataset_id,
            d.title AS dataset_title,
            d.organization_id,
            a.alert_type,
            a.severity,
            a.message,
            a.measured_at
        FROM alert_events a
        JOIN datasets d
            ON d.id = a.dataset_id
        ORDER BY a.measured_at DESC
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()

    items = []
    for row in rows:
        items.append(
            {
                "alertId": str(row["id"]),
                "datasetId": str(row["dataset_id"]),
                "datasetTitle": row["dataset_title"],
                "organizationId": str(row["organization_id"]),
                "alertType": row["alert_type"],
                "severity": row["severity"],
                "message": row["message"],
                "measuredAt": row["measured_at"].isoformat() if row["measured_at"] else None,
            }
        )

    return {"items": items}


@router.get("/{alert_id}")
def get_alert(alert_id: str) -> dict:
    query = """
        SELECT
            id,
            dataset_id,
            alert_type,
            severity,
            message,
            measured_at,
            payload_json
        FROM alert_events
        WHERE id = %s
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (alert_id,))
            row = cur.fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="alert not found")

    return {
        "alertId": str(row["id"]),
        "datasetId": str(row["dataset_id"]),
        "alertType": row["alert_type"],
        "severity": row["severity"],
        "message": row["message"],
        "measuredAt": row["measured_at"].isoformat() if row["measured_at"] else None,
        "payload": row["payload_json"],
    }