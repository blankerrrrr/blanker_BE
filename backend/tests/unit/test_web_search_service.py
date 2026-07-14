import pytest

from app.core.error_codes import ErrorCode
from app.core.exceptions import AppException
from app.services.web_search_service import WebSearchService


@pytest.mark.asyncio
async def test_web_search_service_normalizes_results() -> None:
    requested: dict[str, object] = {}

    class FakeWebSearchService(WebSearchService):
        def _read_json(
            self,
            url: str,
            headers: dict[str, str],
        ) -> dict[str, object]:
            requested["url"] = url
            requested["headers"] = headers
            return {
                "web": {
                    "results": [
                        {
                            "title": "검색 결과",
                            "url": "https://example.com/article",
                            "description": "요약",
                        },
                        {
                            "title": "URL 없는 결과",
                            "description": "제외",
                        },
                    ],
                },
            }

    service = FakeWebSearchService(
        api_key="test_key",
        api_url="https://search.example.test",
    )

    response = await service.search(
        query="테스트 검색",
        count=3,
        country="KR",
        search_lang="ko",
        freshness="pw",
    )

    assert requested["headers"] == {
        "Accept": "application/json",
        "X-Subscription-Token": "test_key",
    }
    assert requested["url"] == (
        "https://search.example.test?"
        "q=%ED%85%8C%EC%8A%A4%ED%8A%B8+%EA%B2%80%EC%83%89"
        "&count=3&safesearch=moderate&country=KR&search_lang=ko&freshness=pw"
    )
    assert response.query == "테스트 검색"
    assert len(response.results) == 1
    assert response.results[0].title == "검색 결과"
    assert response.results[0].url == "https://example.com/article"
    assert response.results[0].description == "요약"


@pytest.mark.asyncio
async def test_web_search_service_requires_api_key() -> None:
    service = WebSearchService(api_key="")

    with pytest.raises(AppException) as exc_info:
        await service.search(
            query="테스트",
            count=5,
            country="KR",
            search_lang="ko",
            freshness=None,
        )

    assert exc_info.value.error_code == ErrorCode.WEB_SEARCH_NOT_CONFIGURED
