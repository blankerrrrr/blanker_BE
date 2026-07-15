"""remove all genre

Revision ID: 20260715_0019
Revises: 20260715_0018
Create Date: 2026-07-15
"""

from collections.abc import Sequence

from alembic import op

revision: str = "20260715_0019"
down_revision: str | None = "20260715_0018"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute(
        """
        DELETE FROM interest_genre_mappings
        WHERE genre_id IN (
            SELECT id FROM interest_genres WHERE name = '전체'
        )
        """,
    )
    op.execute("DELETE FROM interest_genres WHERE name = '전체'")


def downgrade() -> None:
    op.execute(
        """
        INSERT INTO interest_genres (name, created_at, updated_at)
        VALUES ('전체', now(), now())
        ON CONFLICT (name) DO NOTHING
        """,
    )
