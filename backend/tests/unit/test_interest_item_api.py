from collections.abc import AsyncGenerator
from datetime import UTC, datetime

from fastapi.testclient import TestClient

from app.api.deps import get_current_user_id, get_db_session
from app.main import app
from app.schemas.interest_item import (
    InterestItemUrlListResponse,
    InterestItemUrlResponse,
)


class FakeInterestItemService:
    def __init__(self, session: object) -> None:
        self.session = session

    async def list_urls(self, user_id: str) -> InterestItemUrlListResponse:
        assert user_id == "user_1"
        return InterestItemUrlListResponse(
            items=[
                InterestItemUrlResponse(
                    interest_item_id="interest_item_1",
                    source_url="https://example.com/article",
                    discovered_at=datetime(2026, 7, 14, 1, 2, 3, tzinfo=UTC),
                ),
            ],
        )


async def fake_db_session() -> AsyncGenerator[object, None]:
    yield object()


async def fake_current_user_id() -> str:
    return "user_1"


def test_list_interest_item_urls(monkeypatch) -> None:
    from app.api import interest_items

    monkeypatch.setattr(
        interest_items,
        "InterestItemService",
        FakeInterestItemService,
    )
    app.dependency_overrides[get_db_session] = fake_db_session
    app.dependency_overrides[get_current_user_id] = fake_current_user_id
    client = TestClient(app)

    response = client.get("/api/interest-items/urls")

    app.dependency_overrides.clear()
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["items"] == [
        {
            "interestItemId": "interest_item_1",
            "sourceUrl": "https://example.com/article",
            "discoveredAt": "2026-07-14T01:02:03Z",
        },
    ]


def test_list_interest_item_urls_requires_auth() -> None:
    client = TestClient(app, raise_server_exceptions=False)

    response = client.get("/api/interest-items/urls")

    assert response.status_code == 401
