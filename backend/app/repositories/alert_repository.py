from psycopg import Connection


class AlertRepository:
    def __init__(self, conn: Connection) -> None:
        self.conn = conn

    def list_alerts(
        self,
        dataset_id: str | None = None,
        organization_id: str | None = None,
        alert_type: str | None = None,
        severity: str | None = None,
        keyword: str | None = None,
    ):
        where_clauses: list[str] = []
        params: list[object] = []

        if dataset_id:
            where_clauses.append("a.dataset_id = %s")
            params.append(dataset_id)

        if organization_id:
            where_clauses.append("d.organization_id = %s")
            params.append(organization_id)

        if alert_type:
            where_clauses.append("a.alert_type = %s")
            params.append(alert_type)

        if severity:
            where_clauses.append("a.severity = %s")
            params.append(severity)

        if keyword:
            where_clauses.append("(a.message ILIKE %s OR d.title ILIKE %s)")
            keyword_like = f"%{keyword}%"
            params.extend([keyword_like, keyword_like])

        where_sql = ""
        if where_clauses:
            where_sql = "WHERE " + " AND ".join(where_clauses)

        query = f"""
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
            JOIN datasets d ON d.id = a.dataset_id
            {where_sql}
            ORDER BY a.measured_at DESC
        """

        with self.conn.cursor() as cur:
            cur.execute(query, params)
            return cur.fetchall()

    def get_alert_by_id(self, alert_id: str):
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

        with self.conn.cursor() as cur:
            cur.execute(query, (alert_id,))
            return cur.fetchone()
