from typing import Annotated

from fastapi import APIRouter, Cookie, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import (
    get_current_user_id,
    get_db_session,
    get_refresh_token_store,
)
from app.cache.refresh_token_store import RefreshTokenStore
from app.core.config import settings
from app.core.error_codes import ErrorCode
from app.core.exceptions import AppException
from app.core.response import success_response
from app.schemas.auth import LoginRequest, SignupRequest
from app.services.auth_service import AuthService

router = APIRouter()

DbSession = Annotated[AsyncSession, Depends(get_db_session)]
RefreshStore = Annotated[RefreshTokenStore, Depends(get_refresh_token_store)]
CurrentUserId = Annotated[str, Depends(get_current_user_id)]
RefreshTokenCookie = Annotated[
    str | None,
    Cookie(alias="refreshToken"),
]


@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(
    request: SignupRequest,
    session: DbSession,
    refresh_token_store: RefreshStore,
) -> dict[str, object]:
    service = AuthService(session, refresh_token_store)
    result = await service.signup(request)
    return success_response(result.model_dump(mode="json", by_alias=True))


@router.post("/login")
async def login(
    request: LoginRequest,
    response: Response,
    session: DbSession,
    refresh_token_store: RefreshStore,
) -> dict[str, object]:
    service = AuthService(session, refresh_token_store)
    result, refresh_token = await service.login(request.email, request.password)
    _set_refresh_token_cookie(response, refresh_token)
    return success_response(result.model_dump(mode="json", by_alias=True))


@router.post("/refresh")
async def refresh(
    response: Response,
    session: DbSession,
    refresh_token_store: RefreshStore,
    refresh_token: RefreshTokenCookie = None,
) -> dict[str, object]:
    if refresh_token is None:
        raise AppException(ErrorCode.AUTH_REFRESH_TOKEN_COOKIE_MISSING)

    service = AuthService(session, refresh_token_store)
    result, new_refresh_token = await service.refresh(refresh_token)
    _set_refresh_token_cookie(response, new_refresh_token)
    return success_response(result.model_dump(mode="json", by_alias=True))


@router.post("/logout")
async def logout(
    response: Response,
    session: DbSession,
    refresh_token_store: RefreshStore,
    refresh_token: RefreshTokenCookie = None,
) -> dict[str, object]:
    service = AuthService(session, refresh_token_store)
    await service.logout(refresh_token)
    response.delete_cookie(key="refreshToken", path="/api/auth")
    return success_response(None)


@router.get("/me")
async def me(
    user_id: CurrentUserId,
    session: DbSession,
    refresh_token_store: RefreshStore,
) -> dict[str, object]:
    service = AuthService(session, refresh_token_store)
    result = await service.get_current_user(user_id)
    return success_response(result.model_dump(mode="json", by_alias=True))


@router.delete("/me")
async def withdraw(
    response: Response,
    user_id: CurrentUserId,
    session: DbSession,
    refresh_token_store: RefreshStore,
) -> dict[str, object]:
    service = AuthService(session, refresh_token_store)
    await service.withdraw(user_id)
    response.delete_cookie(key="refreshToken", path="/api/auth")
    return success_response(None)


def _set_refresh_token_cookie(response: Response, refresh_token: str) -> None:
    response.set_cookie(
        key="refreshToken",
        value=refresh_token,
        max_age=settings.refresh_token_expires_days * 24 * 60 * 60,
        httponly=True,
        secure=True,
        samesite="none",
        path="/api/auth",
    )
