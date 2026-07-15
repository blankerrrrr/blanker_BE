import argparse
import asyncio
import html
import json
import re
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from typing import Any

from app.core.config import settings
from app.db.session import async_session
from app.schemas.interest import InterestType
from app.services.interest_catalog_import_service import (
    InterestCatalogImportService,
    InterestCatalogItem,
)


def _read_json(url: str, headers: dict[str, str] | None = None) -> dict[str, Any]:
    request = urllib.request.Request(url, headers=headers or {})
    with urllib.request.urlopen(request, timeout=20) as response:
        return json.loads(response.read().decode("utf-8"))


def _read_text(url: str) -> str:
    with urllib.request.urlopen(url, timeout=20) as response:
        return response.read().decode("utf-8")


def _tmdb_headers() -> dict[str, str]:
    if settings.tmdb_access_token is None:
        return {}
    return {"Authorization": f"Bearer {settings.tmdb_access_token}"}


def _tmdb_image(path: str | None) -> str | None:
    if path is None:
        return None
    return f"{settings.tmdb_image_url}{path}"


def _split_genres(value: str | None) -> list[str] | None:
    if not value:
        return None
    genres = [
        genre.strip()
        for part in value.split(",")
        for genre in part.split(">")
        if genre.strip()
    ]
    return list(dict.fromkeys(genres)) or None


def _first_string(value: Any) -> str | None:
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return next((item for item in value if isinstance(item, str)), None)
    return None


def _summary(value: Any) -> str | None:
    raw_value = _first_string(value)
    if raw_value is None:
        return None
    text = re.sub(r"<[^>]+>", " ", html.unescape(raw_value))
    text = " ".join(text.split())
    if not text:
        return None
    return text[:250]


def _summary_from_fields(raw_item: dict[str, Any], *keys: str) -> str | None:
    for key in keys:
        summary = _summary(raw_item.get(key))
        if summary is not None:
            return summary
    return None


def _tmdb_genres(media_type: str) -> dict[int, str]:
    if settings.tmdb_access_token is None:
        return {}
    payload = _read_json(
        f"{settings.tmdb_api_url}/genre/{media_type}/list?language=ko-KR",
        _tmdb_headers(),
    )
    return {
        int(item["id"]): item["name"]
        for item in payload.get("genres", [])
        if item.get("id") is not None and item.get("name")
    }


def _genre_names_from_ids(
    ids: list[int],
    genre_map: dict[int, str],
) -> list[str] | None:
    names = [genre_map[genre_id] for genre_id in ids if genre_id in genre_map]
    return list(dict.fromkeys(names)) or None


def _is_new_title(
    title: str,
    existing_titles: set[str],
    collected_titles: set[str],
) -> bool:
    return title not in existing_titles and title not in collected_titles


def fetch_tmdb_movies(
    limit: int,
    existing_titles: set[str] | None = None,
) -> list[InterestCatalogItem]:
    if settings.tmdb_access_token is None:
        return []
    genres = _tmdb_genres("movie")
    return _fetch_tmdb_pages(
        "/movie/popular",
        "title",
        InterestType.MOVIE,
        genres,
        limit,
        existing_titles or set(),
    )


def fetch_tmdb_dramas(
    limit: int,
    existing_titles: set[str] | None = None,
) -> list[InterestCatalogItem]:
    if settings.tmdb_access_token is None:
        return []
    genres = _tmdb_genres("tv")
    return _fetch_tmdb_pages(
        "/tv/popular",
        "name",
        InterestType.DRAMA,
        genres,
        limit,
        existing_titles or set(),
    )


def fetch_anime(
    limit: int,
    existing_titles: set[str] | None = None,
) -> list[InterestCatalogItem]:
    if settings.tmdb_access_token is None:
        return []
    genres = _tmdb_genres("tv")
    return _fetch_tmdb_pages(
        "/discover/tv",
        "name",
        InterestType.ANIMATION,
        genres,
        limit,
        existing_titles or set(),
        {"with_genres": 16, "sort_by": "popularity.desc"},
    )


