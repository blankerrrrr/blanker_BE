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
        page: int,
        size: int,
        interest_target_id: str,
        category: BlockCategory | None,
    ) -> BlockedItemListResponse:
        assert user_id == "user_1"
        assert interest_target_id == "interest_target_1"
        assert category == BlockCategory.SPOILER
        return BlockedItemListResponse(
            items=[
                BlockedItemListItemResponse(
                    blocked_item_id="blocked_item_1",
                    interest_target_id=interest_target_id,
                    summary="요약",
                    categories=[BlockCategory.SPOILER],
                    related_topics=["작품명"],
                    source_url="https://example.com/article",
                    found_at=datetime.now(UTC),
                ),
            ],
            page=page,
            size=size,
            total_elements=1,
            total_pages=1,
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


def test_list_blocked_items_requires_interest_target_id() -> None:
    app.dependency_overrides[get_current_user_id] = fake_current_user_id
    client = TestClient(app, raise_server_exceptions=False)

    response = client.get("/api/blocked-items")

    app.dependency_overrides.clear()
    assert response.status_code == 422


def test_list_blocked_items_filters_by_interest_target(monkeypatch) -> None:
    from app.api import blocked_items

    monkeypatch.setattr(blocked_items, "BlockedItemService", FakeBlockedItemService)
    app.dependency_overrides[get_db_session] = fake_db_session
    app.dependency_overrides[get_current_user_id] = fake_current_user_id
    client = TestClient(app)

    response = client.get(
        "/api/blocked-items?interestTargetId=interest_target_1&type=SPOILER",
    )

    app.dependency_overrides.clear()
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["items"][0]["interestTargetId"] == "interest_target_1"


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
