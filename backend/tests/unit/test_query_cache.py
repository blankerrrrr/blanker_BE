import json

import pytest

from app.cache.query_cache import QueryCache
from app.schemas.interest import InterestTypeListResponse, InterestTypeResponse


class FakeRedis:
    def __init__(self) -> None:
        self.values: dict[str, str] = {}
        self.ttls: dict[str, int] = {}

    async def get(self, key: str) -> str | None:
        return self.values.get(key)

    async def set(self, key: str, value: str, ex: int) -> None:
        self.values[key] = value
        self.ttls[key] = ex


@pytest.mark.asyncio
async def test_query_cache_round_trips_camel_model() -> None:
    redis = FakeRedis()
    cache = QueryCache(redis)  # type: ignore[arg-type]
    key = QueryCache.key("interests:types", {})
    response = InterestTypeListResponse(
        items=[InterestTypeResponse(name="게임", image_url="https://example.com/a.jpg")],
    )

    await cache.set_model(key, response, ttl_seconds=600)
    cached = await cache.get_model(key, InterestTypeListResponse)

    assert cached == response
    assert redis.ttls[key] == 600
    assert json.loads(redis.values[key]) == {
        "items": [{"name": "게임", "imageUrl": "https://example.com/a.jpg"}],
    }


def test_query_cache_key_is_stable_for_param_order() -> None:
    first = QueryCache.key("interests:list", {"genre": "Action", "keyword": None})
    second = QueryCache.key("interests:list", {"keyword": None, "genre": "Action"})

    assert first == second
