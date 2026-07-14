"""add interest target to blocked items

Revision ID: 20260714_0016
Revises: 20260714_0015
Create Date: 2026-07-14
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "20260714_0016"
down_revision: str | None = "20260714_0015"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "blocked_items",
        sa.Column("interest_target_id", sa.String(length=64), nullable=True),
    )
    op.create_index(
        op.f("ix_blocked_items_interest_target_id"),
        "blocked_items",
        ["interest_target_id"],
        unique=False,
    )
    op.create_foreign_key(
        "fk_blocked_items_interest_target_id",
        "blocked_items",
        "interest_targets",
        ["interest_target_id"],
        ["interest_target_id"],
    )
    op.drop_constraint(
        "uk_blocked_items_user_source_selector",
        "blocked_items",
        type_="unique",
    )
    op.create_unique_constraint(
        "uk_blocked_items_user_target_source_selector",
        "blocked_items",
        ["user_id", "interest_target_id", "source_url", "selector"],
    )


def downgrade() -> None:
    op.drop_constraint(
        "uk_blocked_items_user_target_source_selector",
        "blocked_items",
        type_="unique",
    )
    op.create_unique_constraint(
        "uk_blocked_items_user_source_selector",
        "blocked_items",
        ["user_id", "source_url", "selector"],
    )
    op.drop_constraint(
        "fk_blocked_items_interest_target_id",
        "blocked_items",
        type_="foreignkey",
    )
    op.drop_index(
        op.f("ix_blocked_items_interest_target_id"),
        table_name="blocked_items",
    )
    op.drop_column("blocked_items", "interest_target_id")
