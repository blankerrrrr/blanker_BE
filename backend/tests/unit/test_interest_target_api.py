from collections.abc import AsyncGenerator

from fastapi.testclient import TestClient

from app.api.deps import get_current_user_id, get_db_session
from app.main import app
from app.schemas.interest_target import (
    InterestTargetTitleListResponse,
    InterestTargetTitleResponse,
)


class FakeInterestTargetService:
    def __init__(self, session: object) -> None:
        self.session = session

    async def list_titles(self, user_id: str) -> InterestTargetTitleListResponse:
        assert user_id == "user_1"
        return InterestTargetTitleListResponse(
            items=[
                InterestTargetTitleResponse(
                    interest_target_id="interest_target_1",
                    title="작품명",
                ),
            ],
        )


async def fake_db_session() -> AsyncGenerator[object, None]:
    yield object()


async def fake_current_user_id() -> str:
    return "user_1"


def test_list_interest_target_titles(monkeypatch) -> None:
    from app.api import interest_targets

    monkeypatch.setattr(
        interest_targets,
        "InterestTargetService",
        FakeInterestTargetService,
    )
    app.dependency_overrides[get_db_session] = fake_db_session
    app.dependency_overrides[get_current_user_id] = fake_current_user_id
    client = TestClient(app)

    response = client.get("/api/interest-targets/titles")

    app.dependency_overrides.clear()
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["items"] == [
        {
            "interestTargetId": "interest_target_1",
            "title": "작품명",
        },
    ]


def test_list_interest_target_titles_requires_auth() -> None:
    client = TestClient(app, raise_server_exceptions=False)

    response = client.get("/api/interest-targets/titles")

    assert response.status_code == 401
