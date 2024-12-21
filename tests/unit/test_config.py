import os
from unittest.mock import patch

import pytest

from src.nexmart.core.config import Settings, get_settings


@pytest.mark.unit
class TestSettings:
    def test_default_settings(self) -> None:
        """Test default settings values."""
        settings = Settings()
        assert settings.app_name == "Product Similarity API"
        assert settings.debug is False
        assert settings.api_version == "v1"
        assert settings.cors_origins == ["*"]

    def test_environment_override(self) -> None:
        """Test settings override from environment variables."""
        with patch.dict(
            os.environ,
            {
                "APP_APP_NAME": "Test API",
                "APP_DEBUG": "true",
                "APP_API_VERSION": "v2",
            },
        ):
            settings = Settings()
            assert settings.app_name == "Test API"
            assert settings.debug is True
            assert settings.api_version == "v2"

    def test_get_settings_cache(self) -> None:
        """Test settings caching."""
        settings1 = get_settings()
        settings2 = get_settings()
        assert settings1 is settings2  # Same instance due to lru_cache
