from fastapi import APIRouter

from app.db.connection import get_connection

router = APIRouter(prefix="/api/v1/dashboard", tags=["dashboard"])


@router.get("/summary")
def get_dashboard_summary() -> dict:
    datasets_query = """
        SELECT COUNT(*) AS total_datasets
        FROM datasets
    """

    evaluated_query = """
        SELECT
            COUNT(*) FILTER (WHERE evaluation_status IN ('success', 'partial')) AS evaluated_datasets,
            COUNT(*) FILTER (WHERE evaluation_status = 'unevaluable') AS unevaluable_datasets,
            AVG(total_score) AS average_total_score
        FROM quality_score_snapshots
    """

    rank_distribution_query = """
        SELECT
            COUNT(*) FILTER (WHERE rank = 'A') AS rank_a,
            COUNT(*) FILTER (WHERE rank = 'B') AS rank_b,
            COUNT(*) FILTER (WHERE rank = 'C') AS rank_c,
            COUNT(*) FILTER (WHERE rank = 'D') AS rank_d,
            COUNT(*) FILTER (WHERE rank = 'E') AS rank_e
        FROM quality_score_snapshots
    """

    alert_query = """
        SELECT
            COUNT(*) FILTER (WHERE severity = 'critical') AS critical_alerts,
            COUNT(*) FILTER (WHERE severity = 'warning') AS warning_alerts
        FROM alert_events
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(datasets_query)
            datasets_row = cur.fetchone()

            cur.execute(evaluated_query)
            evaluated_row = cur.fetchone()

            cur.execute(rank_distribution_query)
            rank_row = cur.fetchone()

            cur.execute(alert_query)
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