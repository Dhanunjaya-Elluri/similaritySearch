from typing import List, TypedDict

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from .constants import StatusCodes


class ValidationErrorDetail(TypedDict):
    loc: List[str]
    msg: str
    type: str


def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """Handle validation exceptions.

    Args:
        request: The request object.
        exc: The validation exception.

    Returns:
        A JSON response with the validation errors.
    """
    errors: List[ValidationErrorDetail] = []
    for error in exc.errors():
        error_dict: ValidationErrorDetail = {
            "loc": error["loc"],
            "msg": error["msg"],
            "type": error["type"],
        }
        errors.append(error_dict)
    return JSONResponse(status_code=StatusCodes.BAD_REQUEST, content={"detail": errors})
