from collections.abc import AsyncGenerator

from fastapi.testclient import TestClient

from app.api.deps import get_current_user_id, get_db_session
from app.main import app
from app.schemas.interest import (
    InterestGenreListResponse,
    InterestGenreResponse,
    InterestListResponse,
    InterestResponse,
    InterestSelectResponse,
    InterestTypeListResponse,
    InterestTypeResponse,
)
from app.schemas.interest_target import InterestTargetResponse


class FakeInterestService:
    list_args: tuple[str, str, str | None] | None = None

    def __init__(self, session: object, query_cache: object | None = None) -> None:
        self.session = session
        self.query_cache = query_cache

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

    async def list_genres(self, interest_type: str) -> InterestGenreListResponse:
        assert interest_type == "게임"
        return InterestGenreListResponse(
            items=[
                InterestGenreResponse(name="Action"),
                InterestGenreResponse(name="Adventure"),
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


class FakeInterestTargetService:
    def __init__(self, session: object) -> None:
        self.session = session

    async def create(
        self,
        user_id: str,
        request: object,
    ) -> InterestTargetResponse:
        return InterestTargetResponse(
            interest_target_id="interest_target_1",
            type="WORK",
            name=f"{user_id}:{request.name}",
            aliases=["별칭"],
            keywords=[request.name],
        )


async def fake_db_session() -> AsyncGenerator[object, None]:
    yield object()


async def fake_current_user_id() -> str:
    return "user_1"


def test_list_interests_uses_required_type_and_default_genre(monkeypatch) -> None:
    from app.api import interests

    monkeypatch.setattr(interests, "InterestService", FakeInterestService)
    app.dependency_overrides[get_db_session] = fake_db_session
    app.dependency_overrides[get_current_user_id] = fake_current_user_id
    client = TestClient(app)

    response = client.get("/api/interests?interestType=애니메이션")

    app.dependency_overrides.clear()
    assert response.status_code == 200
    assert FakeInterestService.list_args == ("애니메이션", "전체", None)
    assert response.json()["data"]["items"][0]["interestType"] == "애니메이션"


def test_list_interests_requires_interest_type() -> None:
    app.dependency_overrides[get_current_user_id] = fake_current_user_id
    client = TestClient(app)

    response = client.get("/api/interests")

    app.dependency_overrides.clear()
    assert response.status_code == 422


def test_list_interest_types(monkeypatch) -> None:
    from app.api import interests

    monkeypatch.setattr(interests, "InterestService", FakeInterestService)
    app.dependency_overrides[get_db_session] = fake_db_session
    app.dependency_overrides[get_current_user_id] = fake_current_user_id
    client = TestClient(app)

    response = client.get("/api/interests/types")

    app.dependency_overrides.clear()
    assert response.status_code == 200
    assert response.json()["data"]["items"][0]["name"] == "애니메이션"


def test_list_interest_genres(monkeypatch) -> None:
    from app.api import interests

    monkeypatch.setattr(interests, "InterestService", FakeInterestService)
    app.dependency_overrides[get_db_session] = fake_db_session
    app.dependency_overrides[get_current_user_id] = fake_current_user_id
    client = TestClient(app)

    response = client.get("/api/interests/genres?interestType=게임")

    app.dependency_overrides.clear()
    assert response.status_code == 200
    assert response.json()["data"]["items"] == [
        {"name": "Action"},
        {"name": "Adventure"},
    ]


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


def test_create_interest_target_accepts_name_only(monkeypatch) -> None:
    from app.api import interests

    monkeypatch.setattr(
        interests,
        "InterestTargetService",
        FakeInterestTargetService,
    )
    app.dependency_overrides[get_db_session] = fake_db_session
    app.dependency_overrides[get_current_user_id] = fake_current_user_id
    client = TestClient(app)

    response = client.post(
        "/api/interests/targets",
        json={"name": "작품명"},
    )

    app.dependency_overrides.clear()
    assert response.status_code == 201
    data = response.json()["data"]
    assert data["type"] == "WORK"
    assert data["name"] == "user_1:작품명"
    assert data["aliases"] == ["별칭"]
    assert data["keywords"] == ["작품명"]
