"""add interest_id to interest_targets

Revision ID: 20260714_0011
Revises: 20260713_0010
Create Date: 2026-07-14
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "20260714_0011"
down_revision: str | None = "20260713_0010"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "interest_targets",
        sa.Column("interest_id", sa.String(length=64), nullable=True),
    )
    op.create_index(
        "ix_interest_targets_interest_id",
        "interest_targets",
        ["interest_id"],
    )


def downgrade() -> None:
    op.drop_index("ix_interest_targets_interest_id", table_name="interest_targets")
    op.drop_column("interest_targets", "interest_id")
