import hmac

from app.cache.refresh_token_store import RefreshTokenStore
from app.core.error_codes import ErrorCode
from app.core.exceptions import AppException
from app.core.security import (
    create_access_token,
    create_refresh_token,
    hash_token,
    parse_refresh_token,
)


class TokenService:
    def __init__(self, refresh_token_store: RefreshTokenStore) -> None:
        self.refresh_token_store = refresh_token_store

    def issue_access_token(self, user_id: str) -> tuple[str, int]:
        return create_access_token(user_id)

    async def issue_refresh_token(self, user_id: str) -> str:
        refresh_token, token_id = create_refresh_token(user_id)
        await self.refresh_token_store.save(
            user_id,
            token_id,
            hash_token(refresh_token),
        )
        return refresh_token

    async def rotate_refresh_token(self, refresh_token: str) -> tuple[str, str]:
        user_id = await self.validate_refresh_token(refresh_token)
        await self.delete_refresh_token(refresh_token)
        new_refresh_token = await self.issue_refresh_token(user_id)
        return user_id, new_refresh_token

    async def delete_refresh_token(self, refresh_token: str | None) -> None:
        if refresh_token is None:
            return
        parsed_token = parse_refresh_token(refresh_token)
        if parsed_token is not None:
            await self.refresh_token_store.delete(*parsed_token)

    async def validate_refresh_token(self, refresh_token: str) -> str:
        parsed_token = parse_refresh_token(refresh_token)
        if parsed_token is None:
            raise AppException(ErrorCode.AUTH_INVALID_REFRESH_TOKEN)

        user_id, token_id = parsed_token
        saved_hash = await self.refresh_token_store.get(user_id, token_id)
        if saved_hash is None:
            raise AppException(ErrorCode.AUTH_INVALID_REFRESH_TOKEN)

        if not hmac.compare_digest(saved_hash, hash_token(refresh_token)):
            raise AppException(ErrorCode.AUTH_INVALID_REFRESH_TOKEN)

        return user_id
