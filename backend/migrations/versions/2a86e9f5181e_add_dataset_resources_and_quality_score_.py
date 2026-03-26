"""add dataset_resources and quality_score_snapshots tables

Revision ID: 0002_add_resources_snapshots
Revises: 0001_create_orgs_datasets
Create Date: 2026-03-26
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "0002_add_resources_snapshots"
down_revision: Union[str, None] = "0001_create_orgs_datasets"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "dataset_resources",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("dataset_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("external_key", sa.String(length=255), nullable=True),
        sa.Column("resource_type", sa.String(length=50), nullable=False),
        sa.Column("format", sa.String(length=50), nullable=True),
        sa.Column("resource_url", sa.Text(), nullable=True),
        sa.Column("api_endpoint", sa.Text(), nullable=True),
        sa.Column("is_monitoring_target", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("latest_http_status", sa.Integer(), nullable=True),
        sa.Column("latest_response_time_ms", sa.Integer(), nullable=True),
        sa.Column("latest_checked_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("metadata_json", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["dataset_id"], ["datasets.id"], name="fk_dataset_resources_dataset", ondelete="CASCADE"),
        sa.CheckConstraint(
            "resource_type IN ('file', 'api', 'page')",
            name="chk_dataset_resources_resource_type",
        ),
        sa.CheckConstraint(
            "latest_http_status IS NULL OR (latest_http_status >= 100 AND latest_http_status <= 599)",
            name="chk_dataset_resources_http_status",
        ),
        sa.CheckConstraint(
            "latest_response_time_ms IS NULL OR latest_response_time_ms >= 0",
            name="chk_dataset_resources_response_time_ms",
        ),
    )

    op.create_index(
        "uq_dataset_resources_dataset_external_key",
        "dataset_resources",
        ["dataset_id", "external_key"],
        unique=True,
        postgresql_where=sa.text("external_key IS NOT NULL"),
    )

    op.create_index(
        "idx_dataset_resources_dataset_id",
        "dataset_resources",
        ["dataset_id"],
        unique=False,
    )

    op.create_index(
        "idx_dataset_resources_monitoring_target",
        "dataset_resources",
        ["is_monitoring_target"],
        unique=False,
        postgresql_where=sa.text("is_monitoring_target = true"),
    )

    op.create_index(
        "idx_dataset_resources_format",
        "dataset_resources",
        ["format"],
        unique=False,
    )

    op.create_index(
        "idx_dataset_resources_latest_checked_at",
        "dataset_resources",
        ["latest_checked_at"],
        unique=False,
    )

    op.create_table(
        "quality_score_snapshots",
        sa.Column("dataset_id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("measured_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("evaluation_status", sa.String(length=20), nullable=False),
        sa.Column("completeness_score", sa.Integer(), nullable=True),
        sa.Column("freshness_score", sa.Integer(), nullable=True),
        sa.Column("accessibility_score", sa.Integer(), nullable=True),
        sa.Column("format_quality_score", sa.Integer(), nullable=True),
        sa.Column("total_score", sa.Integer(), nullable=True),
        sa.Column("rank", sa.String(length=2), nullable=True),
        sa.Column("detail_json", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["dataset_id"], ["datasets.id"], name="fk_quality_score_snapshots_dataset", ondelete="CASCADE"),
        sa.CheckConstraint(
            "evaluation_status IN ('success', 'partial', 'failed', 'unevaluable')",
            name="chk_quality_score_snapshots_evaluation_status",
        ),
        sa.CheckConstraint(
            "completeness_score IS NULL OR completeness_score BETWEEN 0 AND 100",
            name="chk_quality_score_snapshots_completeness_score",
        ),
        sa.CheckConstraint(
            "freshness_score IS NULL OR freshness_score BETWEEN 0 AND 100",
            name="chk_quality_score_snapshots_freshness_score",
        ),
        sa.CheckConstraint(
            "accessibility_score IS NULL OR accessibility_score BETWEEN 0 AND 100",
            name="chk_quality_score_snapshots_accessibility_score",
        ),
        sa.CheckConstraint(
            "format_quality_score IS NULL OR format_quality_score BETWEEN 0 AND 100",
            name="chk_quality_score_snapshots_format_quality_score",
        ),
        sa.CheckConstraint(
            "total_score IS NULL OR total_score BETWEEN 0 AND 100",
            name="chk_quality_score_snapshots_total_score",
        ),
        sa.CheckConstraint(
            "rank IS NULL OR rank IN ('A', 'B', 'C', 'D', 'E')",
            name="chk_quality_score_snapshots_rank",
        ),
    )

    op.create_index(
        "idx_quality_score_snapshots_measured_at",
        "quality_score_snapshots",
        ["measured_at"],
        unique=False,
    )

    op.create_index(
        "idx_quality_score_snapshots_total_score",
        "quality_score_snapshots",
        ["total_score"],
        unique=False,
    )

    op.create_index(
        "idx_quality_score_snapshots_rank",
        "quality_score_snapshots",
        ["rank"],
        unique=False,
    )

    op.create_index(
        "idx_quality_score_snapshots_evaluation_status",
        "quality_score_snapshots",
        ["evaluation_status"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("idx_quality_score_snapshots_evaluation_status", table_name="quality_score_snapshots")
    op.drop_index("idx_quality_score_snapshots_rank", table_name="quality_score_snapshots")
    op.drop_index("idx_quality_score_snapshots_total_score", table_name="quality_score_snapshots")
    op.drop_index("idx_quality_score_snapshots_measured_at", table_name="quality_score_snapshots")
    op.drop_table("quality_score_snapshots")

    op.drop_index("idx_dataset_resources_latest_checked_at", table_name="dataset_resources")
    op.drop_index("idx_dataset_resources_format", table_name="dataset_resources")
    op.drop_index("idx_dataset_resources_monitoring_target", table_name="dataset_resources")
    op.drop_index("idx_dataset_resources_dataset_id", table_name="dataset_resources")
    op.drop_index("uq_dataset_resources_dataset_external_key", table_name="dataset_resources")
    op.drop_table("dataset_resources")