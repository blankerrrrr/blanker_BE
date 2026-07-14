from typing import Any

from app.core.config import settings
from app.schemas.interest import InterestType
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
    assert items[0].genres == ["전체"]
    assert items[0].image_url == "https://example.com/webtoon.png"


def test_fetch_webtoons_skips_when_api_url_is_not_configured(
    monkeypatch,
) -> None:
    monkeypatch.setattr(settings, "korea_webtoon_api_url", None)

    assert import_interests.fetch_webtoons(10) == []
