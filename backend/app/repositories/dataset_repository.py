from psycopg import Connection


class DatasetRepository:
    def __init__(self, conn: Connection) -> None:
        self.conn = conn

    def list_datasets(
        self,
        page: int,
        page_size: int,
        organization_id: str | None = None,
        source_type: str | None = None,
        monitoring_enabled: bool | None = None,
        evaluation_status: str | None = None,
        rank: str | None = None,
        min_total_score: int | None = None,
        max_total_score: int | None = None,
        keyword: str | None = None,
        excluded_from_scoring: bool | None = None,
        has_alert: bool | None = None,
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
            raise ValueError("invalid sort_by")

        if sort_order not in {"asc", "desc"}:
            raise ValueError("invalid sort_order")

        where_clauses: list[str] = []
        params: list[object] = []

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

        if excluded_from_scoring is not None:
            where_clauses.append("d.excluded_from_scoring = %s")
            params.append(excluded_from_scoring)

        if keyword:
            where_clauses.append("(d.title ILIKE %s OR d.description ILIKE %s)")
            keyword_like = f"%{keyword}%"
            params.extend([keyword_like, keyword_like])

        if has_alert is True:
            where_clauses.append(
                "EXISTS (SELECT 1 FROM alert_events a WHERE a.dataset_id = d.id)"
            )
        elif has_alert is False:
            where_clauses.append(
                "NOT EXISTS (SELECT 1 FROM alert_events a WHERE a.dataset_id = d.id)"
            )

        where_sql = ""
        if where_clauses:
            where_sql = "WHERE " + " AND ".join(where_clauses)

        offset = (page - 1) * page_size

        count_query = f"""
            SELECT COUNT(*) AS total_count
            FROM datasets d
            LEFT JOIN quality_score_snapshots q ON q.dataset_id = d.id
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
            LEFT JOIN quality_score_snapshots q ON q.dataset_id = d.id
            {where_sql}
            ORDER BY {allowed_sort_by[sort_by]} {sort_order}
            LIMIT %s OFFSET %s
        """

        with self.conn.cursor() as cur:
            cur.execute(count_query, params)
            count_row = cur.fetchone()
            total_items = count_row["total_count"] if count_row else 0

            cur.execute(data_query, params + [page_size, offset])
            rows = cur.fetchall()

        return {
            "rows": rows,
            "total_items": total_items,
            "page": page,
            "page_size": page_size,
        }

    def get_dataset_by_id(self, dataset_id: str):
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
            JOIN organizations o ON o.id = d.organization_id
            LEFT JOIN quality_score_snapshots q ON q.dataset_id = d.id
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

        with self.conn.cursor() as cur:
            cur.execute(dataset_query, (dataset_id,))
            dataset = cur.fetchone()

            if not dataset:
                return None

            cur.execute(resources_query, (dataset_id,))
            resources = cur.fetchall()

        return {
            "dataset": dataset,
            "resources": resources,
        }

    def patch_monitoring_settings(
        self,
        dataset_id: str,
        monitoring_enabled: bool | None,
        excluded_from_scoring: bool | None,
        expected_update_cycle: str | None,
    ):
        update_fields: list[str] = []
        params: list[object] = []

        if monitoring_enabled is not None:
            update_fields.append("monitoring_enabled = %s")
            params.append(monitoring_enabled)

        if excluded_from_scoring is not None:
            update_fields.append("excluded_from_scoring = %s")
            params.append(excluded_from_scoring)

        if expected_update_cycle is not None:
            update_fields.append("expected_update_cycle = %s")
            params.append(expected_update_cycle)

        if not update_fields:
            raise ValueError("no fields to update")

        update_fields.append("updated_at = now()")
        params.append(dataset_id)

        query = f"""
            UPDATE datasets
            SET {", ".join(update_fields)}
            WHERE id = %s
            RETURNING
                id,
                monitoring_enabled,
                excluded_from_scoring,
                expected_update_cycle,
                updated_at
        """

        with self.conn.cursor() as cur:
            cur.execute(query, params)
            row = cur.fetchone()
            self.conn.commit()

        return row
