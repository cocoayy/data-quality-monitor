from fastapi import APIRouter, Query

from app.db.connection import get_connection

router = APIRouter(prefix="/api/v1/dashboard", tags=["dashboard"])


@router.get("/summary")
def get_dashboard_summary(
    organization_id: str | None = Query(None),
) -> dict:
    dataset_where = ""
    score_where = ""
    alert_where = ""
    params: list[str] = []

    if organization_id:
        dataset_where = "WHERE d.organization_id = %s"
        score_where = "WHERE d.organization_id = %s"
        alert_where = "WHERE d.organization_id = %s"
        params = [organization_id]

    datasets_query = f"""
        SELECT COUNT(*) AS total_datasets
        FROM datasets d
        {dataset_where}
    """

    evaluated_query = f"""
        SELECT
            COUNT(*) FILTER (WHERE q.evaluation_status IN ('success', 'partial')) AS evaluated_datasets,
            COUNT(*) FILTER (WHERE q.evaluation_status = 'unevaluable') AS unevaluable_datasets,
            AVG(q.total_score) AS average_total_score
        FROM quality_score_snapshots q
        JOIN datasets d
            ON d.id = q.dataset_id
        {score_where}
    """

    rank_distribution_query = f"""
        SELECT
            COUNT(*) FILTER (WHERE q.rank = 'A') AS rank_a,
            COUNT(*) FILTER (WHERE q.rank = 'B') AS rank_b,
            COUNT(*) FILTER (WHERE q.rank = 'C') AS rank_c,
            COUNT(*) FILTER (WHERE q.rank = 'D') AS rank_d,
            COUNT(*) FILTER (WHERE q.rank = 'E') AS rank_e
        FROM quality_score_snapshots q
        JOIN datasets d
            ON d.id = q.dataset_id
        {score_where}
    """

    alert_query = f"""
        SELECT
            COUNT(*) FILTER (WHERE a.severity = 'critical') AS critical_alerts,
            COUNT(*) FILTER (WHERE a.severity = 'warning') AS warning_alerts
        FROM alert_events a
        JOIN datasets d
            ON d.id = a.dataset_id
        {alert_where}
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(datasets_query, params)
            datasets_row = cur.fetchone()

            cur.execute(evaluated_query, params)
            evaluated_row = cur.fetchone()

            cur.execute(rank_distribution_query, params)
            rank_row = cur.fetchone()

            cur.execute(alert_query, params)
            alert_row = cur.fetchone()

    return {
        "measuredDate": None,
        "summary": {
            "totalDatasets": datasets_row["total_datasets"] or 0,
            "evaluatedDatasets": evaluated_row["evaluated_datasets"] or 0,
            "unevaluableDatasets": evaluated_row["unevaluable_datasets"] or 0,
            "averageTotalScore": float(evaluated_row["average_total_score"]) if evaluated_row["average_total_score"] is not None else 0.0,
            "rankDistribution": {
                "A": rank_row["rank_a"] or 0,
                "B": rank_row["rank_b"] or 0,
                "C": rank_row["rank_c"] or 0,
                "D": rank_row["rank_d"] or 0,
                "E": rank_row["rank_e"] or 0,
            },
            "criticalAlerts": alert_row["critical_alerts"] or 0,
            "warningAlerts": alert_row["warning_alerts"] or 0,
        },
    }


@router.get("/history")
def get_dashboard_history(
    organization_id: str | None = Query(None),
) -> dict:
    where_sql = ""
    params: list[str] = []

    if organization_id:
        where_sql = "WHERE d.organization_id = %s"
        params.append(organization_id)

    query = f"""
        SELECT
            h.measured_date,
            ROUND(AVG(h.total_score)::numeric, 1) AS average_total_score,
            COUNT(*) FILTER (WHERE h.rank = 'A') AS rank_a,
            COUNT(*) FILTER (WHERE h.rank = 'B') AS rank_b,
            COUNT(*) FILTER (WHERE h.rank = 'C') AS rank_c,
            COUNT(*) FILTER (WHERE h.rank = 'D') AS rank_d,
            COUNT(*) FILTER (WHERE h.rank = 'E') AS rank_e
        FROM quality_score_history h
        JOIN datasets d
            ON d.id = h.dataset_id
        {where_sql}
        GROUP BY h.measured_date
        ORDER BY h.measured_date ASC
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params)
            rows = cur.fetchall()

    items = []
    for row in rows:
        items.append(
            {
                "measuredDate": row["measured_date"].isoformat(),
                "averageTotalScore": float(row["average_total_score"]) if row["average_total_score"] is not None else 0.0,
                "rankDistribution": {
                    "A": row["rank_a"] or 0,
                    "B": row["rank_b"] or 0,
                    "C": row["rank_c"] or 0,
                    "D": row["rank_d"] or 0,
                    "E": row["rank_e"] or 0,
                },
            }
        )

    return {"items": items}
