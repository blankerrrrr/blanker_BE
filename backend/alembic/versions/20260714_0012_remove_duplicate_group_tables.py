"""remove duplicate group tables and columns

Revision ID: 20260714_0012
Revises: 20260714_0011
Create Date: 2026-07-14
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "20260714_0012"
down_revision: str | None = "20260714_0011"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # interest_items에서 group_id, duplicate_score 컬럼 제거
    with op.batch_alter_table("interest_items") as batch_op:
        batch_op.drop_index("ix_interest_items_group_id")
        batch_op.drop_column("group_id")
        batch_op.drop_column("duplicate_score")

    # interest_item_groups 테이블 제거
    op.drop_table("interest_item_groups")


def downgrade() -> None:
    op.create_table(
        "interest_item_groups",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("group_id", sa.String(64), nullable=True),
        sa.Column("user_id", sa.String(64), nullable=False),
        sa.Column("representative_item_id", sa.String(64), nullable=True),
        sa.Column("title", sa.String(500), nullable=False),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("related_topics", sa.JSON(), nullable=False),
        sa.Column("duplicate_reason", sa.Text(), nullable=True),
        sa.Column("source_count", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.user_id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("group_id"),
    )
    op.create_index(
        "ix_interest_item_groups_group_id",
        "interest_item_groups",
        ["group_id"],
    )
    op.create_index(
        "ix_interest_item_groups_user_id",
        "interest_item_groups",
        ["user_id"],
    )

    with op.batch_alter_table("interest_items") as batch_op:
        batch_op.add_column(
            sa.Column("group_id", sa.String(64), nullable=False),
        )
        batch_op.add_column(
            sa.Column("duplicate_score", sa.Numeric(5, 4), nullable=True),
        )
        batch_op.create_index("ix_interest_items_group_id", ["group_id"])
        batch_op.create_foreign_key(
            "fk_interest_items_group_id",
            "interest_item_groups",
            ["group_id"],
            ["group_id"],
        )
