from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from app.db.connection import get_connection

router = APIRouter(prefix="/api/v1/datasets", tags=["datasets"])


class PatchMonitoringSettingsRequest(BaseModel):
    monitoringEnabled: bool | None = None
    excludedFromScoring: bool | None = None
    expectedUpdateCycle: str | None = None


@router.get("")
def list_datasets(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    organization_id: str | None = None,
    source_type: str | None = None,
    monitoring_enabled: bool | None = None,
    evaluation_status: str | None = None,
    rank: str | None = None,
    min_total_score: int | None = Query(None, ge=0, le=100),
    max_total_score: int | None = Query(None, ge=0, le=100),
    keyword: str | None = Query(None, max_length=200),
    sort_by: str = "created_at",
    sort_order: str = "desc",
) -> dict:
    allowed_sort_by = {
        "title": "d.title",
        "last_updated": "d.last_updated",
        "total_score": "q.total_score",
        "rank": "q.rank",
        "measured_at": "q.measured_at",
        "created_at": "d.created_at",
    }

    if sort_by not in allowed_sort_by:
        raise HTTPException(status_code=422, detail="invalid sort_by")

    if sort_order not in {"asc", "desc"}:
        raise HTTPException(status_code=422, detail="invalid sort_order")

    where_clauses = []
    params = []

    if organization_id:
        where_clauses.append("d.organization_id = %s")
        params.append(organization_id)

    if source_type:
        where_clauses.append("d.source_type = %s")
        params.append(source_type)

    if monitoring_enabled is not None:
        where_clauses.append("d.monitoring_enabled = %s")
        params.append(monitoring_enabled)

    if evaluation_status:
        where_clauses.append("q.evaluation_status = %s")
        params.append(evaluation_status)

    if rank:
        where_clauses.append("q.rank = %s")
        params.append(rank)

    if min_total_score is not None:
        where_clauses.append("q.total_score >= %s")
        params.append(min_total_score)

    if max_total_score is not None:
        where_clauses.append("q.total_score <= %s")
        params.append(max_total_score)

    if keyword:
        where_clauses.append("(d.title ILIKE %s OR d.description ILIKE %s)")
        keyword_like = f"%{keyword}%"
        params.extend([keyword_like, keyword_like])

    where_sql = ""
    if where_clauses:
        where_sql = "WHERE " + " AND ".join(where_clauses)

    offset = (page - 1) * page_size

    count_query = f"""
        SELECT COUNT(*) AS total_count
        FROM datasets d
        LEFT JOIN quality_score_snapshots q
            ON q.dataset_id = d.id
        {where_sql}
    """

    data_query = f"""
        SELECT
            d.id,
            d.organization_id,
            d.title,
            d.source_type,
            d.last_updated,
            d.monitoring_enabled,
            d.excluded_from_scoring,
            d.created_at,
            d.updated_at,
            q.total_score,
            q.rank,
            q.evaluation_status,
            q.measured_at
        FROM datasets d
        LEFT JOIN quality_score_snapshots q
            ON q.dataset_id = d.id
        {where_sql}
        ORDER BY {allowed_sort_by[sort_by]} {sort_order}
        LIMIT %s OFFSET %s
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(count_query, params)
            count_row = cur.fetchone()
            total_items = count_row["total_count"] if count_row else 0

            cur.execute(data_query, params + [page_size, offset])
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
                "qualityScore": {
                    "total": row["total_score"],
                    "rank": row["rank"],
                    "evaluationStatus": row["evaluation_status"],
                    "measuredAt": row["measured_at"].isoformat() if row["measured_at"] else None,
                },
            }
        )

    total_pages = (total_items + page_size - 1) // page_size if total_items > 0 else 0

    return {
        "items": items,
        "pagination": {
            "page": page,
            "pageSize": page_size,
            "totalItems": total_items,
            "totalPages": total_pages,
        },
    }
