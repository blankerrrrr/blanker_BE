"""split interest catalog

Revision ID: 20260714_0014
Revises: 20260714_0013
Create Date: 2026-07-14
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "20260714_0014"
down_revision: str | None = "20260714_0013"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "interest_catalog",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.Column("image_url", sa.String(length=1000), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name", name="uk_interest_catalog_name"),
    )

    op.execute(
        """
        INSERT INTO interest_catalog (name, image_url, created_at, updated_at)
        SELECT interest_type, MAX(interest_type_image_url), NOW(), NOW()
        FROM interests
        GROUP BY interest_type
        """,
    )

    op.add_column(
        "interests",
        sa.Column("interest_catalog_id", sa.Integer(), nullable=True),
    )
    op.create_foreign_key(
        "fk_interests_interest_catalog_id",
        "interests",
        "interest_catalog",
        ["interest_catalog_id"],
        ["id"],
    )
    op.create_index(
        op.f("ix_interests_interest_catalog_id"),
        "interests",
        ["interest_catalog_id"],
        unique=False,
    )
    op.execute(
        """
        UPDATE interests
        SET interest_catalog_id = interest_catalog.id
        FROM interest_catalog
        WHERE interests.interest_type = interest_catalog.name
        """,
    )
    op.alter_column("interests", "interest_catalog_id", nullable=False)

    op.drop_constraint("uk_interests_type_title_genre", "interests", type_="unique")
    op.create_unique_constraint(
        "uk_interests_catalog_title_genre",
        "interests",
        ["interest_catalog_id", "title", "genre"],
    )
    op.drop_column("interests", "interest_type_image_url")
    op.drop_column("interests", "interest_type")


def downgrade() -> None:
    op.add_column(
        "interests",
        sa.Column("interest_type", sa.String(length=50), nullable=True),
    )
    op.add_column(
        "interests",
        sa.Column("interest_type_image_url", sa.String(length=1000), nullable=True),
    )
    op.execute(
        """
        UPDATE interests
        SET
            interest_type = interest_catalog.name,
            interest_type_image_url = interest_catalog.image_url
        FROM interest_catalog
        WHERE interests.interest_catalog_id = interest_catalog.id
        """,
    )
    op.alter_column("interests", "interest_type", nullable=False)

    op.drop_constraint("uk_interests_catalog_title_genre", "interests", type_="unique")
    op.create_unique_constraint(
        "uk_interests_type_title_genre",
        "interests",
        ["interest_type", "title", "genre"],
    )
    op.drop_index(op.f("ix_interests_interest_catalog_id"), table_name="interests")
    op.drop_constraint(
        "fk_interests_interest_catalog_id",
        "interests",
        type_="foreignkey",
    )
    op.drop_column("interests", "interest_catalog_id")
    op.drop_table("interest_catalog")
