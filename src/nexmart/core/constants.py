from enum import IntEnum, StrEnum, auto


class ModelProvider(StrEnum):
    """Enum for model providers."""

    HKUNLP = auto()
    INSTRUCTOR_BASE = "instructor-base"


class StatusCodes(IntEnum):
    """Enum for HTTP status codes."""

    OK = 200
    BAD_REQUEST = 400
    NOT_FOUND = 404
    SERVER_ERROR = 500
    SERVICE_UNAVAILABLE = 503


class APIRoutes(StrEnum):
    """Enum for API routes."""

    API_V1 = "/api/v1"
    HEALTH = "/health"
    SIMILARITY = "/similarity"
    DOCS = "/docs"
    REDOC = "/redoc"
    OPENAPI = "/openapi.json"


class AppSettings(StrEnum):
    """Enum for application settings."""

    APP_NAME = "Product Similarity API"
    MODEL_NAME = f"{ModelProvider.HKUNLP}/{ModelProvider.INSTRUCTOR_BASE}"
    API_VERSION = "v1"
    CORS_ORIGINS = "*"
