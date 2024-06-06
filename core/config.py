import os
import secrets
from functools import lru_cache
from pathlib import Path
from typing import List, Literal, Union

from pydantic import AnyHttpUrl, validator
from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_FILE_PATH = Path(__file__).resolve().parent.parent / ".env"


class Settings(BaseSettings):
    PROJECT_NAME: str = (
        f"FastAPI Server - {os.getenv('ENV', 'development').capitalize()}"
    )
    DESCRIPTION: str = "MillionVue API"
    ENV: Literal["development", "staging", "production"] = "development"
    VERSION: str = "0.1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    DATABASE_URI: str = os.getenv(
        "DATABASE_URI", "postgresql://localhost:5432/millionvue"
    )
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = ["http://localhost:8000", "https://www.millionvue.com"]
    DEBUG: bool = False

    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_REGION_DEFAULT: str = "us-east-1"

    OAUTH_PROVIDER: str
    OAUTH_PROVIDER_CLIENT_ID: str
    OAUTH_PROVIDER_CLIENT_DOMAIN: str
    OAUTH_PROVIDER_CLIENT_SECRET: str
    OAUTH_PROVIDER_CALLBACK_URL: str
    OAUTH_PROVIDER_API_AUDIENCE: str
    MODAL_APP_NAME: str
    AWS_SENDER_EMAIL: str

    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=ENV_FILE_PATH,
        extra="allow",
    )

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)


class TestSettings(Settings):
    DATABASE_URI: str = os.getenv("TEST_DATABASE_URI", "sqlite+aiosqlite://")

    model_config = SettingsConfigDict(
        case_sensitive=True
    )


@lru_cache()
def get_settings() -> Union[Settings, TestSettings]:
    if os.getenv("ENV") == "test":
        return TestSettings()
    return Settings()
