from datetime import UTC, datetime
from types import SimpleNamespace

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
