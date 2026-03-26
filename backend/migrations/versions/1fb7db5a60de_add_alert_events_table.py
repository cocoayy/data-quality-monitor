"""add alert_events table

Revision ID: 0004_add_alert_events
Revises: 0003_add_history_reasons
Create Date: 2026-03-26
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "0004_add_alert_events"
down_revision: Union[str, None] = "0003_add_history_reasons"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "alert_events",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("dataset_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("measured_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("measured_date", sa.Date(), nullable=False),
        sa.Column("alert_type", sa.String(length=50), nullable=False),
        sa.Column("severity", sa.String(length=20), nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("payload_json", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["dataset_id"], ["datasets.id"], name="fk_alert_events_dataset", ondelete="CASCADE"),
        sa.CheckConstraint(
            "alert_type IN ('low_total_score', 'stale_dataset', 'inaccessible_dataset', 'sudden_score_drop')",
            name="chk_alert_events_alert_type",
        ),
        sa.CheckConstraint(
            "severity IN ('info', 'warning', 'critical')",
            name="chk_alert_events_severity",
        ),
    )

    op.create_index(
        "uq_alert_events_dataset_type_date",
        "alert_events",
        ["dataset_id", "alert_type", "measured_date"],
        unique=True,
    )

    op.create_index(
        "idx_alert_events_dataset_measured_at",
        "alert_events",
        ["dataset_id", "measured_at"],
        unique=False,
    )

    op.create_index(
        "idx_alert_events_alert_type",
        "alert_events",
        ["alert_type"],
        unique=False,
    )

    op.create_index(
        "idx_alert_events_severity",
        "alert_events",
        ["severity"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("idx_alert_events_severity", table_name="alert_events")
    op.drop_index("idx_alert_events_alert_type", table_name="alert_events")
    op.drop_index("idx_alert_events_dataset_measured_at", table_name="alert_events")
    op.drop_index("uq_alert_events_dataset_type_date", table_name="alert_events")
    op.drop_table("alert_events")