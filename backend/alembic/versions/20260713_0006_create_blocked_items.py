"""create blocked items table

Revision ID: 20260713_0006
Revises: 20260713_0005
Create Date: 2026-07-13
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "20260713_0006"
down_revision: str | None = "20260713_0005"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "blocked_items",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("blocked_item_id", sa.String(length=64), nullable=False),
        sa.Column("user_id", sa.String(length=64), nullable=False),
        sa.Column("analysis_request_id", sa.String(length=64), nullable=True),
        sa.Column("client_content_id", sa.String(length=100), nullable=True),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("categories", sa.JSON(), nullable=False),
        sa.Column("related_topics", sa.JSON(), nullable=False),
        sa.Column("source_url", sa.Text(), nullable=False),
        sa.Column("selector", sa.Text(), nullable=True),
        sa.Column("position_text", sa.Text(), nullable=True),
        sa.Column("found_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("saved_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.user_id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "user_id",
            "source_url",
            "selector",
            name="uk_blocked_items_user_source_selector",
        ),
    )
    op.create_index(
        "ix_blocked_items_blocked_item_id",
        "blocked_items",
        ["blocked_item_id"],
        unique=True,
    )
    op.create_index(
        "ix_blocked_items_user_id",
        "blocked_items",
        ["user_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_blocked_items_user_id", table_name="blocked_items")
    op.drop_index("ix_blocked_items_blocked_item_id", table_name="blocked_items")
    op.drop_table("blocked_items")
