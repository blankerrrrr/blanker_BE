from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from scripts import start


@pytest.mark.asyncio
async def test_seed_disposes_engine(monkeypatch: pytest.MonkeyPatch) -> None:
    seed = AsyncMock()
    dispose = AsyncMock()
    monkeypatch.setattr(start, "seed_default_interest_types", seed)
    monkeypatch.setattr(start, "engine", SimpleNamespace(dispose=dispose))

    await start.seed_and_dispose_engine()

    seed.assert_awaited_once_with()
    dispose.assert_awaited_once_with()


@pytest.mark.asyncio
async def test_seed_failure_still_disposes_engine(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    seed = AsyncMock(side_effect=RuntimeError("seed failed"))
    dispose = AsyncMock()
    monkeypatch.setattr(start, "seed_default_interest_types", seed)
    monkeypatch.setattr(start, "engine", SimpleNamespace(dispose=dispose))

    with pytest.raises(RuntimeError, match="seed failed"):
        await start.seed_and_dispose_engine()

    dispose.assert_awaited_once_with()
