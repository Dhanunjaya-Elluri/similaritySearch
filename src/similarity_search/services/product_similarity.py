from typing import List, Optional

from sentence_transformers import SentenceTransformer, util

from ..core.logging import get_logger

logger = get_logger(__name__)


class SimilarityService:
    """Service for handling similarity product search operations."""

    def __init__(self, model_name: str):
        """Initialize the similarity service.

        Args:
            model_name (str): The name of the sentence transformer model to load.
        """
        self.model_name: str = model_name
        self.model: Optional[SentenceTransformer] = None

    async def load_model(self) -> None:
        """Load the sentence transformer model asynchronously.

        This method initializes the model and makes it ready for similarity computations.
        """
        logger.info("Loading model...")
        self.model = SentenceTransformer(self.model_name)

        logger.info("Model loaded successfully")

    async def cleanup(self) -> None:
        """Clean up model resources asynchronously.

        This method frees GPU memory if available and removes the model from memory.
        """
        if self.model:
            logger.info("Cleaning up model resources...")
            del self.model  # Remove model from CPU memory
            self.model = None
            logger.info("Model cleanup complete")

    def find_similar(
        self, queries: List[str], products: List[str], top_k: int
    ) -> List[List[dict]]:
        """Find similar products for given queries.

        Args:
            queries (List[str]): List of query texts to search for.
            products (List[str]): List of product descriptions to search in.
            top_k (int): Number of top matches to return for each query.

        Returns:
            List[List[dict]]: A list of lists where each inner list contains dictionaries
                with 'product' and 'score' keys for the top_k matches for each query.

        Raises:
            RuntimeError: If the model is not loaded.
        """
        if not self.model:
            raise RuntimeError("Model not loaded")

        query_embeddings = self.model.encode(queries)
        product_embeddings = self.model.encode(products)

        hits = util.semantic_search(query_embeddings, product_embeddings, top_k=top_k)

        return [
            [
                {
                    "product": products[hit["corpus_id"]],
                    "score": round(float(hit["score"]), 4),
                }
                for hit in query_hits
            ]
            for query_hits in hits
        ]
