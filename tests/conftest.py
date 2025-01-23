"""Shared test fixtures and configurations."""

from typing import Generator
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from similarity_search.main import app
from similarity_search.services.product_similarity import SimilarityService


@pytest.fixture  # type: ignore[misc]
def client() -> Generator[TestClient, None, None]:
    """Fixture for FastAPI TestClient.

    Used by integration tests for API testing.
    """
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture  # type: ignore[misc]
def similarity_service() -> SimilarityService:
    """Fixture for SimilarityService with mocked dependencies.

    Used by unit tests for service testing.
    """
    with patch("sentence_transformers.SentenceTransformer.__init__", return_value=None):
        service = SimilarityService("test-model")
        service.model = MagicMock()
        return service


@pytest.fixture  # type: ignore[misc]
def mock_request() -> Generator[MagicMock, None, None]:
    """Fixture for mocking FastAPI requests.

    Used by exception handler tests.
    """
    mock = MagicMock(
        scope={"type": "http", "method": "GET", "path": "/", "headers": []}
    )
    yield mock
