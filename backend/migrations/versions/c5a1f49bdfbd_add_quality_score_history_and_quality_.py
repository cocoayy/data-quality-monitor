"""add quality_score_history and quality_score_reasons tables

Revision ID: 0003_add_history_reasons
Revises: 0002_add_resources_snapshots
Create Date: 2026-03-26
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "0003_add_history_reasons"
down_revision: Union[str, None] = "0002_add_resources_snapshots"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "quality_score_history",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("dataset_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("measured_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("measured_date", sa.Date(), nullable=False),
        sa.Column("evaluation_status", sa.String(length=20), nullable=False),
        sa.Column("completeness_score", sa.Integer(), nullable=True),
        sa.Column("freshness_score", sa.Integer(), nullable=True),
        sa.Column("accessibility_score", sa.Integer(), nullable=True),
        sa.Column("format_quality_score", sa.Integer(), nullable=True),
        sa.Column("total_score", sa.Integer(), nullable=True),
        sa.Column("rank", sa.String(length=2), nullable=True),
        sa.Column("detail_json", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["dataset_id"], ["datasets.id"], name="fk_quality_score_history_dataset", ondelete="CASCADE"),
        sa.CheckConstraint(
            "evaluation_status IN ('success', 'partial', 'failed', 'unevaluable')",
            name="chk_quality_score_history_evaluation_status",
        ),
        sa.CheckConstraint(
            "completeness_score IS NULL OR completeness_score BETWEEN 0 AND 100",
            name="chk_quality_score_history_completeness_score",
        ),
        sa.CheckConstraint(
            "freshness_score IS NULL OR freshness_score BETWEEN 0 AND 100",
            name="chk_quality_score_history_freshness_score",
        ),
        sa.CheckConstraint(
            "accessibility_score IS NULL OR accessibility_score BETWEEN 0 AND 100",
            name="chk_quality_score_history_accessibility_score",
        ),
        sa.CheckConstraint(
            "format_quality_score IS NULL OR format_quality_score BETWEEN 0 AND 100",
            name="chk_quality_score_history_format_quality_score",
        ),
        sa.CheckConstraint(
            "total_score IS NULL OR total_score BETWEEN 0 AND 100",
            name="chk_quality_score_history_total_score",
        ),
        sa.CheckConstraint(
            "rank IS NULL OR rank IN ('A', 'B', 'C', 'D', 'E')",
            name="chk_quality_score_history_rank",
        ),
    )

    op.create_index(
        "uq_quality_score_history_dataset_measured_date",
        "quality_score_history",
        ["dataset_id", "measured_date"],
        unique=True,
    )

    op.create_index(
        "idx_quality_score_history_dataset_measured_at",
        "quality_score_history",
        ["dataset_id", "measured_at"],
        unique=False,
    )

    op.create_index(
        "idx_quality_score_history_measured_date",
        "quality_score_history",
        ["measured_date"],
        unique=False,
    )

    op.create_index(
        "idx_quality_score_history_total_score",
        "quality_score_history",
        ["total_score"],
        unique=False,
    )

    op.create_table(
        "quality_score_reasons",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("dataset_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("measured_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("metric_type", sa.String(length=50), nullable=False),
        sa.Column("reason_code", sa.String(length=100), nullable=False),
        sa.Column("severity", sa.String(length=20), nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("detail_json", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["dataset_id"], ["datasets.id"], name="fk_quality_score_reasons_dataset", ondelete="CASCADE"),
        sa.CheckConstraint(
            "metric_type IN ('completeness', 'freshness', 'accessibility', 'format_quality', 'total')",
            name="chk_quality_score_reasons_metric_type",
        ),
        sa.CheckConstraint(
            "severity IN ('info', 'warning', 'critical')",
            name="chk_quality_score_reasons_severity",
        ),
    )

    op.create_index(
        "idx_quality_score_reasons_dataset_measured_at",
        "quality_score_reasons",
        ["dataset_id", "measured_at"],
        unique=False,
    )

    op.create_index(
        "idx_quality_score_reasons_metric_type",
        "quality_score_reasons",
        ["metric_type"],
        unique=False,
    )

    op.create_index(
        "idx_quality_score_reasons_reason_code",
        "quality_score_reasons",
        ["reason_code"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("idx_quality_score_reasons_reason_code", table_name="quality_score_reasons")
    op.drop_index("idx_quality_score_reasons_metric_type", table_name="quality_score_reasons")
    op.drop_index("idx_quality_score_reasons_dataset_measured_at", table_name="quality_score_reasons")
    op.drop_table("quality_score_reasons")

    op.drop_index("idx_quality_score_history_total_score", table_name="quality_score_history")
    op.drop_index("idx_quality_score_history_measured_date", table_name="quality_score_history")
    op.drop_index("idx_quality_score_history_dataset_measured_at", table_name="quality_score_history")
    op.drop_index("uq_quality_score_history_dataset_measured_date", table_name="quality_score_history")
    op.drop_table("quality_score_history")