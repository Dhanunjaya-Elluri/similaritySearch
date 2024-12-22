from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict

from .constants import AppDefaults, AppSettings


class Settings(BaseSettings):
    """Application settings.

    Attributes:
        app_name (str): The name of the application.
        model_name (str): The name of the sentence transformer model to use.
        debug (bool): Whether to run the application in debug mode.
        api_version (str): The API version.
        cors_origins (List[str]): The allowed origins for CORS.
    """

    app_name: str = AppSettings.APP_NAME
    model_name: str = AppSettings.MODEL_NAME
    debug: bool = AppDefaults.DEBUG
    api_version: str = AppDefaults.API_VERSION
    cors_origins: List[str] = AppDefaults.CORS_ORIGINS

    model_config = SettingsConfigDict(env_prefix="APP_", env_file_encoding="utf-8")


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance.

    Returns:
        Settings: A cached instance of the application settings.
    """
    return Settings()
