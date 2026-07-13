from datetime import datetime

from app.schemas.common import CamelModel


class UserResponse(CamelModel):
    user_id: str
    email: str
    created_at: datetime


class LoginUserResponse(CamelModel):
    user_id: str
    email: str
