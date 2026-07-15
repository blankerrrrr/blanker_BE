from typing import Any

from app.core.config import settings
from app.schemas.interest import InterestType
from app.services.interest_catalog_import_service import InterestCatalogImportService
from scripts import import_interests


def test_fetch_webtoons_uses_configured_api_url(
    monkeypatch,
) -> None:
    requested_urls: list[str] = []

    def fake_read_json(
        url: str,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        requested_urls.append(url)
        return {
            "webtoons": [
                {
                    "title": "테스트 웹툰",
                    "thumbnail": [
                        "https://example.com/webtoon.png",
                    ],
                    "description": "테스트 웹툰 설명",
                },
            ],
        }

    monkeypatch.setattr(settings, "korea_webtoon_api_url", "http://webtoon-api:3000")
    monkeypatch.setattr(import_interests, "_read_json", fake_read_json)

    items = import_interests.fetch_webtoons(10)

    assert requested_urls == ["http://webtoon-api:3000/webtoons?perPage=10"]
    assert len(items) == 1
    assert items[0].interest_type == InterestType.WEBTOON
    assert items[0].title == "테스트 웹툰"
    assert items[0].genres is None
    assert items[0].summary == "테스트 웹툰 설명"
    assert items[0].image_url == "https://example.com/webtoon.png"


def test_fetch_webtoons_skips_when_api_url_is_not_configured(
    monkeypatch,
) -> None:
    monkeypatch.setattr(settings, "korea_webtoon_api_url", None)

    assert import_interests.fetch_webtoons(10) == []


def test_fetch_tmdb_movies_skips_existing_titles_and_reads_next_page(
    monkeypatch,
) -> None:
    requested_urls: list[str] = []

    def fake_read_json(
        url: str,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        requested_urls.append(url)
        if "/genre/" in url:
            return {"genres": []}
        if "page=1" in url:
            return {
                "results": [{"title": "기존 영화", "overview": "기존 설명"}],
                "total_pages": 2,
            }
        return {
            "results": [{"title": "새 영화", "overview": "새 영화 설명"}],
            "total_pages": 2,
        }

    monkeypatch.setattr(settings, "tmdb_access_token", "token")
    monkeypatch.setattr(import_interests, "_read_json", fake_read_json)

    items = import_interests.fetch_tmdb_movies(1, {"기존 영화"})

    assert [item.title for item in items] == ["새 영화"]
    assert items[0].summary == "새 영화 설명"
    assert any("page=2" in url for url in requested_urls)


def test_summary_normalizes_html_and_limits_length() -> None:
    text = "<p>요약&nbsp;내용</p>" + "가" * 300

    assert import_interests._summary(text) == ("요약 내용 " + "가" * 300)[:250]


def test_import_service_limits_summary_to_250_chars() -> None:
    summary = "가" * 251

    assert InterestCatalogImportService._normalize_summary(summary) == "가" * 250
