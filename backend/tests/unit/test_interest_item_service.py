from datetime import UTC, datetime
from types import SimpleNamespace

import pytest

from app.services.interest_item_service import InterestItemService


def test_interest_item_list_response_includes_image_url() -> None:
    item = SimpleNamespace(
        interest_item_id="interest_item_1",
        title="관심 정보",
        summary="요약",
        image_url="https://example.com/image.png",
        related_topics=["작품명"],
        discovered_at=datetime.now(UTC),
    )

    response = InterestItemService._to_list_item(item)

    assert response.image_url == "https://example.com/image.png"


def test_interest_item_detail_response_includes_image_url() -> None:
    item = SimpleNamespace(
        interest_item_id="interest_item_1",
        title="관심 정보",
        summary="요약",
        image_url="https://example.com/image.png",
        related_topics=["작품명"],
        source_url="https://example.com/article",
        selector="article",
        discovered_at=datetime.now(UTC),
    )

    response = InterestItemService._to_detail(item)

    assert response.image_url == "https://example.com/image.png"


def test_interest_item_url_response_includes_source_url() -> None:
    item = SimpleNamespace(
        interest_item_id="interest_item_1",
        source_url="https://example.com/article",
        discovered_at=datetime.now(UTC),
    )

    response = InterestItemService._to_url_item(item)

    assert response.interest_item_id == "interest_item_1"
    assert response.source_url == "https://example.com/article"


@pytest.mark.asyncio
async def test_interest_item_url_list_is_ordered_by_latest() -> None:
    older_item = SimpleNamespace(
        interest_item_id="interest_item_1",
        source_url="https://example.com/older",
        discovered_at=datetime(2026, 7, 14, 1, 2, 3, tzinfo=UTC),
    )
    newer_same_date_item = SimpleNamespace(
        interest_item_id="interest_item_2",
        source_url="https://example.com/newer-same-date",
        discovered_at=datetime(2026, 7, 14, 3, 2, 1, tzinfo=UTC),
    )
    newest_item = SimpleNamespace(
        interest_item_id="interest_item_3",
        source_url="https://example.com/newest",
        discovered_at=datetime(2026, 7, 15, 1, 2, 3, tzinfo=UTC),
    )

    class FakeInterestItemRepository:
        async def find_urls(self, user_id: str) -> list[SimpleNamespace]:
            assert user_id == "user_1"
            return [older_item, newest_item, newer_same_date_item]

    service = InterestItemService.__new__(InterestItemService)
    service.interest_items = FakeInterestItemRepository()

    response = await service.list_urls("user_1")

    assert response.root == [
        {"2026-07-15": [InterestItemService._to_url_item(newest_item)]},
        {
            "2026-07-14": [
                InterestItemService._to_url_item(newer_same_date_item),
                InterestItemService._to_url_item(older_item),
            ],
        },
    ]
