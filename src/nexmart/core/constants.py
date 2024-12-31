from enum import IntEnum, StrEnum
from typing import Final


class ModelProvider(StrEnum):
    """Enum for model providers."""

    MODEL_NAME = "hkunlp/instructor-base"


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
    API_DOCS = "/docs"

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
    MODEL_NAME = ModelProvider.MODEL_NAME


class AppDefaults:
    """Default values for application settings."""

    DEBUG: Final[bool] = False
