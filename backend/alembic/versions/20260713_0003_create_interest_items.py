"""create interest item tables

Revision ID: 20260713_0003
Revises: 20260713_0002
Create Date: 2026-07-13
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "20260713_0003"
down_revision: str | None = "20260713_0002"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "interest_item_groups",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("group_id", sa.String(length=64), nullable=False),
        sa.Column("user_id", sa.String(length=64), nullable=False),
        sa.Column("representative_item_id", sa.String(length=64), nullable=True),
        sa.Column("title", sa.String(length=500), nullable=False),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("related_topics", sa.JSON(), nullable=False),
        sa.Column("duplicate_reason", sa.Text(), nullable=True),
        sa.Column("source_count", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.user_id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_interest_item_groups_group_id",
        "interest_item_groups",
        ["group_id"],
        unique=True,
    )
    op.create_index(
        "ix_interest_item_groups_user_id",
        "interest_item_groups",
        ["user_id"],
        unique=False,
    )

    op.create_table(
        "interest_items",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("interest_item_id", sa.String(length=64), nullable=False),
        sa.Column("user_id", sa.String(length=64), nullable=False),
        sa.Column("group_id", sa.String(length=64), nullable=False),
        sa.Column("title", sa.String(length=500), nullable=False),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("content_text", sa.Text(), nullable=True),
        sa.Column("related_topics", sa.JSON(), nullable=False),
        sa.Column("source_url", sa.Text(), nullable=False),
        sa.Column("selector", sa.Text(), nullable=True),
        sa.Column("duplicate_score", sa.Numeric(5, 4), nullable=True),
        sa.Column("discovered_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["group_id"], ["interest_item_groups.group_id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.user_id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "user_id",
            "source_url",
            name="uk_interest_items_user_source",
        ),
    )
    op.create_index(
        "ix_interest_items_group_id",
        "interest_items",
        ["group_id"],
        unique=False,
    )
    op.create_index(
        "ix_interest_items_interest_item_id",
        "interest_items",
        ["interest_item_id"],
        unique=True,
    )
    op.create_index(
        "ix_interest_items_user_id",
        "interest_items",
        ["user_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_interest_items_user_id", table_name="interest_items")
    op.drop_index("ix_interest_items_interest_item_id", table_name="interest_items")
    op.drop_index("ix_interest_items_group_id", table_name="interest_items")
    op.drop_table("interest_items")
    op.drop_index(
        "ix_interest_item_groups_user_id",
        table_name="interest_item_groups",
    )
    op.drop_index(
        "ix_interest_item_groups_group_id",
        table_name="interest_item_groups",
    )
    op.drop_table("interest_item_groups")
