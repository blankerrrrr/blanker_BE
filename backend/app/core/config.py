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
    tmdb_api_url: str = Field(
        default="https://api.themoviedb.org/3",
        alias="TMDB_API_URL",
    )
    tmdb_image_url: str = Field(
        default="https://image.tmdb.org/t/p/w500",
        alias="TMDB_IMAGE_URL",
    )
    rawg_api_key: str | None = Field(default=None, alias="RAWG_API_KEY")
    rawg_api_url: str = Field(default="https://api.rawg.io/api", alias="RAWG_API_URL")
    aladin_ttb_key: str | None = Field(default=None, alias="ALADIN_TTB_KEY")
    aladin_api_url: str = Field(
        default="http://www.aladin.co.kr/ttb/api",
        alias="ALADIN_API_URL",
    )
    kopis_service_key: str | None = Field(default=None, alias="KOPIS_SERVICE_KEY")
    kopis_api_url: str = Field(
        default="http://www.kopis.or.kr/openApi/restful",
        alias="KOPIS_API_URL",
    )
    korea_webtoon_api_url: str | None = Field(
        default=None,
        alias="KOREA_WEBTOON_API_URL",
    )
    tesseract_cmd: str | None = Field(default=None, alias="TESSERACT_CMD")
    tessdata_prefix: str | None = Field(default=None, alias="TESSDATA_PREFIX")
    aws_bucket: str | None = Field(default=None, alias="AWS_BUCKET")
    aws_region: str = Field(default="ap-northeast-2", alias="AWS_REGION")
    aws_access_key_id: str | None = Field(default=None, alias="AWS_ACCESS_KEY_ID")
    aws_secret_access_key: str | None = Field(
        default=None,
        alias="AWS_SECRET_ACCESS_KEY",
    )


settings = Settings()
