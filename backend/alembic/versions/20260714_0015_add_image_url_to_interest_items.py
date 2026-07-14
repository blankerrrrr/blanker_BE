"""add image url to interest items

Revision ID: 20260714_0015
Revises: 20260714_0014
Create Date: 2026-07-14
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "20260714_0015"
down_revision: str | None = "20260714_0014"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "interest_items",
        sa.Column("image_url", sa.String(length=1000), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("interest_items", "image_url")
