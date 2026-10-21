"""Application configuration using Pydantic Settings."""

from functools import lru_cache

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

DEFAULT_SECRET_KEY = "your-secret-key-change-in-production"


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # App
    app_name: str = "Aye House API"
    app_version: str = "0.1.0"
    debug: bool = False
    environment: str = "development"

    # API
    api_prefix: str = "/api/v1"

    # Database
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/aye_house"
    database_pool_size: int = 5
    database_max_overflow: int = 10

    # Security
    secret_key: str = DEFAULT_SECRET_KEY
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # CORS
    cors_origins: list[str] = ["http://localhost:3000", "http://localhost:5173"]
    cors_allow_credentials: bool = True
    cors_allow_methods: list[str] = ["*"]
    cors_allow_headers: list[str] = ["*"]

    @model_validator(mode="after")
    def _require_secret_key_in_production(self) -> "Settings":
        # Anyone knowing the default key could forge valid JWTs
        if self.environment == "production" and self.secret_key == DEFAULT_SECRET_KEY:
            raise ValueError("SECRET_KEY must be set in production")
        return self


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
