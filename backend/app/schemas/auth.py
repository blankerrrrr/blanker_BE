from pydantic import BaseModel, ConfigDict, Field

from app.schemas.user import LoginUserResponse, UserResponse


class SignupRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    email: str
    password: str
    terms_agreed: bool = Field(alias="termsAgreed")
    privacy_agreed: bool = Field(alias="privacyAgreed")


class LoginRequest(BaseModel):
    email: str
    password: str


class SignupResponse(UserResponse):
    pass


class TokenResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    access_token: str = Field(alias="accessToken")
    token_type: str = Field(default="Bearer", alias="tokenType")
    expires_in: int = Field(alias="expiresIn")


class LoginResponse(TokenResponse):
    user: LoginUserResponse
