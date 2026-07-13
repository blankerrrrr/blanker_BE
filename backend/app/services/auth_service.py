import hmac

from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession

from app.cache.refresh_token_store import RefreshTokenStore
from app.core.error_codes import ErrorCode
from app.core.exceptions import AppException
from app.core.id_generator import generate_public_id
from app.core.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    hash_token,
    parse_refresh_token,
    verify_password,
)
from app.db.models.user import User
from app.db.repositories.user_repository import UserRepository
from app.schemas.auth import LoginResponse, SignupRequest, SignupResponse, TokenResponse
from app.schemas.user import LoginUserResponse, UserResponse


class AuthService:
    def __init__(
        self,
        session: AsyncSession,
        refresh_token_store: RefreshTokenStore,
    ) -> None:
        self.session = session
        self.users = UserRepository(session)
        self.refresh_token_store = refresh_token_store

    async def signup(self, request: SignupRequest) -> SignupResponse:
        if not request.terms_agreed or not request.privacy_agreed:
            raise AppException(
                ErrorCode.AUTH_REQUIRED_AGREEMENT_MISSING,
                "필수 약관에 동의해야 합니다.",
                status.HTTP_400_BAD_REQUEST,
            )

        if len(request.password) < 8:
            raise AppException(
                ErrorCode.AUTH_WEAK_PASSWORD,
                "비밀번호는 8자 이상이어야 합니다.",
                status.HTTP_400_BAD_REQUEST,
            )

        existing_user = await self.users.get_by_email(request.email)
        if existing_user is not None:
            raise AppException(
                ErrorCode.AUTH_EMAIL_ALREADY_EXISTS,
                "이미 가입된 이메일입니다.",
                status.HTTP_409_CONFLICT,
            )

        user = User(
            user_id=generate_public_id("user_"),
            email=request.email,
            password_hash=hash_password(request.password),
        )
        await self.users.save(user)
        await self.session.commit()
        return SignupResponse.model_validate(
            self._user_response(user),
            from_attributes=True,
        )

    async def login(self, email: str, password: str) -> tuple[LoginResponse, str]:
        user = await self.users.get_by_email(email)
        if user is None or not verify_password(password, user.password_hash):
            raise AppException(
                ErrorCode.AUTH_INVALID_CREDENTIALS,
                "이메일 또는 비밀번호가 올바르지 않습니다.",
                status.HTTP_401_UNAUTHORIZED,
            )

        if not user.is_active:
            raise AppException(
                ErrorCode.AUTH_ACCOUNT_DISABLED,
                "비활성화된 계정입니다.",
                status.HTTP_403_FORBIDDEN,
            )

        access_token, expires_in = create_access_token(user.user_id)
        refresh_token = await self._issue_refresh_token(user.user_id)
        return (
            LoginResponse(
                accessToken=access_token,
                expiresIn=expires_in,
                user=LoginUserResponse(userId=user.user_id, email=user.email),
            ),
            refresh_token,
        )

    async def refresh(self, refresh_token: str) -> tuple[TokenResponse, str]:
        user_id = await self._validate_refresh_token(refresh_token)
        access_token, expires_in = create_access_token(user_id)

        old_token = parse_refresh_token(refresh_token)
        if old_token is not None:
            await self.refresh_token_store.delete(*old_token)

        new_refresh_token = await self._issue_refresh_token(user_id)
        return (
            TokenResponse(accessToken=access_token, expiresIn=expires_in),
            new_refresh_token,
        )

    async def logout(self, refresh_token: str | None) -> None:
        if refresh_token is None:
            return
        parsed_token = parse_refresh_token(refresh_token)
        if parsed_token is not None:
            await self.refresh_token_store.delete(*parsed_token)

    async def get_current_user(self, user_id: str) -> UserResponse:
        user = await self.users.get_by_user_id(user_id)
        if user is None:
            raise AppException(
                ErrorCode.USER_NOT_FOUND,
                "사용자를 찾을 수 없습니다.",
                status.HTTP_404_NOT_FOUND,
            )
        return UserResponse.model_validate(
            self._user_response(user),
            from_attributes=True,
        )

    async def _issue_refresh_token(self, user_id: str) -> str:
        refresh_token, token_id = create_refresh_token(user_id)
        await self.refresh_token_store.save(
            user_id,
            token_id,
            hash_token(refresh_token),
        )
        return refresh_token

    async def _validate_refresh_token(self, refresh_token: str) -> str:
        parsed_token = parse_refresh_token(refresh_token)
        if parsed_token is None:
            raise AppException(
                ErrorCode.AUTH_INVALID_REFRESH_TOKEN,
                "유효하지 않은 refresh token입니다.",
                status.HTTP_401_UNAUTHORIZED,
            )

        user_id, token_id = parsed_token
        saved_hash = await self.refresh_token_store.get(user_id, token_id)
        if saved_hash is None:
            raise AppException(
                ErrorCode.AUTH_INVALID_REFRESH_TOKEN,
                "유효하지 않은 refresh token입니다.",
                status.HTTP_401_UNAUTHORIZED,
            )

        if not hmac.compare_digest(saved_hash, hash_token(refresh_token)):
            raise AppException(
                ErrorCode.AUTH_INVALID_REFRESH_TOKEN,
                "유효하지 않은 refresh token입니다.",
                status.HTTP_401_UNAUTHORIZED,
            )

        return user_id

    def _user_response(self, user: User) -> dict[str, object]:
        return {
            "userId": user.user_id,
            "email": user.email,
            "createdAt": user.created_at,
        }
