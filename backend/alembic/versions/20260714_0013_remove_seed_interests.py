"""remove seed interests

Revision ID: 20260714_0013
Revises: 20260714_0012
Create Date: 2026-07-14
"""

from collections.abc import Sequence

from alembic import op

revision: str = "20260714_0013"
down_revision: str | None = "20260714_0012"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute(
        "DELETE FROM interests "
        "WHERE interest_id IN ('interest_1', 'interest_2', 'interest_3', 'interest_4')",
    )


def downgrade() -> None:
    pass