def _fetch_tmdb_pages(
    path: str,
    title_key: str,
    interest_type: InterestType,
    genres: dict[int, str],
    limit: int,
    existing_titles: set[str],
    extra_params: dict[str, Any] | None = None,
) -> list[InterestCatalogItem]:
    items: list[InterestCatalogItem] = []
    collected_titles: set[str] = set()
    page = 1
    while len(items) < limit:
        query = urllib.parse.urlencode(
            {"language": "ko-KR", "page": page, **(extra_params or {})},
        )
        payload = _read_json(f"{settings.tmdb_api_url}{path}?{query}", _tmdb_headers())
        results = payload.get("results", [])
        if not results:
            break
        for raw_item in results:
            title = raw_item.get(title_key)
            if not title or not _is_new_title(
                title,
                existing_titles,
                collected_titles,
            ):
                continue
            items.append(
                InterestCatalogItem(
                    interest_type=interest_type,
                    title=title,
                    genres=_genre_names_from_ids(
                        raw_item.get("genre_ids", []),
                        genres,
                    ),
                    summary=_summary(raw_item.get("overview")),
                    image_url=_tmdb_image(raw_item.get("poster_path")),
                ),
            )
            collected_titles.add(title)
            if len(items) == limit:
                break
        if page >= int(payload.get("total_pages", page)):
            break
        page += 1
    return items


def fetch_books(
    limit: int,
    existing_titles: set[str] | None = None,
) -> list[InterestCatalogItem]:
    if settings.aladin_ttb_key is None:
        return []
    existing_titles = existing_titles or set()
    items: list[InterestCatalogItem] = []
    collected_titles: set[str] = set()
    page = 1
    while len(items) < limit:
        query = urllib.parse.urlencode(
            {
                "ttbkey": settings.aladin_ttb_key,
                "QueryType": "Bestseller",
                "SearchTarget": "Book",
                "output": "js",
                "Version": "20131101",
                "MaxResults": min(limit, 50),
                "start": page,
            },
        )
        payload = _read_json(f"{settings.aladin_api_url}/ItemList.aspx?{query}")
        results = payload.get("item", [])
        for raw_item in results:
            title = raw_item.get("title")
            if not title or not _is_new_title(
                title,
                existing_titles,
                collected_titles,
            ):
                continue
            items.append(
                InterestCatalogItem(
                    interest_type=InterestType.NOVEL,
                    title=title,
                    genres=_split_genres(raw_item.get("categoryName")),
                    summary=_summary(raw_item.get("description")),
                    image_url=raw_item.get("cover"),
                ),
            )
            collected_titles.add(title)
            if len(items) == limit:
                break
        if not results or len(results) < min(limit, 50) or page >= 100:
            break
        page += 1
    return items


def fetch_games(
    limit: int,
    existing_titles: set[str] | None = None,
) -> list[InterestCatalogItem]:
    if settings.rawg_api_key is None:
        return []
    existing_titles = existing_titles or set()
    items: list[InterestCatalogItem] = []
    collected_titles: set[str] = set()
    page = 1
    while len(items) < limit:
        query = urllib.parse.urlencode(
            {
                "key": settings.rawg_api_key,
                "ordering": "-rating",
                "page": page,
                "page_size": min(limit, 40),
            },
        )
        payload = _read_json(f"{settings.rawg_api_url}/games?{query}")
        results = payload.get("results", [])
        for raw_item in results:
            title = raw_item.get("name")
            if not title or not _is_new_title(
                title,
                existing_titles,
                collected_titles,
            ):
                continue
            items.append(
                InterestCatalogItem(
                    interest_type=InterestType.GAME,
                    title=title,
                    genres=[
                        genre["name"]
                        for genre in raw_item.get("genres", [])
                        if genre.get("name")
                    ]
                    or None,
                    summary=_summary_from_fields(
                        raw_item,
                        "description_raw",
                        "description",
                    ),
                    image_url=raw_item.get("background_image"),
                ),
            )
            collected_titles.add(title)
            if len(items) == limit:
                break
        if not results or payload.get("next") is None or page >= 100:
            break
        page += 1
    return items


def _fetch_kopis_summary(performance_id: str | None) -> str | None:
    if not performance_id:
        return None
    try:
        node = ET.fromstring(
            _read_text(
                f"{settings.kopis_api_url}/pblprfr/{performance_id}"
                f"?service={settings.kopis_service_key}",
            ),
        ).find("db")
    except Exception:
        return None
    if node is None:
        return None
    return _summary(node.findtext("sty"))


