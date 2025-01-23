from pydantic_settings import BaseSettings

from .constants import AppDefaults, AppSettings


class Settings(BaseSettings):
    """Application settings."""

    app_name: str = AppSettings.APP_NAME
    model_name: str = AppSettings.MODEL_NAME
    debug: bool = AppDefaults.DEBUG


def get_settings() -> Settings:
    """Get settings instance.

    Returns:
        Settings: An instance of the application settings.
    """
    return Settings()
