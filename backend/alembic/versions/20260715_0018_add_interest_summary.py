"""add interest summary

Revision ID: 20260715_0018
Revises: 20260714_0017
Create Date: 2026-07-15
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "20260715_0018"
down_revision: str | None = "20260714_0017"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "interests",
        sa.Column("summary", sa.String(length=250), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("interests", "summary")
