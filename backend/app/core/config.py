from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BACKEND_DIR = Path(__file__).resolve().parents[2]


# env 임포트 설정
class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BACKEND_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "blanker API"
    debug: bool = False
    database_url: str = Field(
        default="postgresql+asyncpg://blanker:blanker@localhost:5432/blanker",
        alias="DATABASE_URL",
    )
    redis_url: str = Field(default="redis://localhost:6379/0", alias="REDIS_URL")
    jwt_secret_key: str = Field(default="change-me", alias="JWT_SECRET_KEY")
    jwt_algorithm: str = "HS256"
    access_token_expires_minutes: int = 30
    refresh_token_expires_days: int = 14
    anthropic_api_key: str | None = Field(default=None, alias="ANTHROPIC_API_KEY")
    ai_request_timeout_seconds: int = Field(
        default=30,
        alias="AI_REQUEST_TIMEOUT_SECONDS",
    )
    tmdb_access_token: str | None = Field(default=None, alias="TMDB_ACCESS_TOKEN")
    rawg_api_key: str | None = Field(default=None, alias="RAWG_API_KEY")
    aladin_ttb_key: str | None = Field(default=None, alias="ALADIN_TTB_KEY")
    kopis_service_key: str | None = Field(default=None, alias="KOPIS_SERVICE_KEY")


settings = Settings()
