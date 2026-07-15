"""set blocked item target to null when interest target is deleted

Revision ID: 20260715_0021
Revises: 20260715_0020
Create Date: 2026-07-15
"""

from collections.abc import Sequence

from alembic import op

revision: str = "20260715_0021"
down_revision: str | None = "20260715_0020"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.drop_constraint(
        "fk_blocked_items_interest_target_id",
        "blocked_items",
        type_="foreignkey",
    )
    op.create_foreign_key(
        "fk_blocked_items_interest_target_id",
        "blocked_items",
        "interest_targets",
        ["interest_target_id"],
        ["interest_target_id"],
        ondelete="SET NULL",
    )


def downgrade() -> None:
    op.drop_constraint(
        "fk_blocked_items_interest_target_id",
        "blocked_items",
        type_="foreignkey",
    )
    op.create_foreign_key(
        "fk_blocked_items_interest_target_id",
        "blocked_items",
        "interest_targets",
        ["interest_target_id"],
        ["interest_target_id"],
    )
