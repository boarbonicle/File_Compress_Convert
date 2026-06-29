from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "ConvertFlow API"
    app_version: str = "0.1.0"
    app_description: str = "API para convertir y comprimir archivos."
    api_prefix: str = "/api"
    environment: str = "development"

    storage_path: Path = Path("storage")
    max_file_size_mb: int = 10

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()