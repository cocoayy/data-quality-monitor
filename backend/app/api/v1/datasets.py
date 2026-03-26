from fastapi import APIRouter, HTTPException

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
            d.updated_at,
            q.total_score,
            q.rank,
            q.evaluation_status,
            q.measured_at
        FROM datasets d
        LEFT JOIN quality_score_snapshots q
            ON q.dataset_id = d.id
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
                "qualityScore": {
                    "total": row["total_score"],
                    "rank": row["rank"],
                    "evaluationStatus": row["evaluation_status"],
                    "measuredAt": row["measured_at"].isoformat() if row["measured_at"] else None,
                },
            }
        )

    return {"items": items}

@router.get("/{dataset_id}")
def get_dataset(dataset_id: str) -> dict:
    dataset_query = """
        SELECT
            d.id,
            d.organization_id,
            o.name AS organization_name,
            d.source_type,
            d.title,
            d.description,
            d.license,
            d.category,
            d.tags,
            d.last_updated,
            d.expected_update_cycle,
            d.monitoring_enabled,
            d.excluded_from_scoring,
            d.created_at,
            d.updated_at,
            q.completeness_score,
            q.freshness_score,
            q.accessibility_score,
            q.format_quality_score,
            q.total_score,
            q.rank,
            q.evaluation_status,
            q.measured_at
        FROM datasets d
        JOIN organizations o
            ON o.id = d.organization_id
        LEFT JOIN quality_score_snapshots q
            ON q.dataset_id = d.id
        WHERE d.id = %s
    """

    resources_query = """
        SELECT
            r.id,
            r.resource_type,
            r.format,
            r.resource_url,
            r.api_endpoint,
            r.is_monitoring_target,
            r.latest_http_status,
            r.latest_response_time_ms,
            r.latest_checked_at
        FROM dataset_resources r
        WHERE r.dataset_id = %s
        ORDER BY r.created_at ASC
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(dataset_query, (dataset_id,))
            dataset = cur.fetchone()

            if not dataset:
                raise HTTPException(status_code=404, detail="dataset not found")

            cur.execute(resources_query, (dataset_id,))
            resources = cur.fetchall()

    resource_items = []
    for resource in resources:
        resource_items.append(
            {
                "resourceId": str(resource["id"]),
                "resourceType": resource["resource_type"],
                "format": resource["format"],
                "resourceUrl": resource["resource_url"],
                "apiEndpoint": resource["api_endpoint"],
                "isMonitoringTarget": resource["is_monitoring_target"],
                "latestHttpStatus": resource["latest_http_status"],
                "latestResponseTimeMs": resource["latest_response_time_ms"],
                "latestCheckedAt": resource["latest_checked_at"].isoformat() if resource["latest_checked_at"] else None,
            }
        )

    return {
        "datasetId": str(dataset["id"]),
        "organization": {
            "organizationId": str(dataset["organization_id"]),
            "name": dataset["organization_name"],
        },
        "sourceType": dataset["source_type"],
        "title": dataset["title"],
        "description": dataset["description"],
        "license": dataset["license"],
        "category": dataset["category"],
        "tags": dataset["tags"],
        "lastUpdated": dataset["last_updated"].isoformat() if dataset["last_updated"] else None,
        "expectedUpdateCycle": dataset["expected_update_cycle"],
        "monitoringEnabled": dataset["monitoring_enabled"],
        "excludedFromScoring": dataset["excluded_from_scoring"],
        "createdAt": dataset["created_at"].isoformat() if dataset["created_at"] else None,
        "updatedAt": dataset["updated_at"].isoformat() if dataset["updated_at"] else None,
        "latestQualityScore": {
            "completeness": dataset["completeness_score"],
            "freshness": dataset["freshness_score"],
            "accessibility": dataset["accessibility_score"],
            "formatQuality": dataset["format_quality_score"],
            "total": dataset["total_score"],
            "rank": dataset["rank"],
            "evaluationStatus": dataset["evaluation_status"],
            "measuredAt": dataset["measured_at"].isoformat() if dataset["measured_at"] else None,
        },
        "resources": resource_items,
    }