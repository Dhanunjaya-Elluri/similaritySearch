from unittest.mock import patch

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from nexmart.main import create_app
from nexmart.services.product_similarity import SimilarityService


@pytest.mark.integration  # type: ignore[misc]
def test_app_creation() -> None:
    """Test application creation and configuration."""
    app = create_app()
    assert isinstance(app, FastAPI)
    assert app.title == "Product Similarity API"
    assert app.debug is False


@pytest.mark.integration  # type: ignore[misc]
def test_health_check(client: TestClient) -> None:
    """Test health check endpoint."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


@pytest.mark.integration  # type: ignore[misc]
@pytest.mark.asyncio  # type: ignore[misc]
async def test_similarity_endpoint_success(client: TestClient) -> None:
    """Test similarity endpoint with valid input."""
    with patch.object(SimilarityService, "find_similar") as mock_find_similar:
        mock_find_similar.return_value = [
            [
                {"product": "Circular saw", "score": 0.95},
                {"product": "Hammer", "score": 0.75},
            ]
        ]
        payload = {
            "text": ["What can I use to cut wood?"],
            "products": ["Circular saw", "Hammer"],
            "top_k": 2,
        }
        response = client.post("/api/v1/similarity", json=payload)
        assert response.status_code == 200
        result = response.json()
        assert len(result) == 1
        assert len(result[0]["matches"]) == 2
        assert result[0]["matches"][0]["score"] == 0.95


@pytest.mark.integration  # type: ignore[misc]
@pytest.mark.asyncio  # type: ignore[misc]
async def test_similarity_endpoint_validation_error(client: TestClient) -> None:
    """Test similarity endpoint with invalid input."""
    payload = {
        "text": [],  # Empty text list should fail validation
        "products": ["test product"],
        "top_k": 1,
    }
    response = client.post("/api/v1/similarity", json=payload)
    assert response.status_code == 400
    error_detail = response.json()["detail"]
    assert isinstance(error_detail, list)
    assert len(error_detail) > 0
    assert error_detail[0]["msg"] == "text list cannot be empty"
    assert error_detail[0]["loc"] == ["body", "text"]
    assert error_detail[0]["type"] == "value_error"


@pytest.mark.integration  # type: ignore[misc]
@pytest.mark.asyncio  # type: ignore[misc]
async def test_similarity_endpoint_model_not_loaded(client: TestClient) -> None:
    """Test similarity endpoint when model is not loaded."""
    with patch("nexmart.main.similarity_service.model", None):
        payload = {
            "text": ["test query"],
            "products": ["test product"],
            "top_k": 1,
        }
        response = client.post("/api/v1/similarity", json=payload)
        assert response.status_code == 503
        assert response.json()["detail"] == "Model not loaded"


@pytest.mark.integration  # type: ignore[misc]
@pytest.mark.asyncio  # type: ignore[misc]
async def test_similarity_endpoint_error_handling(client: TestClient) -> None:
    """Test similarity endpoint error handling."""
    with patch.object(SimilarityService, "find_similar") as mock_find_similar:
        mock_find_similar.side_effect = Exception("Test error")
        payload = {
            "text": ["test query"],
            "products": ["test product"],
            "top_k": 1,
        }
        response = client.post("/api/v1/similarity", json=payload)
        assert response.status_code == 500
        assert response.json()["detail"] == "Test error"


@pytest.mark.integration  # type: ignore[misc]
def test_docs_endpoint(client: TestClient) -> None:
    """Test OpenAPI documentation endpoint."""
    response = client.get("/docs")
    assert response.status_code == 200


@pytest.mark.integration  # type: ignore[misc]
def test_openapi_endpoint(client: TestClient) -> None:
    """Test OpenAPI schema endpoint."""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    schema = response.json()
    assert schema["info"]["title"] == "Product Similarity API"
    assert "/api/v1/similarity" in schema["paths"]


@pytest.mark.integration  # type: ignore[misc]
def test_redoc_endpoint(client: TestClient) -> None:
    """Test ReDoc documentation endpoint."""
    response = client.get("/redoc")
    assert response.status_code == 200