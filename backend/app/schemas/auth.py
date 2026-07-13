from app.schemas.common import CamelModel
from app.schemas.user import LoginUserResponse, UserResponse


class SignupRequest(CamelModel):
    email: str
    password: str
    terms_agreed: bool
    privacy_agreed: bool


class LoginRequest(CamelModel):
    email: str
    password: str


class SignupResponse(UserResponse):
    pass


class TokenResponse(CamelModel):
    access_token: str
    token_type: str = "Bearer"
    expires_in: int


class LoginResponse(TokenResponse):
    user: LoginUserResponse
