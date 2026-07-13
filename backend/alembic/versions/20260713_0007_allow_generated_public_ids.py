"""allow generated public ids

Revision ID: 20260713_0007
Revises: 20260713_0006
Create Date: 2026-07-13
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "20260713_0007"
down_revision: str | None = "20260713_0006"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


PUBLIC_ID_COLUMNS = (
    ("users", "user_id"),
    ("interest_targets", "interest_target_id"),
    ("interest_item_groups", "group_id"),
    ("interest_items", "interest_item_id"),
    ("analysis_requests", "analysis_request_id"),
    ("analysis_contents", "analysis_content_id"),
    ("analysis_results", "analysis_result_id"),
    ("block_settings", "block_setting_id"),
    ("blocked_items", "blocked_item_id"),
)


def upgrade() -> None:
    for table_name, column_name in PUBLIC_ID_COLUMNS:
        op.alter_column(
            table_name,
            column_name,
            existing_type=sa.String(length=64),
            nullable=True,
        )


def downgrade() -> None:
    for table_name, column_name in reversed(PUBLIC_ID_COLUMNS):
        op.alter_column(
            table_name,
            column_name,
            existing_type=sa.String(length=64),
            nullable=False,
        )
