from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest
from sqlalchemy.exc import IntegrityError

from app.core.error_codes import ErrorCode
from app.core.exceptions import AppException
from app.services.interest_target_service import InterestTargetService


class FakeAIClient:
    def __init__(self) -> None:
        self.called = False

    async def enrich_interest_target(self, name: str) -> SimpleNamespace:
        self.called = True
        return SimpleNamespace(type="WORK", aliases=[], keywords=[name])


@pytest.mark.asyncio
async def test_create_checks_duplicate_before_ai_call() -> None:
    class FakeRepository:
        async def get_by_name(self, user_id: str, name: str) -> object:
            assert user_id == "user_1"
            assert name == "작품명"
            return object()

    ai_client = FakeAIClient()
    service = InterestTargetService(AsyncMock(), ai_client=ai_client)
    service.interest_targets = FakeRepository()

    with pytest.raises(AppException) as exc_info:
        await service.create("user_1", SimpleNamespace(name="작품명"))

    assert exc_info.value.error_code == ErrorCode.INTEREST_TARGET_ALREADY_EXISTS
    assert ai_client.called is False


@pytest.mark.asyncio
async def test_create_converts_integrity_error_to_duplicate_error() -> None:
    class FakeRepository:
        async def get_by_name(self, user_id: str, name: str) -> None:
            return None

        async def save(self, target: object) -> None:
            raise IntegrityError("INSERT", {}, Exception("duplicate"))

    session = AsyncMock()
    service = InterestTargetService(session, ai_client=FakeAIClient())
    service.interest_targets = FakeRepository()

    with pytest.raises(AppException) as exc_info:
        await service.create("user_1", SimpleNamespace(name="작품명"))

    assert exc_info.value.error_code == ErrorCode.INTEREST_TARGET_ALREADY_EXISTS
    session.rollback.assert_awaited_once()
