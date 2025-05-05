import os
from functools import lru_cache
from typing import Sequence

from pydantic import field_validator
from pydantic_settings import BaseSettings


@lru_cache
def get_env_filename():
    runtime_env = os.getenv("ENV")
    return f".env.{runtime_env}" if runtime_env else ".env"


class Settings(BaseSettings):
    ENVIRONMENT: str
    APP_NAME: str
    APP_VERSION: str

    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_REGION: str

    MODEL_ID: str
    MODEL_TEMPERATURE: float

    LANGSMITH_TRACING: str
    LANGSMITH_ENDPOINT: str
    LANGSMITH_API_KEY: str
    LANGSMITH_PROJECT: str

    FIRECRAWL_API_KEY: str

    TAVILY_API_KEY: str

    CORS_ORIGINS: Sequence[str]

    class Config:
        env_file = get_env_filename()
        env_file_encoding = "utf-8"

    @field_validator("CORS_ORIGINS", mode="before")
    def parse_origins(cls, value):
        if isinstance(value, str):
            return [origin.strip() for origin in value.split(",")]
        return value


@lru_cache
def get_settings():
    return Settings()
