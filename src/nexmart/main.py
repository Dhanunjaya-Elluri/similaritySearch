from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from .api.endpoints import router
from .core.config import get_settings
from .core.constants import APIRoutes
from .core.dependencies import similarity_service
from .core.exceptions import validation_exception_handler
from .core.logging import setup_logging


def create_app() -> FastAPI:
    """Create FastAPI application."""
    setup_logging()
    settings = get_settings()

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        try:
            await similarity_service.load_model()
            yield
        finally:
            await similarity_service.cleanup()

    app = FastAPI(
        title=settings.app_name,
        description="API for product similarity search",
        version="1.0.0",
        lifespan=lifespan,
        debug=settings.debug,
        docs_url=APIRoutes.DOCS,
        redoc_url=APIRoutes.REDOC,
        openapi_url=APIRoutes.OPENAPI,
    )

    # Add exception handlers
    app.add_exception_handler(RequestValidationError, validation_exception_handler)

    # Include routers
    app.include_router(router)

    return app


app = create_app()
