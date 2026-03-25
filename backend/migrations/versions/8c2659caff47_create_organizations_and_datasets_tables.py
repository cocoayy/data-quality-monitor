"""create organizations and datasets tables

Revision ID: 0001_create_orgs_datasets
Revises:
Create Date: 2026-03-25
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "0001_create_orgs_datasets"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "organizations",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("external_key", sa.String(length=255), nullable=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("display_name", sa.String(length=255), nullable=True),
        sa.Column("source_type", sa.String(length=50), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.CheckConstraint(
            "source_type IN ('ckan', 'data_json', 'csv_url', 'api', 'manual')",
            name="chk_organizations_source_type",
        ),
    )

    op.create_index(
        "uq_organizations_external_key",
        "organizations",
        ["external_key"],
        unique=True,
        postgresql_where=sa.text("external_key IS NOT NULL"),
    )

    op.create_index(
        "idx_organizations_source_type",
        "organizations",
        ["source_type"],
        unique=False,
    )

    op.create_index(
        "idx_organizations_is_active",
        "organizations",
        ["is_active"],
        unique=False,
    )

    op.create_table(
        "datasets",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("source_type", sa.String(length=50), nullable=False),
        sa.Column("external_key", sa.String(length=255), nullable=True),
        sa.Column("title", sa.Text(), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("license", sa.String(length=255), nullable=True),
        sa.Column("category", sa.String(length=255), nullable=True),
        sa.Column("tags", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("last_updated", sa.DateTime(timezone=True), nullable=True),
        sa.Column("expected_update_cycle", sa.String(length=50), nullable=True),
        sa.Column("monitoring_enabled", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("excluded_from_scoring", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("metadata_json", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["organization_id"], ["organizations.id"], name="fk_datasets_organization"),
        sa.CheckConstraint(
            "source_type IN ('ckan', 'data_json', 'csv_url', 'api', 'manual')",
            name="chk_datasets_source_type",
        ),
        sa.CheckConstraint(
            "expected_update_cycle IS NULL OR expected_update_cycle IN ('daily', 'weekly', 'monthly', 'quarterly', 'yearly', 'unknown')",
            name="chk_datasets_expected_update_cycle",
        ),
        sa.CheckConstraint(
            "tags IS NULL OR jsonb_typeof(tags) = 'array'",
            name="chk_datasets_tags_is_array",
        ),
    )

    op.create_index(
        "uq_datasets_source_external_key",
        "datasets",
        ["source_type", "external_key"],
        unique=True,
        postgresql_where=sa.text("external_key IS NOT NULL"),
    )

    op.create_index(
        "idx_datasets_organization_id",
        "datasets",
        ["organization_id"],
        unique=False,
    )

    op.create_index(
        "idx_datasets_monitoring_enabled",
        "datasets",
        ["monitoring_enabled"],
        unique=False,
        postgresql_where=sa.text("monitoring_enabled = true"),
    )

    op.create_index(
        "idx_datasets_excluded_from_scoring",
        "datasets",
        ["excluded_from_scoring"],
        unique=False,
    )

    op.create_index(
        "idx_datasets_last_updated",
        "datasets",
        ["last_updated"],
        unique=False,
    )

    op.create_index(
        "idx_datasets_expected_update_cycle",
        "datasets",
        ["expected_update_cycle"],
        unique=False,
    )

    op.create_index(
        "idx_datasets_tags_gin",
        "datasets",
        ["tags"],
        unique=False,
        postgresql_using="gin",
    )


def downgrade() -> None:
    op.drop_index("idx_datasets_tags_gin", table_name="datasets")
    op.drop_index("idx_datasets_expected_update_cycle", table_name="datasets")
    op.drop_index("idx_datasets_last_updated", table_name="datasets")
    op.drop_index("idx_datasets_excluded_from_scoring", table_name="datasets")
    op.drop_index("idx_datasets_monitoring_enabled", table_name="datasets")
    op.drop_index("idx_datasets_organization_id", table_name="datasets")
    op.drop_index("uq_datasets_source_external_key", table_name="datasets")
    op.drop_table("datasets")

    op.drop_index("idx_organizations_is_active", table_name="organizations")
    op.drop_index("idx_organizations_source_type", table_name="organizations")
    op.drop_index("uq_organizations_external_key", table_name="organizations")
    op.drop_table("organizations")