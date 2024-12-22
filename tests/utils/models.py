"""Test models and utilities."""

from pydantic import BaseModel, Field


class ValidationTestModel(BaseModel):
    """Model for testing validation errors.

    This model is used in validation error tests.
    """

    value: int = Field(gt=0, description="Value must be greater than 0")
