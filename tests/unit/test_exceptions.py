import json
from typing import Any, Dict, List

import pytest
from fastapi import Request
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError

from nexmart.api.models import Query
from nexmart.core.constants import StatusCodes
from nexmart.core.exceptions import validation_exception_handler


@pytest.mark.unit  # type: ignore[misc]
def test_validation_exception_handler(mock_request: Request) -> None:
    """Test validation exception handler processes errors correctly."""

    # Create invalid data that should trigger multiple validation errors
    invalid_data = {
        "text": [],  # Invalid: empty list
        "products": [],  # Invalid: empty list
        "top_k": 0,  # Invalid: must be > 0
    }

    # Attempt to create Query with invalid data
    try:
        Query(**invalid_data)
        pytest.fail("Query validation should have failed with invalid data")
    except ValidationError as e:
        errors: List[Dict[str, Any]] = e.errors()
        for error in errors:
            error["loc"] = ("body",) + tuple(error["loc"])
        exc = RequestValidationError(errors=errors)

    # Test the exception handler
    response = validation_exception_handler(mock_request, exc)

    # Test response structure
    assert response.status_code == StatusCodes.BAD_REQUEST
    assert response.headers["content-type"] == "application/json"

    # Test error details
    error_detail = json.loads(response.body.decode())["detail"]
    assert isinstance(error_detail, list)
    assert len(error_detail) == 3  # Should have 3 validation errors

    # Verify each error has correct structure
    for error in error_detail:
        assert set(error.keys()) == {"loc", "msg", "type"}
        assert isinstance(error["loc"], list)
        assert isinstance(error["msg"], str)
        assert isinstance(error["type"], str)

    # Verify specific errors
    errors_by_field = {error["loc"][-1]: error for error in error_detail}

    # Check text validation
    text_error = errors_by_field["text"]
    assert text_error["msg"] == "Value error, text list cannot be empty"
    assert text_error["type"] == "value_error"

    # Check products validation
    products_error = errors_by_field["products"]
    assert products_error["msg"] == "Value error, products list cannot be empty"
    assert products_error["type"] == "value_error"

    # Check top_k validation
    top_k_error = errors_by_field["top_k"]
    assert top_k_error["msg"] == "Value error, top_k must be greater than 0"
    assert top_k_error["type"] == "value_error"
