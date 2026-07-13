from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
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
    openai_api_key: str | None = Field(default=None, alias="OPENAI_API_KEY")
    openai_request_timeout_seconds: int = Field(
        default=30,
        alias="OPENAI_REQUEST_TIMEOUT_SECONDS",
    )


settings = Settings()
