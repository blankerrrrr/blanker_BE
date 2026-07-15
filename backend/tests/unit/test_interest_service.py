from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from app.schemas.interest_target import InterestTargetSyncRequest
from app.services.interest_service import InterestService


@pytest.mark.asyncio
async def test_sync_reuses_direct_target_with_same_name() -> None:
    interest = SimpleNamespace(
        interest_id="interest_1098",
        title="모아나",
        catalog=SimpleNamespace(name="영화", image_url=None),
        summary="모아나 줄거리",
        image_url=None,
        genre_mappings=[],
    )
    direct_target = SimpleNamespace(
        interest_target_id="interest_target_1",
        interest_id=None,
        type="WORK",
        name="모아나",
        aliases=["모아나"],
        keywords=["모아나"],
        created_at=None,
    )

    class FakeInterestRepository:
        async def find_all_by_ids(self, interest_ids: list[str]) -> list[object]:
            assert interest_ids == ["interest_1098"]
            return [interest]

    class FakeInterestTargetRepository:
        async def find_catalog_targets_by_user_id(
            self,
            user_id: str,
        ) -> list[object]:
            assert user_id == "user_1"
            return []

        async def find_catalog_target_by_interest_id(
            self,
            user_id: str,
            interest_id: str,
        ) -> None:
            return None

        async def get_by_type_and_name(
            self,
            user_id: str,
            target_type: str,
            name: str,
        ) -> object:
            assert (user_id, target_type, name) == ("user_1", "WORK", "모아나")
            return direct_target

        async def save(self, target: object) -> object:
            return target

        async def delete(self, target: object) -> None:
            raise AssertionError("direct target should not be deleted")

    session = AsyncMock()
    service = InterestService(session)
    service.interests = FakeInterestRepository()
    service.interest_targets = FakeInterestTargetRepository()

    result = await service.sync(
        "user_1",
        InterestTargetSyncRequest(interest_ids=["interest_1098"]),
    )

    session.commit.assert_awaited_once()
    assert direct_target.interest_id == "interest_1098"
    assert result.items[0].interest_id == "interest_1098"
