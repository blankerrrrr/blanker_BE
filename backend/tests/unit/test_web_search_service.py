import pytest

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
                "results": [
                    {
                        "title": "검색 결과",
                        "url": "https://example.com/article",
                        "content": "요약",
                    },
                    {
                        "title": "두 번째 결과",
                        "url": "https://example.com/second",
                        "content": "제외",
                    },
                    {
                        "title": "URL 없는 결과",
                        "content": "제외",
                    },
                ],
            }

    service = FakeWebSearchService(
        api_url="https://search.example.test",
    )

    response = await service.search(
        query="테스트 검색",
        count=1,
        search_lang="ko",
        freshness="pm",
    )

    assert requested["headers"] == {"Accept": "application/json"}
    assert requested["url"] == (
        "https://search.example.test?"
        "q=%ED%85%8C%EC%8A%A4%ED%8A%B8+%EA%B2%80%EC%83%89"
        "&format=json&safesearch=1&language=ko&time_range=month"
    )
    assert response.query == "테스트 검색"
    assert len(response.results) == 1
    assert response.results[0].title == "검색 결과"
    assert response.results[0].url == "https://example.com/article"
    assert response.results[0].description == "요약"
