"""seed default interests

Revision ID: 20260713_0010
Revises: 20260713_0009
Create Date: 2026-07-14
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "20260713_0010"
down_revision: str | None = "20260713_0009"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


INTERESTS = (
    (1, "interest_1", "영화", "옵세션", "전체"),
    (2, "interest_2", "드라마", "폭싹 속았수다", "전체"),
    (3, "interest_3", "애니메이션", "Sousou no Frieren", "Adventure"),
    (4, "interest_4", "소설", "해리 포터와 마법사의 돌", "국내도서>소설"),
)


def upgrade() -> None:
    interests = sa.table(
        "interests",
        sa.column("id", sa.Integer),
        sa.column("interest_id", sa.String),
        sa.column("interest_type", sa.String),
        sa.column("interest_type_image_url", sa.String),
        sa.column("title", sa.String),
        sa.column("genre", sa.String),
        sa.column("image_url", sa.String),
        sa.column("created_at", sa.DateTime),
        sa.column("updated_at", sa.DateTime),
    )
    op.bulk_insert(
        interests,
        [
            {
                "id": item_id,
                "interest_id": public_id,
                "interest_type": interest_type,
                "interest_type_image_url": None,
                "title": title,
                "genre": genre,
                "image_url": None,
                "created_at": sa.func.now(),
                "updated_at": sa.func.now(),
            }
            for item_id, public_id, interest_type, title, genre in INTERESTS
        ],
    )
    op.execute(
        "SELECT setval("
        "pg_get_serial_sequence('interests', 'id'), "
        "(SELECT COALESCE(MAX(id), 1) FROM interests)"
        ")",
    )


def downgrade() -> None:
    op.execute(
        "DELETE FROM interests "
        "WHERE interest_id IN ('interest_1', 'interest_2', 'interest_3', 'interest_4')",
    )
