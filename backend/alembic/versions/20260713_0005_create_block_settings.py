"""create block settings table

Revision ID: 20260713_0005
Revises: 20260713_0004
Create Date: 2026-07-13
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "20260713_0005"
down_revision: str | None = "20260713_0004"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "block_settings",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("block_setting_id", sa.String(length=64), nullable=False),
        sa.Column("user_id", sa.String(length=64), nullable=False),
        sa.Column("category", sa.String(length=20), nullable=False),
        sa.Column("enabled", sa.Boolean(), nullable=False),
        sa.Column("sensitivity", sa.String(length=20), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.user_id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "user_id",
            "category",
            name="uk_block_settings_user_category",
        ),
    )
    op.create_index(
        "ix_block_settings_block_setting_id",
        "block_settings",
        ["block_setting_id"],
        unique=True,
    )
    op.create_index(
        "ix_block_settings_user_id",
        "block_settings",
        ["user_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_block_settings_user_id", table_name="block_settings")
    op.drop_index("ix_block_settings_block_setting_id", table_name="block_settings")
    op.drop_table("block_settings")
