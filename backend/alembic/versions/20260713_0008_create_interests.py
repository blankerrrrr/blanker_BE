"""create interests

Revision ID: 20260713_0008
Revises: 20260713_0007
Create Date: 2026-07-14
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "20260713_0008"
down_revision: str | None = "20260713_0007"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "interests",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("interest_id", sa.String(length=64), nullable=True),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("genre", sa.String(length=100), nullable=False),
        sa.Column("image_url", sa.String(length=1000), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("interest_id"),
        sa.UniqueConstraint("title", "genre", name="uk_interests_title_genre"),
    )
    op.create_index(
        op.f("ix_interests_interest_id"),
        "interests",
        ["interest_id"],
        unique=True,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_interests_interest_id"), table_name="interests")
    op.drop_table("interests")
