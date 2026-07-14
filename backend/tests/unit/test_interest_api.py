from collections.abc import AsyncGenerator

from fastapi.testclient import TestClient

from app.api.deps import get_current_user_id, get_db_session
from app.main import app
from app.schemas.interest import (
    InterestListResponse,
    InterestResponse,
    InterestSelectResponse,
    InterestTypeListResponse,
    InterestTypeResponse,
)
from app.schemas.interest_target import InterestTargetResponse


class FakeInterestService:
    list_args: tuple[str, str, str | None] | None = None

    def __init__(self, session: object) -> None:
        self.session = session

    async def list(
        self,
        interest_type: str,
        genre: str,
        keyword: str | None,
    ) -> InterestListResponse:
        FakeInterestService.list_args = (interest_type, genre, keyword)
        return InterestListResponse(
            items=[
                InterestResponse(
                    interest_id="interest_1",
                    interest_type=interest_type,
                    interest_type_image_url="https://example.com/type.jpg",
                    title="작품명",
                    genre=genre,
                    image_url="https://example.com/image.jpg",
                ),
            ],
        )

    async def list_types(self) -> InterestTypeListResponse:
        return InterestTypeListResponse(
            items=[
                InterestTypeResponse(
                    name="애니메이션",
                    image_url="https://example.com/anime.jpg",
                ),
            ],
        )

    async def select(
        self,
        user_id: str,
        request: object,
    ) -> InterestSelectResponse:
        return InterestSelectResponse(
            items=[
                InterestTargetResponse(
                    interest_target_id="interest_target_1",
                    type="WORK",
                    name=f"{user_id}:{request.interest_ids[0]}",
                    aliases=[],
                    keywords=["애니메이션"],
                ),
            ],
        )


async def fake_db_session() -> AsyncGenerator[object, None]:
    yield object()


async def fake_current_user_id() -> str:
    return "user_1"


def test_list_interests_uses_required_type_and_default_genre(monkeypatch) -> None:
    from app.api import interests

    monkeypatch.setattr(interests, "InterestService", FakeInterestService)
    app.dependency_overrides[get_db_session] = fake_db_session
    client = TestClient(app)

    response = client.get("/api/interests?interestType=애니메이션")

    app.dependency_overrides.clear()
    assert response.status_code == 200
    assert FakeInterestService.list_args == ("애니메이션", "전체", None)
    assert response.json()["data"]["items"][0]["interestType"] == "애니메이션"


def test_list_interests_requires_interest_type() -> None:
    client = TestClient(app)

    response = client.get("/api/interests")

    assert response.status_code == 422


def test_list_interest_types(monkeypatch) -> None:
    from app.api import interests

    monkeypatch.setattr(interests, "InterestService", FakeInterestService)
    app.dependency_overrides[get_db_session] = fake_db_session
    client = TestClient(app)

    response = client.get("/api/interests/types")

    app.dependency_overrides.clear()
    assert response.status_code == 200
    assert response.json()["data"]["items"][0]["name"] == "애니메이션"


def test_select_interests(monkeypatch) -> None:
    from app.api import interests

    monkeypatch.setattr(interests, "InterestService", FakeInterestService)
    app.dependency_overrides[get_db_session] = fake_db_session
    app.dependency_overrides[get_current_user_id] = fake_current_user_id
    client = TestClient(app)

    response = client.post(
        "/api/interests/select",
        json={"interestIds": ["interest_1"]},
    )

    app.dependency_overrides.clear()
    assert response.status_code == 200
    assert response.json()["data"]["items"][0]["name"] == "user_1:interest_1"
