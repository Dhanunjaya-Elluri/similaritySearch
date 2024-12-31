from ..services.product_similarity import SimilarityService
from .config import get_settings


def get_similarity_service() -> SimilarityService:
    """Get similarity service instance."""
    settings = get_settings()
    return SimilarityService(settings.model_name)


# Global instance
similarity_service = get_similarity_service()
