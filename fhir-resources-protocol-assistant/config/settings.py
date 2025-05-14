import os
from functools import lru_cache

from pydantic_settings import BaseSettings


@lru_cache
def get_env_filename():
    runtime_env = os.getenv("ENV")
    return f".env.{runtime_env}" if runtime_env else ".env"


class Settings(BaseSettings):
    ENVIRONMENT: str
    APP_NAME: str
    APP_VERSION: str

    PINECONE_API_KEY: str
    PINECONE_INDEX_NAME: str

    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_REGION: str

    EMBEDDING_MODEL_ID: str

    MODEL_ID: str
    MODEL_TEMPERATURE: float

    VECTOR_STORE_NUMBER_OF_DOCUMENTS_TO_RETRIEVE: int

    LANGSMITH_TRACING: str
    LANGSMITH_ENDPOINT: str
    LANGSMITH_API_KEY: str
    LANGSMITH_PROJECT: str

    class Config:
        env_file = get_env_filename()
        env_file_encoding = "utf-8"


@lru_cache
def get_settings():
    return Settings()
