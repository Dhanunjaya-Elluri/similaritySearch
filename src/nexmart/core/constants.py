from enum import IntEnum, StrEnum
from typing import Final, List


class ModelProvider(StrEnum):
    """Enum for model providers."""

    HKUNLP = "hkunlp"
    INSTRUCTOR_BASE = "instructor-base"

    @classmethod
    def get_model_name(cls) -> str:
        """Get the full model name."""
        return f"{cls.HKUNLP}/{cls.INSTRUCTOR_BASE}"


class StatusCodes(IntEnum):
    """Enum for HTTP status codes."""

    OK = 200
    BAD_REQUEST = 400
    NOT_FOUND = 404
    SERVER_ERROR = 500
    SERVICE_UNAVAILABLE = 503


class APIRoutes(StrEnum):
    """Enum for API routes."""

    PREFIX = "/api/v1"
    HEALTH = "/health"
    SIMILARITY = "/similarity"
    DOCS = "/docs"
    REDOC = "/redoc"
    OPENAPI = "/openapi.json"

    @classmethod
    def get_health_route(cls) -> str:
        """Get the health API route."""
        return cls.PREFIX + cls.HEALTH

    @classmethod
    def get_similarity_route(cls) -> str:
        """Get the similarity API route."""
        return cls.PREFIX + cls.SIMILARITY


class AppSettings(StrEnum):
    """Enum for application settings."""

    APP_NAME = "Product Similarity API"
    MODEL_NAME = ModelProvider.get_model_name()


# Add type-safe constants for settings
class AppDefaults:
    """Default values for application settings."""

    DEBUG: Final[bool] = False
    CORS_ORIGINS: Final[List[str]] = ["*"]
    API_VERSION: Final[str] = "v1"
