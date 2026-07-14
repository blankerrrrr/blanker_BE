"""add interest type

Revision ID: 20260713_0009
Revises: 20260713_0008
Create Date: 2026-07-14
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "20260713_0009"
down_revision: str | None = "20260713_0008"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "interests",
        sa.Column(
            "interest_type",
            sa.String(length=50),
            nullable=False,
            server_default="기타",
        ),
    )
    op.add_column(
        "interests",
        sa.Column("interest_type_image_url", sa.String(length=1000), nullable=True),
    )
    op.drop_constraint("uk_interests_title_genre", "interests", type_="unique")
    op.create_unique_constraint(
        "uk_interests_type_title_genre",
        "interests",
        ["interest_type", "title", "genre"],
    )
    op.alter_column("interests", "interest_type", server_default=None)


def downgrade() -> None:
    op.drop_constraint("uk_interests_type_title_genre", "interests", type_="unique")
    op.create_unique_constraint(
        "uk_interests_title_genre",
        "interests",
        ["title", "genre"],
    )
    op.drop_column("interests", "interest_type")
    op.drop_column("interests", "interest_type_image_url")
