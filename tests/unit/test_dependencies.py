from unittest.mock import patch

import pytest

from src.nexmart.core.dependencies import get_similarity_service


@pytest.mark.unit  # type: ignore[misc]
def test_get_similarity_service_cache() -> None:
    """Test similarity service caching."""
    # Clear the lru_cache to ensure clean test
    get_similarity_service.cache_clear()

    with patch("src.nexmart.core.dependencies.get_settings") as mock_get_settings:
        mock_get_settings.return_value.model_name = "test-model"
        service1 = get_similarity_service()
        service2 = get_similarity_service()
        assert service1 is service2  # Same instance due to lru_cache


@pytest.mark.unit  # type: ignore[misc]
def test_get_similarity_service_model_name() -> None:
    """Test similarity service initialization with correct model name."""
    # Clear the lru_cache to ensure clean test
    get_similarity_service.cache_clear()

    with patch("src.nexmart.core.dependencies.get_settings") as mock_get_settings:
        mock_get_settings.return_value.model_name = "test-model"
        service = get_similarity_service()
        assert service.model_name == "test-model"
