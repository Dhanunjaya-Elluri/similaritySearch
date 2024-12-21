import json
from typing import Any, Dict, List

import pytest
from fastapi import Request
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError

from nexmart.core.constants import StatusCodes
from nexmart.core.exceptions import validation_exception_handler
from tests.conftest import TestModel


@pytest.mark.unit  # type: ignore[misc]
async def test_validation_exception_handler() -> None:
    """Test validation exception handler."""
    # Create a validation error
    try:
        TestModel(value=-1)
        pytest.fail("Should have raised ValidationError")
    except ValidationError as e:
        # Convert ValidationError to list of dict for RequestValidationError
        errors: List[Dict[str, Any]] = e.errors()
        exc = RequestValidationError(errors=errors)

    # Create a mock request
    request = Request(
        scope={"type": "http", "method": "GET", "path": "/", "headers": []}
    )

    # Test the handler
    response = await validation_exception_handler(request, exc)

    # Verify response
    assert response.status_code == StatusCodes.BAD_REQUEST

    # Parse response body
    error_detail = json.loads(response.body.decode())["detail"]
    assert isinstance(error_detail, list)
    assert len(error_detail) == 1

    error = error_detail[0]
    assert error["loc"] == ["value"]
    assert error["msg"] == "Input should be greater than 0"
