from datetime import datetime, timezone
import uuid

from app.db import get_connection
from app.scoring import (
    calc_accessibility,
    calc_completeness,
    calc_format_quality,
    calc_freshness,
    calc_rank,
    calc_total_score,
)


def load_datasets(conn):
    query = """
        SELECT
            id,
            title,
            description,
            license,
            source_type,
            last_updated
        FROM datasets
        WHERE monitoring_enabled = true
    """
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()


def load_resources(conn, dataset_id):
    query = """
        SELECT
            id,
            format,
            latest_http_status,
            latest_response_time_ms
        FROM dataset_resources
        WHERE dataset_id = %s
          AND is_monitoring_target = true
    """
    with conn.cursor() as cur:
        cur.execute(query, (dataset_id,))
        return cur.fetchall()


def upsert_snapshot(conn, dataset_id, measured_at, scores):
    query = """
        INSERT INTO quality_score_snapshots (
            dataset_id,
            measured_at,
            evaluation_status,
            completeness_score,
            freshness_score,
            accessibility_score,
            format_quality_score,
            total_score,
            rank,
            detail_json
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, '{}'::jsonb)
        ON CONFLICT (dataset_id)
        DO UPDATE SET
            measured_at = EXCLUDED.measured_at,
            evaluation_status = EXCLUDED.evaluation_status,
            completeness_score = EXCLUDED.completeness_score,
            freshness_score = EXCLUDED.freshness_score,
            accessibility_score = EXCLUDED.accessibility_score,
            format_quality_score = EXCLUDED.format_quality_score,
            total_score = EXCLUDED.total_score,
            rank = EXCLUDED.rank,
            updated_at = now()
    """

    with conn.cursor() as cur:
        cur.execute(
            query,
            (
                dataset_id,
                measured_at,
                "success",
                scores["completeness"],
                scores["freshness"],
                scores["accessibility"],
                scores["format_quality"],
                scores["total"],
                scores["rank"],
            ),
        )


def upsert_history(conn, dataset_id, measured_at, scores):
    query = """
        INSERT INTO quality_score_history (
            id,
            dataset_id,
            measured_at,
            measured_date,
            evaluation_status,
            completeness_score,
            freshness_score,
            accessibility_score,
            format_quality_score,
            total_score,
            rank,
            detail_json
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '{}'::jsonb)
        ON CONFLICT (dataset_id, measured_date)
        DO UPDATE SET
            measured_at = EXCLUDED.measured_at,
            evaluation_status = EXCLUDED.evaluation_status,
            completeness_score = EXCLUDED.completeness_score,
            freshness_score = EXCLUDED.freshness_score,
            accessibility_score = EXCLUDED.accessibility_score,
            format_quality_score = EXCLUDED.format_quality_score,
            total_score = EXCLUDED.total_score,
            rank = EXCLUDED.rank,
            detail_json = EXCLUDED.detail_json
    """

    with conn.cursor() as cur:
        cur.execute(
            query,
            (
                uuid.uuid4(),
                dataset_id,
                measured_at,
                measured_at.date(),
                "success",
                scores["completeness"],
                scores["freshness"],
                scores["accessibility"],
                scores["format_quality"],
                scores["total"],
                scores["rank"],
            ),
        )


def replace_reasons(conn, dataset_id, measured_at, scores):
    delete_query = """
        DELETE FROM quality_score_reasons
        WHERE dataset_id = %s
    """

    insert_query = """
        INSERT INTO quality_score_reasons (
            id,
            dataset_id,
            measured_at,
            metric_type,
            reason_code,
            severity,
            message,
            detail_json
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s::jsonb)
    """

    items = [
        (
            uuid.uuid4(),
            dataset_id,
            measured_at,
            "completeness",
            "completeness_calculated",
            "info",
            f"completeness score = {scores['completeness']}",
            "{}",
        ),
        (
            uuid.uuid4(),
            dataset_id,
            measured_at,
            "freshness",
            "freshness_calculated",
            "info",
            f"freshness score = {scores['freshness']}",
            "{}",
        ),
        (
            uuid.uuid4(),
            dataset_id,
            measured_at,
            "accessibility",
            "accessibility_calculated",
            "info",
            f"accessibility score = {scores['accessibility']}",
            "{}",
        ),
        (
            uuid.uuid4(),
            dataset_id,
            measured_at,
            "format_quality",
            "format_quality_calculated",
            "info",
            f"format quality score = {scores['format_quality']}",
            "{}",
        ),
    ]

    with conn.cursor() as cur:
        cur.execute(delete_query, (dataset_id,))
        cur.executemany(insert_query, items)


def replace_alerts(conn, dataset_id, measured_at, scores):
    delete_query = """
        DELETE FROM alert_events
        WHERE dataset_id = %s
          AND measured_date = %s
    """

    insert_query = """
        INSERT INTO alert_events (
            id,
            dataset_id,
            measured_at,
            measured_date,
            alert_type,
            severity,
            message,
            payload_json
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s::jsonb)
    """

    items = []

    if scores["total"] < 50:
        items.append(
            (
                uuid.uuid4(),
                dataset_id,
                measured_at,
                measured_at.date(),
                "low_total_score",
                "warning",
                "総合スコアが閾値を下回っています",
                f'{{"totalScore": {scores["total"]}}}',
            )
        )

    if scores["freshness"] == 0:
        items.append(
            (
                uuid.uuid4(),
                dataset_id,
                measured_at,
                measured_at.date(),
                "stale_dataset",
                "critical",
                "更新停止疑いがあります",
                f'{{"freshnessScore": {scores["freshness"]}}}',
            )
        )

    with conn.cursor() as cur:
        cur.execute(delete_query, (dataset_id, measured_at.date()))
        if items:
            cur.executemany(insert_query, items)


def run():
    measured_at = datetime.now(timezone.utc)

    with get_connection() as conn:
        datasets = load_datasets(conn)

        for dataset in datasets:
            resources = load_resources(conn, dataset["id"])

            completeness = calc_completeness(dataset)
            freshness = calc_freshness(dataset)
            accessibility = calc_accessibility(resources)
            format_quality = calc_format_quality(resources)
            total = calc_total_score(
                completeness=completeness,
                freshness=freshness,
                accessibility=accessibility,
                format_quality=format_quality,
            )
            rank = calc_rank(total)

            scores = {
                "completeness": completeness,
                "freshness": freshness,
                "accessibility": accessibility,
                "format_quality": format_quality,
                "total": total,
                "rank": rank,
            }

            upsert_snapshot(conn, dataset["id"], measured_at, scores)
            upsert_history(conn, dataset["id"], measured_at, scores)
            replace_reasons(conn, dataset["id"], measured_at, scores)
            replace_alerts(conn, dataset["id"], measured_at, scores)

        conn.commit()

    print("score batch completed")


if __name__ == "__main__":
    run()