def fetch_musicals(
    limit: int,
    existing_titles: set[str] | None = None,
) -> list[InterestCatalogItem]:
    if settings.kopis_service_key is None:
        return []
    items: list[InterestCatalogItem] = []
    existing_titles = existing_titles or set()
    collected_titles: set[str] = set()
    page = 1
    while len(items) < limit:
        url = (
            f"{settings.kopis_api_url}/pblprfr"
            f"?service={settings.kopis_service_key}"
            "&stdate=20260101&eddate=20261231"
            f"&cpage={page}&rows={min(limit, 100)}&shcate=GGGD"
        )
        nodes = ET.fromstring(_read_text(url)).findall("db")
        for node in nodes:
            title = node.findtext("prfnm")
            if not title or not _is_new_title(
                title,
                existing_titles,
                collected_titles,
            ):
                continue
            items.append(
                InterestCatalogItem(
                    interest_type=InterestType.MUSICAL,
                    title=title,
                    genres=_split_genres(node.findtext("genrenm") or "뮤지컬"),
                    summary=_fetch_kopis_summary(node.findtext("mt20id")),
                    image_url=node.findtext("poster"),
                ),
            )
            collected_titles.add(title)
            if len(items) == limit:
                break
        if not nodes or len(nodes) < min(limit, 100) or page >= 100:
            break
        page += 1
    return items


def fetch_webtoons(
    limit: int,
    existing_titles: set[str] | None = None,
) -> list[InterestCatalogItem]:
    if settings.korea_webtoon_api_url is None:
        return []
    existing_titles = existing_titles or set()
    items: list[InterestCatalogItem] = []
    collected_titles: set[str] = set()
    page = 1
    while len(items) < limit:
        params = {"perPage": limit}
        if page > 1:
            params["page"] = page
        query = urllib.parse.urlencode(params)
        payload = _read_json(f"{settings.korea_webtoon_api_url}/webtoons?{query}")
        results = payload.get("webtoons", [])
        for raw_item in results:
            title = raw_item.get("title")
            if not title or not _is_new_title(
                title,
                existing_titles,
                collected_titles,
            ):
                continue
            items.append(
                InterestCatalogItem(
                    interest_type=InterestType.WEBTOON,
                    title=title,
                    genres=_split_genres(
                        raw_item.get("genre") or raw_item.get("genreNm"),
                    ),
                    summary=_summary_from_fields(
                        raw_item,
                        "summary",
                        "description",
                        "synopsis",
                        "story",
                        "contents",
                    ),
                    image_url=_first_string(raw_item.get("thumbnail")),
                ),
            )
            collected_titles.add(title)
            if len(items) == limit:
                break
        if not results or len(results) < limit or page >= 100:
            break
        page += 1
    return items


def fetch_all(
    limit: int,
    existing_titles: dict[InterestType, set[str]] | None = None,
) -> list[InterestCatalogItem]:
    items: list[InterestCatalogItem] = []
    fetchers = (
        fetch_tmdb_movies,
        fetch_tmdb_dramas,
        fetch_anime,
        fetch_books,
        fetch_games,
        fetch_musicals,
        fetch_webtoons,
    )
    for fetcher in fetchers:
        try:
            interest_type = {
                fetch_tmdb_movies: InterestType.MOVIE,
                fetch_tmdb_dramas: InterestType.DRAMA,
                fetch_anime: InterestType.ANIMATION,
                fetch_books: InterestType.NOVEL,
                fetch_games: InterestType.GAME,
                fetch_musicals: InterestType.MUSICAL,
                fetch_webtoons: InterestType.WEBTOON,
            }[fetcher]
            items.extend(fetcher(limit, (existing_titles or {}).get(interest_type)))
        except Exception as exc:
            print(f"{fetcher.__name__} failed: {exc}")
    return items


async def main() -> None:
    parser = argparse.ArgumentParser(description="Import interests from external APIs")
    parser.add_argument("--limit", type=int, default=20)
    args = parser.parse_args()

    async with async_session() as session:
        repository = InterestCatalogImportService(session).interests
        pairs = await repository.find_type_title_pairs()
    existing_titles = {
        interest_type: {
            title for type_name, title in pairs if type_name == interest_type.value
        }
        for interest_type in InterestType
    }
    items = await asyncio.to_thread(fetch_all, args.limit, existing_titles)
    async with async_session() as session:
        imported_count = await InterestCatalogImportService(session).import_items(items)
    print(f"fetched={len(items)} imported={imported_count}")


if __name__ == "__main__":
    asyncio.run(main())
