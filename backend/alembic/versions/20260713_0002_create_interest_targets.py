"""create interest targets table

Revision ID: 20260713_0002
Revises: 20260713_0001
Create Date: 2026-07-13
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "20260713_0002"
down_revision: str | None = "20260713_0001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "interest_targets",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("interest_target_id", sa.String(length=64), nullable=False),
        sa.Column("user_id", sa.String(length=64), nullable=False),
        sa.Column("type", sa.String(length=20), nullable=False),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("aliases", sa.JSON(), nullable=False),
        sa.Column("keywords", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.user_id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "user_id",
            "type",
            "name",
            name="uk_interest_targets_user_type_name",
        ),
    )
    op.create_index(
        "ix_interest_targets_interest_target_id",
        "interest_targets",
        ["interest_target_id"],
        unique=True,
    )
    op.create_index(
        "ix_interest_targets_user_id",
        "interest_targets",
        ["user_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_interest_targets_user_id", table_name="interest_targets")
    op.drop_index(
        "ix_interest_targets_interest_target_id",
        table_name="interest_targets",
    )
    op.drop_table("interest_targets")
