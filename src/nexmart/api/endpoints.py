from typing import Dict, List

from fastapi import APIRouter, Depends, HTTPException

from ..core.constants import APIRoutes, StatusCodes
from ..core.dependencies import similarity_service
from ..core.logging import get_logger
from ..services.product_similarity import SimilarityService
from .models import Query, SimilarityResult

logger = get_logger(__name__)
router = APIRouter(prefix=APIRoutes.PREFIX, tags=["Product Similarity"])


similarity_service_dependency = Depends(lambda: similarity_service)


@router.get(APIRoutes.HEALTH)
async def health_check() -> Dict[str, str]:
    """Health check endpoint.

    Returns:
        Dict[str, str]: A dictionary with a "status" key set to "healthy".
    """
    return {"status": "healthy"}


@router.post(APIRoutes.SIMILARITY, response_model=List[SimilarityResult])
async def get_similarity(
    query: Query,
    service: SimilarityService = similarity_service_dependency,
) -> List[SimilarityResult]:
    """Get similar products for given queries.

    Args:
        query (Query): The query object containing the text and products.
        service (SimilarityService): The similarity service instance.

    Returns:
        List[SimilarityResult]: A list of similarity results.
    """
    if not service.model:
        raise HTTPException(
            status_code=StatusCodes.SERVICE_UNAVAILABLE, detail="Model not loaded"
        )

    try:
        hits = service.find_similar(
            queries=query.text,
            products=query.products,
            top_k=query.top_k,
        )

        return [
            SimilarityResult(query=query.text[i], matches=hits[i])
            for i in range(len(query.text))
        ]

    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        raise HTTPException(status_code=StatusCodes.SERVER_ERROR, detail=str(e)) from e
