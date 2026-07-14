from collections.abc import AsyncGenerator
from datetime import UTC, datetime

from fastapi.testclient import TestClient

from app.api.deps import get_current_user_id, get_db_session
from app.main import app
from app.schemas.analysis import BlockCategory
from app.schemas.blocked_item import (
    BlockedItemCreateResponse,
    BlockedItemListItemResponse,
    BlockedItemListResponse,
)


class FakeBlockedItemService:
    def __init__(self, session: object) -> None:
        self.session = session

    async def list(
        self,
        user_id: str,
        interest_target_id: str | None,
        interest_type: str | None,
        category: BlockCategory | None,
    ) -> BlockedItemListResponse:
        assert user_id == "user_1"
        assert interest_target_id == "interest_target_1"
        assert interest_type == "애니메이션"
        assert category == BlockCategory.SPOILER
        return BlockedItemListResponse(
            root=[
                {
                    "작품명": [
                        BlockedItemListItemResponse(
                            blocked_item_id="blocked_item_1",
                            interest_target_id=interest_target_id,
                            summary="요약",
                            categories=[BlockCategory.SPOILER],
                            related_topics=["작품명"],
                            source_url="https://example.com/article",
                            found_at=datetime(2026, 7, 13, 5, 0, tzinfo=UTC),
                        ),
                    ],
                },
            ],
        )

    async def create(
        self,
        user_id: str,
        request: object,
    ) -> BlockedItemCreateResponse:
        assert user_id == "user_1"
        assert request.interest_target_id == "interest_target_1"
        return BlockedItemCreateResponse(
            blocked_item_id="blocked_item_1",
            saved_at=datetime.now(UTC),
        )


async def fake_db_session() -> AsyncGenerator[object, None]:
    yield object()


async def fake_current_user_id() -> str:
    return "user_1"


def test_list_blocked_items_filters_by_interest_target(monkeypatch) -> None:
    from app.api import blocked_items

    monkeypatch.setattr(blocked_items, "BlockedItemService", FakeBlockedItemService)
    app.dependency_overrides[get_db_session] = fake_db_session
    app.dependency_overrides[get_current_user_id] = fake_current_user_id
    client = TestClient(app)

    response = client.get(
        "/api/blocked-items?interestTargetId=interest_target_1&interestType=애니메이션&type=SPOILER",
    )

    app.dependency_overrides.clear()
    assert response.status_code == 200
    data = response.json()["data"]
    assert data == [
        {
            "작품명": [
                {
                    "blockedItemId": "blocked_item_1",
                    "interestTargetId": "interest_target_1",
                    "summary": "요약",
                    "categories": ["SPOILER"],
                    "relatedTopics": ["작품명"],
                    "sourceUrl": "https://example.com/article",
                    "foundAt": "2026-07-13T05:00:00Z",
                },
            ],
        },
    ]


def test_create_blocked_item_accepts_interest_target_id(monkeypatch) -> None:
    from app.api import blocked_items

    monkeypatch.setattr(blocked_items, "BlockedItemService", FakeBlockedItemService)
    app.dependency_overrides[get_db_session] = fake_db_session
    app.dependency_overrides[get_current_user_id] = fake_current_user_id
    client = TestClient(app)

    response = client.post(
        "/api/blocked-items",
        json={
            "interestTargetId": "interest_target_1",
            "summary": "요약",
            "categories": ["SPOILER"],
            "relatedTopics": ["작품명"],
            "sourceUrl": "https://example.com/article",
        },
    )

    app.dependency_overrides.clear()
    assert response.status_code == 201
    assert response.json()["data"]["blockedItemId"] == "blocked_item_1"
