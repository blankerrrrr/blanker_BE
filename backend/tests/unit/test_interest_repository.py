from unittest.mock import AsyncMock, MagicMock

import pytest
from sqlalchemy.dialects import postgresql

from app.db.repositories.interest_repository import InterestRepository


@pytest.mark.asyncio
async def test_find_types_orders_by_catalog_id() -> None:
    session = AsyncMock()
    result = MagicMock()
    result.all.return_value = []
    session.execute.return_value = result

    await InterestRepository(session).find_types()

    statement = session.execute.await_args.args[0]
    compiled = str(
        statement.compile(dialect=postgresql.dialect()),
    )
    assert "ORDER BY interest_catalog.id ASC" in compiled
