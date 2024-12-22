"""Shared test fixtures and configurations."""

from typing import Generator
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from nexmart.main import app
from nexmart.services.product_similarity import SimilarityService


@pytest.fixture  # type: ignore[misc]
def client() -> Generator[TestClient, None, None]:
    """Fixture for FastAPI TestClient.

    Can be used by all integration tests.
    """
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture  # type: ignore[misc]
def mock_sentence_transformer() -> Generator[MagicMock, None, None]:
    """Fixture for mocking SentenceTransformer.

    Can be used by all unit tests that need to mock the transformer.
    """
    with patch("src.nexmart.services.product_similarity.SentenceTransformer") as mock:
        yield mock


@pytest.fixture  # type: ignore[misc]
def mock_transformers_utils() -> Generator[None, None, None]:
    """Fixture for mocking transformer utilities.

    Can be used by all unit tests that need to mock transformer utilities.
    """
    with patch(
        "sentence_transformers.SentenceTransformer.__init__", return_value=None
    ) as mock_init:
        mock_init.return_value = None
        yield


@pytest.fixture  # type: ignore[misc]
def similarity_service() -> SimilarityService:
    """Fixture for SimilarityService with mocked dependencies.

    Can be used by all tests that need a SimilarityService instance.
    """
    with patch("sentence_transformers.SentenceTransformer.__init__", return_value=None):
        service = SimilarityService("test-model")
        return service
