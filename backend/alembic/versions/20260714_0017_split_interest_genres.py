"""split interest genres

Revision ID: 20260714_0017
Revises: 20260714_0016
Create Date: 2026-07-14
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "20260714_0017"
down_revision: str | None = "20260714_0016"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "interest_genres",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name", name="uk_interest_genres_name"),
    )
    op.create_table(
        "interest_genre_mappings",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("interest_id", sa.Integer(), nullable=False),
        sa.Column("genre_id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["genre_id"],
            ["interest_genres.id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(["interest_id"], ["interests.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "interest_id",
            "genre_id",
            name="uk_interest_genre_mappings_interest_genre",
        ),
    )
    op.create_index(
        op.f("ix_interest_genre_mappings_genre_id"),
        "interest_genre_mappings",
        ["genre_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_interest_genre_mappings_interest_id"),
        "interest_genre_mappings",
        ["interest_id"],
        unique=False,
    )

    op.execute(
        """
        INSERT INTO interest_genres (name, created_at, updated_at)
        SELECT DISTINCT TRIM(genre_name), NOW(), NOW()
        FROM interests
        CROSS JOIN LATERAL regexp_split_to_table(
            COALESCE(interests.genre, '전체'),
            '\\s*>\\s*|\\s*,\\s*'
        ) AS genre_name
        WHERE TRIM(genre_name) <> ''
        ON CONFLICT (name) DO NOTHING
        """,
    )
    op.execute(
        """
        INSERT INTO interest_genre_mappings (interest_id, genre_id, created_at)
        SELECT DISTINCT interests.id, interest_genres.id, NOW()
        FROM interests
        CROSS JOIN LATERAL regexp_split_to_table(
            COALESCE(interests.genre, '전체'),
            '\\s*>\\s*|\\s*,\\s*'
        ) AS genre_name
        JOIN interest_genres ON interest_genres.name = TRIM(genre_name)
        WHERE TRIM(genre_name) <> ''
        ON CONFLICT (interest_id, genre_id) DO NOTHING
        """,
    )
    op.execute(
        """
        WITH duplicates AS (
            SELECT
                id,
                interest_id AS public_id,
                FIRST_VALUE(id) OVER (
                    PARTITION BY interest_catalog_id, title
                    ORDER BY id
                ) AS keep_id
            FROM interests
        )
        INSERT INTO interest_genre_mappings (interest_id, genre_id, created_at)
        SELECT DISTINCT duplicates.keep_id, mappings.genre_id, NOW()
        FROM interest_genre_mappings AS mappings
        JOIN duplicates ON duplicates.id = mappings.interest_id
        WHERE duplicates.id <> duplicates.keep_id
        ON CONFLICT (interest_id, genre_id) DO NOTHING
        """,
    )
    op.execute(
        """
        WITH duplicates AS (
            SELECT
                id,
                FIRST_VALUE(id) OVER (
                    PARTITION BY interest_catalog_id, title
                    ORDER BY id
                ) AS keep_id
            FROM interests
        )
        DELETE FROM interest_genre_mappings AS mappings
        USING duplicates
        WHERE mappings.interest_id = duplicates.id
            AND duplicates.id <> duplicates.keep_id
        """,
    )
    op.execute(
        """
        WITH duplicates AS (
            SELECT
                id,
                interest_id AS public_id,
                FIRST_VALUE(interest_id) OVER (
                    PARTITION BY interest_catalog_id, title
                    ORDER BY id
                ) AS keep_public_id,
                FIRST_VALUE(id) OVER (
                    PARTITION BY interest_catalog_id, title
                    ORDER BY id
                ) AS keep_id
            FROM interests
        )
        UPDATE interest_targets
        SET interest_id = duplicates.keep_public_id
        FROM duplicates
        WHERE interest_targets.interest_id = duplicates.public_id
            AND duplicates.id <> duplicates.keep_id
        """,
    )
    op.execute(
        """
        WITH duplicates AS (
            SELECT
                id,
                FIRST_VALUE(id) OVER (
                    PARTITION BY interest_catalog_id, title
                    ORDER BY id
                ) AS keep_id
            FROM interests
        )
        DELETE FROM interests
        USING duplicates
        WHERE interests.id = duplicates.id
            AND duplicates.id <> duplicates.keep_id
        """,
    )

    op.drop_constraint("uk_interests_catalog_title_genre", "interests", type_="unique")
    op.create_unique_constraint(
        "uk_interests_catalog_title",
        "interests",
        ["interest_catalog_id", "title"],
    )
    op.drop_column("interests", "genre")


def downgrade() -> None:
    op.add_column(
        "interests",
        sa.Column("genre", sa.String(length=100), nullable=True),
    )
    op.execute(
        """
        UPDATE interests
        SET genre = COALESCE(genres.name, '전체')
        FROM (
            SELECT
                interest_genre_mappings.interest_id,
                string_agg(interest_genres.name, ', ' ORDER BY interest_genres.name)
                    AS name
            FROM interest_genre_mappings
            JOIN interest_genres
                ON interest_genres.id = interest_genre_mappings.genre_id
            GROUP BY interest_genre_mappings.interest_id
        ) AS genres
        WHERE interests.id = genres.interest_id
        """,
    )
    op.execute("UPDATE interests SET genre = '전체' WHERE genre IS NULL")
    op.alter_column("interests", "genre", nullable=False)

    op.drop_constraint("uk_interests_catalog_title", "interests", type_="unique")
    op.create_unique_constraint(
        "uk_interests_catalog_title_genre",
        "interests",
        ["interest_catalog_id", "title", "genre"],
    )
    op.drop_index(
        op.f("ix_interest_genre_mappings_interest_id"),
        table_name="interest_genre_mappings",
    )
    op.drop_index(
        op.f("ix_interest_genre_mappings_genre_id"),
        table_name="interest_genre_mappings",
    )
    op.drop_table("interest_genre_mappings")
    op.drop_table("interest_genres")
