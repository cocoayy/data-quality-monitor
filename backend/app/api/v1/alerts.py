from fastapi import APIRouter, HTTPException, Query

from app.db.connection import get_connection
from app.repositories.alert_repository import AlertRepository
from app.services.alert_service import AlertService

router = APIRouter(prefix="/api/v1/alerts", tags=["alerts"])


@router.get("")
def list_alerts(
    dataset_id: str | None = None,
    organization_id: str | None = None,
    alert_type: str | None = None,
    severity: str | None = None,
    keyword: str | None = Query(None, max_length=200),
) -> dict:
    with get_connection() as conn:
        repository = AlertRepository(conn)
        service = AlertService(repository)
        rows = service.list_alerts(
            dataset_id=dataset_id,
            organization_id=organization_id,
            alert_type=alert_type,
            severity=severity,
            keyword=keyword,
        )

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
    with get_connection() as conn:
        repository = AlertRepository(conn)
        service = AlertService(repository)
        row = service.get_alert_by_id(alert_id)

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
