"""add interest target name unique index

Revision ID: 20260715_0020
Revises: 20260715_0019
Create Date: 2026-07-15
"""

from collections.abc import Sequence

from alembic import op

revision: str = "20260715_0020"
down_revision: str | None = "20260715_0019"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute(
        """
        CREATE UNIQUE INDEX uk_interest_targets_user_name_ci
        ON interest_targets (user_id, lower(btrim(name)))
        """,
    )


def downgrade() -> None:
    op.drop_index(
        "uk_interest_targets_user_name_ci",
        table_name="interest_targets",
    )
