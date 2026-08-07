"""Typed and centralized StudyHive runtime configuration."""

from enum import StrEnum
from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(StrEnum):
    """Supported runtime configuration profiles."""

    DEVELOPMENT = "development"
    TEST = "test"
    CI = "ci"
    STAGING = "staging"
    PRODUCTION = "production"


class Settings(BaseSettings):
    """Validated process configuration read once at the composition boundary."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="STUDYHIVE_",
        extra="ignore",
        case_sensitive=False,
    )

    environment: Environment = Environment.DEVELOPMENT
    log_level: str = "INFO"
    api_host: str = "127.0.0.1"
    api_port: int = Field(default=8000, ge=1, le=65535)
    database_url: str = "postgresql+asyncpg://studyhive:studyhive@localhost:5432/studyhive"
    redis_url: str = "redis://localhost:6379/0"
    storage_path: Path = Path(".data/storage")
    web_origin: str = "http://localhost:3000"
    session_cookie_name: str = "studyhive_session"
    csrf_cookie_name: str = "studyhive_csrf"
    session_cookie_secure: bool = False
    session_idle_minutes: int = Field(default=60, ge=5, le=1440)
    session_absolute_hours: int = Field(default=8, ge=1, le=168)
    session_remember_days: int = Field(default=30, ge=1, le=90)
    recent_authentication_minutes: int = Field(default=15, ge=5, le=60)
    password_min_length: int = Field(default=12, ge=10, le=64)
    password_max_length: int = Field(default=128, ge=64, le=1024)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return the validated process settings singleton."""

    return Settings()
