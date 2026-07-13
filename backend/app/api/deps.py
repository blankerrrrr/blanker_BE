from collections.abc import AsyncGenerator

from fastapi import Header, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.cache.redis import create_redis_client
from app.cache.refresh_token_store import RefreshTokenStore
from app.core.error_codes import ErrorCode
from app.core.exceptions import AppException
from app.core.security import decode_access_token
from app.db.session import async_session


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


async def get_refresh_token_store() -> AsyncGenerator[RefreshTokenStore, None]:
    redis = create_redis_client()
    try:
        yield RefreshTokenStore(redis)
    finally:
        await redis.aclose()


async def get_current_user_id(
    authorization: str | None = Header(default=None, alias="Authorization"),
) -> str:
    if authorization is None or not authorization.startswith("Bearer "):
        raise AppException(
            ErrorCode.AUTH_UNAUTHORIZED,
            "인증 토큰이 필요합니다.",
            status.HTTP_401_UNAUTHORIZED,
        )

    user_id = decode_access_token(authorization.removeprefix("Bearer ").strip())
    if user_id is None:
        raise AppException(
            ErrorCode.AUTH_UNAUTHORIZED,
            "유효하지 않은 인증 토큰입니다.",
            status.HTTP_401_UNAUTHORIZED,
        )

    return user_id
