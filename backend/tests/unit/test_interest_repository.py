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


@pytest.mark.asyncio
async def test_find_all_filters_by_multiple_genres() -> None:
    session = AsyncMock()
    result = MagicMock()
    result.scalars.return_value.unique.return_value.all.return_value = []
    session.execute.return_value = result

    await InterestRepository(session).find_all(
        "애니메이션",
        ["액션", "판타지"],
        None,
    )

    statement = session.execute.await_args.args[0]
    compiled = str(
        statement.compile(
            dialect=postgresql.dialect(),
            compile_kwargs={"literal_binds": True},
        ),
    )
    assert "interest_genres.name IN ('액션', '판타지')" in compiled
