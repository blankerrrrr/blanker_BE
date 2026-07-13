import pytest

from app.core.exceptions import AppException
from app.services.token_service import TokenService


class FakeRefreshTokenStore:
    def __init__(self) -> None:
        self.values: dict[tuple[str, str], str] = {}

    async def save(self, user_id: str, token_id: str, token_hash: str) -> None:
        self.values[(user_id, token_id)] = token_hash

    async def get(self, user_id: str, token_id: str) -> str | None:
        return self.values.get((user_id, token_id))

    async def delete(self, user_id: str, token_id: str) -> None:
        self.values.pop((user_id, token_id), None)


@pytest.mark.asyncio
async def test_token_service_issues_and_validates_refresh_token() -> None:
    store = FakeRefreshTokenStore()
    service = TokenService(store)

    refresh_token = await service.issue_refresh_token("user_1")

    assert await service.validate_refresh_token(refresh_token) == "user_1"
    assert len(store.values) == 1


@pytest.mark.asyncio
async def test_token_service_rotates_refresh_token() -> None:
    store = FakeRefreshTokenStore()
    service = TokenService(store)
    old_refresh_token = await service.issue_refresh_token("user_1")

    user_id, new_refresh_token = await service.rotate_refresh_token(old_refresh_token)

    assert user_id == "user_1"
    assert new_refresh_token != old_refresh_token
    assert await service.validate_refresh_token(new_refresh_token) == "user_1"
    with pytest.raises(AppException):
        await service.validate_refresh_token(old_refresh_token)


@pytest.mark.asyncio
async def test_token_service_ignores_empty_delete() -> None:
    store = FakeRefreshTokenStore()
    service = TokenService(store)

    await service.delete_refresh_token(None)

    assert store.values == {}
