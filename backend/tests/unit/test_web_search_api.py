from fastapi.testclient import TestClient

from app.api.deps import get_current_user_id
from app.main import app
from app.schemas.web_search import WebSearchResponse, WebSearchResultResponse


class FakeWebSearchService:
    async def search(
        self,
        query: str,
        count: int,
        country: str | None,
        search_lang: str | None,
        freshness: str | None,
    ) -> WebSearchResponse:
        assert query == "테스트"
        assert count == 2
        assert country == "KR"
        assert search_lang == "ko"
        assert freshness is None
        return WebSearchResponse(
            query=query,
            results=[
                WebSearchResultResponse(
                    title="검색 결과",
                    url="https://example.com/article",
                    description="요약",
                ),
            ],
        )


async def fake_current_user_id() -> str:
    return "user_1"


def test_search_web(monkeypatch) -> None:
    from app.api import web_search

    monkeypatch.setattr(web_search, "WebSearchService", FakeWebSearchService)
    app.dependency_overrides[get_current_user_id] = fake_current_user_id
    client = TestClient(app)

    response = client.get("/api/web-search?query=테스트&count=2")

    app.dependency_overrides.clear()
    assert response.status_code == 200
    assert response.json()["data"] == {
        "query": "테스트",
        "results": [
            {
                "title": "검색 결과",
                "url": "https://example.com/article",
                "description": "요약",
            },
        ],
    }


def test_search_web_requires_auth() -> None:
    client = TestClient(app, raise_server_exceptions=False)

    response = client.get("/api/web-search?query=테스트")

    assert response.status_code == 401
