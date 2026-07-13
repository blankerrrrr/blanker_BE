"""create analysis tables

Revision ID: 20260713_0004
Revises: 20260713_0003
Create Date: 2026-07-13
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "20260713_0004"
down_revision: str | None = "20260713_0003"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "analysis_requests",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("analysis_request_id", sa.String(length=64), nullable=False),
        sa.Column("user_id", sa.String(length=64), nullable=False),
        sa.Column("page_url", sa.Text(), nullable=False),
        sa.Column("page_title", sa.String(length=500), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.user_id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_analysis_requests_analysis_request_id",
        "analysis_requests",
        ["analysis_request_id"],
        unique=True,
    )
    op.create_index(
        "ix_analysis_requests_user_id",
        "analysis_requests",
        ["user_id"],
        unique=False,
    )

    op.create_table(
        "analysis_contents",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("analysis_content_id", sa.String(length=64), nullable=False),
        sa.Column("analysis_request_id", sa.String(length=64), nullable=False),
        sa.Column("client_content_id", sa.String(length=100), nullable=False),
        sa.Column("unit_type", sa.String(length=20), nullable=False),
        sa.Column("text", sa.Text(), nullable=True),
        sa.Column("image_url", sa.Text(), nullable=True),
        sa.Column("alt_text", sa.Text(), nullable=True),
        sa.Column("context_text", sa.Text(), nullable=True),
        sa.Column("selector", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["analysis_request_id"],
            ["analysis_requests.analysis_request_id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("analysis_content_id"),
        sa.UniqueConstraint(
            "analysis_request_id",
            "client_content_id",
            name="uk_analysis_contents_request_client_id",
        ),
    )
    op.create_index(
        "ix_analysis_contents_analysis_request_id",
        "analysis_contents",
        ["analysis_request_id"],
        unique=False,
    )

    op.create_table(
        "analysis_results",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("analysis_result_id", sa.String(length=64), nullable=False),
        sa.Column("analysis_content_id", sa.String(length=64), nullable=False),
        sa.Column("categories", sa.JSON(), nullable=False),
        sa.Column("risk_level", sa.String(length=20), nullable=False),
        sa.Column("relevance_level", sa.String(length=20), nullable=False),
        sa.Column("should_block", sa.Boolean(), nullable=False),
        sa.Column("block_reason", sa.Text(), nullable=True),
        sa.Column("related_topics", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["analysis_content_id"],
            ["analysis_contents.analysis_content_id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("analysis_content_id"),
    )
    op.create_index(
        "ix_analysis_results_analysis_result_id",
        "analysis_results",
        ["analysis_result_id"],
        unique=True,
    )


def downgrade() -> None:
    op.drop_index(
        "ix_analysis_results_analysis_result_id",
        table_name="analysis_results",
    )
    op.drop_table("analysis_results")
    op.drop_index(
        "ix_analysis_contents_analysis_request_id",
        table_name="analysis_contents",
    )
    op.drop_table("analysis_contents")
    op.drop_index(
        "ix_analysis_requests_user_id",
        table_name="analysis_requests",
    )
    op.drop_index(
        "ix_analysis_requests_analysis_request_id",
        table_name="analysis_requests",
    )
    op.drop_table("analysis_requests")
