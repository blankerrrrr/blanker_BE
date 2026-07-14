import asyncio
import json
import urllib.parse
import urllib.request
from typing import Any

from app.core.config import settings
from app.core.error_codes import ErrorCode
from app.core.exceptions import AppException
from app.schemas.web_search import WebSearchResponse, WebSearchResultResponse


class WebSearchService:
    def __init__(
        self,
        api_key: str | None = None,
        api_url: str | None = None,
        timeout_seconds: int | None = None,
    ) -> None:
        self.api_key = api_key if api_key is not None else settings.web_search_api_key
        self.api_url = api_url or settings.web_search_api_url
        self.timeout_seconds = timeout_seconds or settings.web_search_timeout_seconds

    # 외부 검색 API 결과를 서버 표준 응답으로 정규화한다.
    async def search(
        self,
        query: str,
        count: int,
        country: str | None,
        search_lang: str | None,
        freshness: str | None,
    ) -> WebSearchResponse:
        if self.api_key is None or not self.api_key.strip():
            raise AppException(ErrorCode.WEB_SEARCH_NOT_CONFIGURED)

        params: dict[str, str | int] = {
            "q": query,
            "count": count,
            "safesearch": "moderate",
        }
        if country:
            params["country"] = country
        if search_lang:
            params["search_lang"] = search_lang
        if freshness:
            params["freshness"] = freshness

        url = f"{self.api_url}?{urllib.parse.urlencode(params)}"
        headers = {
            "Accept": "application/json",
            "X-Subscription-Token": self.api_key,
        }

        try:
            payload = await asyncio.to_thread(self._read_json, url, headers)
        except Exception as exc:
            raise AppException(ErrorCode.WEB_SEARCH_FAILED) from exc

        return WebSearchResponse(
            query=query,
            results=self._to_results(payload),
        )

    def _read_json(self, url: str, headers: dict[str, str]) -> dict[str, Any]:
        request = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(
            request,
            timeout=self.timeout_seconds,
        ) as response:
            return json.loads(response.read().decode("utf-8"))

    @staticmethod
    def _to_results(payload: dict[str, Any]) -> list[WebSearchResultResponse]:
        raw_results = payload.get("web", {}).get("results", [])
        if not isinstance(raw_results, list):
            return []

        results: list[WebSearchResultResponse] = []
        for item in raw_results:
            if not isinstance(item, dict):
                continue
            title = item.get("title")
            url = item.get("url")
            if not isinstance(title, str) or not isinstance(url, str):
                continue
            description = item.get("description")
            results.append(
                WebSearchResultResponse(
                    title=title,
                    url=url,
                    description=description if isinstance(description, str) else "",
                ),
            )
        return results
