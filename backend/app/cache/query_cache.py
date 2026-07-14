import hashlib
import json
from typing import TypeVar

from pydantic import ValidationError
from redis.asyncio import Redis
from redis.exceptions import RedisError

from app.schemas.common import CamelModel

T = TypeVar("T", bound=CamelModel)


class QueryCache:
    def __init__(self, redis: Redis) -> None:
        self.redis = redis

    async def get_model(self, key: str, model_type: type[T]) -> T | None:
        try:
            cached = await self.redis.get(key)
        except RedisError:
            return None

        if not isinstance(cached, str):
            return None

        try:
            return model_type.model_validate(json.loads(cached))
        except (json.JSONDecodeError, ValidationError, TypeError, ValueError):
            return None

    async def set_model(self, key: str, value: CamelModel, ttl_seconds: int) -> None:
        payload = json.dumps(
            value.model_dump(mode="json", by_alias=True),
            ensure_ascii=False,
        )
        try:
            await self.redis.set(key, payload, ex=ttl_seconds)
        except RedisError:
            return

    @staticmethod
    def key(namespace: str, params: dict[str, object]) -> str:
        normalized = json.dumps(params, ensure_ascii=False, sort_keys=True)
        digest = hashlib.sha256(normalized.encode("utf-8")).hexdigest()
        return f"query:{namespace}:{digest}"
