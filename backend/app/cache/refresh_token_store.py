from redis.asyncio import Redis

from app.core.config import settings


class RefreshTokenStore:
    def __init__(self, redis: Redis) -> None:
        self.redis = redis

    async def save(self, user_id: str, token_id: str, token_hash: str) -> None:
        await self.redis.set(
            self._key(user_id, token_id),
            token_hash,
            ex=settings.refresh_token_expires_days * 24 * 60 * 60,
        )

    async def get(self, user_id: str, token_id: str) -> str | None:
        value = await self.redis.get(self._key(user_id, token_id))
        return value if isinstance(value, str) else None

    async def delete(self, user_id: str, token_id: str) -> None:
        await self.redis.delete(self._key(user_id, token_id))

    async def delete_all_by_user_id(self, user_id: str) -> None:
        keys = await self.redis.keys(f"auth:refresh:{user_id}:*")
        if keys:
            await self.redis.delete(*keys)

    @staticmethod
    def _key(user_id: str, token_id: str) -> str:
        return f"auth:refresh:{user_id}:{token_id}"
