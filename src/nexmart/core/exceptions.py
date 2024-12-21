from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from .constants import StatusCodes


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation exceptions.

    Args:
        request: The incoming request
        exc: The validation exception

    Returns:
        JSONResponse with formatted error details
    """
    errors = []
    for error in exc.errors():
        error_dict = {"loc": error["loc"], "msg": error["msg"], "type": error["type"]}
        # Handle context if it exists
        if "ctx" in error:
            ctx = error["ctx"]
            if "error" in ctx and isinstance(ctx["error"], ValueError):
                error_dict["msg"] = str(ctx["error"])
        errors.append(error_dict)

    return JSONResponse(status_code=StatusCodes.BAD_REQUEST, content={"detail": errors})
