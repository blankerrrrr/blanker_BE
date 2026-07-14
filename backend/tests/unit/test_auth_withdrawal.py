from collections.abc import AsyncGenerator

from fastapi.testclient import TestClient

from app.api.deps import get_current_user_id, get_db_session, get_refresh_token_store
from app.main import app


class FakeAuthService:
    withdrawn_user_id: str | None = None

    def __init__(self, session: object, refresh_token_store: object) -> None:
        self.session = session
        self.refresh_token_store = refresh_token_store

    async def withdraw(self, user_id: str) -> None:
        FakeAuthService.withdrawn_user_id = user_id


async def fake_db_session() -> AsyncGenerator[object, None]:
    yield object()


async def fake_refresh_token_store() -> AsyncGenerator[object, None]:
    yield object()


async def fake_current_user_id() -> str:
    return "user_1"


def test_withdraw_calls_service_and_returns_200(monkeypatch) -> None:
    from app.api import auth

    FakeAuthService.withdrawn_user_id = None
    monkeypatch.setattr(auth, "AuthService", FakeAuthService)
    app.dependency_overrides[get_db_session] = fake_db_session
    app.dependency_overrides[get_refresh_token_store] = fake_refresh_token_store
    app.dependency_overrides[get_current_user_id] = fake_current_user_id
    client = TestClient(app)

    response = client.delete("/api/auth/me")

    app.dependency_overrides.clear()
    assert response.status_code == 200
    assert response.json() == {"success": True, "data": None}
    assert FakeAuthService.withdrawn_user_id == "user_1"


def test_withdraw_clears_refresh_token_cookie(monkeypatch) -> None:
    from app.api import auth

    monkeypatch.setattr(auth, "AuthService", FakeAuthService)
    app.dependency_overrides[get_db_session] = fake_db_session
    app.dependency_overrides[get_refresh_token_store] = fake_refresh_token_store
    app.dependency_overrides[get_current_user_id] = fake_current_user_id
    client = TestClient(app)

    response = client.delete("/api/auth/me")

    app.dependency_overrides.clear()
    assert response.status_code == 200
    set_cookie = response.headers.get("set-cookie", "")
    assert "refreshToken" in set_cookie
    assert "Max-Age=0" in set_cookie or 'expires=Thu, 01 Jan 1970' in set_cookie


def test_withdraw_requires_auth() -> None:
    client = TestClient(app, raise_server_exceptions=False)

    response = client.delete("/api/auth/me")

    assert response.status_code == 401
