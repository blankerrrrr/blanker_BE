from sqlalchemy.ext.asyncio import AsyncSession

from app.cache.refresh_token_store import RefreshTokenStore
from app.core.error_codes import ErrorCode
from app.core.exceptions import AppException
from app.core.security import hash_password, verify_password
from app.db.models.user import User
from app.db.repositories.user_repository import UserRepository
from app.schemas.auth import LoginResponse, SignupRequest, SignupResponse, TokenResponse
from app.schemas.user import LoginUserResponse, UserResponse
from app.services.token_service import TokenService


class AuthService:
    def __init__(
        self,
        session: AsyncSession,
        refresh_token_store: RefreshTokenStore,
    ) -> None:
        self.session = session
        self.users = UserRepository(session)
        self.tokens = TokenService(refresh_token_store)

    # 회원가입
    async def signup(self, request: SignupRequest) -> SignupResponse:
        if len(request.password) < 8:
            raise AppException(ErrorCode.AUTH_WEAK_PASSWORD)

        existing_user = await self.users.get_by_email(request.email)
        if existing_user is not None:
            raise AppException(ErrorCode.AUTH_EMAIL_ALREADY_EXISTS)

        user = User(
            email=request.email,
            password_hash=hash_password(request.password),
        )
        await self.users.save(user)
        await self.session.commit()
        return SignupResponse.model_validate(
            self._user_response(user),
            from_attributes=True,
        )

    # 로그인
    async def login(self, email: str, password: str) -> tuple[LoginResponse, str]:
        user = await self.users.get_by_email(email)
        if user is None or not verify_password(password, user.password_hash):
            raise AppException(ErrorCode.AUTH_INVALID_CREDENTIALS)

        if not user.is_active:
            raise AppException(ErrorCode.AUTH_ACCOUNT_DISABLED)

        access_token, expires_in = self.tokens.issue_access_token(user.user_id)
        refresh_token = await self.tokens.issue_refresh_token(user.user_id)
        return (
            LoginResponse(
                accessToken=access_token,
                expiresIn=expires_in,
                user=LoginUserResponse(userId=user.user_id, email=user.email),
            ),
            refresh_token,
        )

    # 토큰 재발급
    async def refresh(self, refresh_token: str) -> tuple[TokenResponse, str]:
        user_id, new_refresh_token = await self.tokens.rotate_refresh_token(
            refresh_token,
        )
        access_token, expires_in = self.tokens.issue_access_token(user_id)
        return (
            TokenResponse(accessToken=access_token, expiresIn=expires_in),
            new_refresh_token,
        )

    # 로그아웃
    async def logout(self, refresh_token: str | None) -> None:
        await self.tokens.delete_refresh_token(refresh_token)

    # 유저 정보 가져오기
    async def get_current_user(self, user_id: str) -> UserResponse:
        user = await self.users.get_by_user_id(user_id)
        if user is None:
            raise AppException(ErrorCode.USER_NOT_FOUND)
        return UserResponse.model_validate(
            self._user_response(user),
            from_attributes=True,
        )

    def _user_response(self, user: User) -> dict[str, object]:
        return {
            "userId": user.user_id,
            "email": user.email,
            "createdAt": user.created_at,
        }
