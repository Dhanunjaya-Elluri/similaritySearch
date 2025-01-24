from unittest.mock import MagicMock, call, patch

import pytest

from similarity_search.services.product_similarity import SimilarityService


@pytest.mark.unit  # type: ignore[misc]
async def test_model_loading() -> None:
    """Test model loading."""
    with patch(
        "similarity_search.services.product_similarity.SentenceTransformer"
    ) as mock:
        service = SimilarityService("test-model")
        await service.load_model()
        mock.assert_called_once_with("test-model")


@pytest.mark.unit  # type: ignore[misc]
async def test_cleanup(similarity_service: SimilarityService) -> None:
    """Test cleanup.

    Args:
        similarity_service: Fixture providing a mocked similarity service.
    """
    await similarity_service.cleanup()
    assert similarity_service.model is None


@pytest.mark.unit  # type: ignore[misc]
def test_find_similar(similarity_service: SimilarityService) -> None:
    """Test find similar.

    Args:
        similarity_service: Fixture providing a mocked similarity service.
    """
    mock_encode = MagicMock(
        side_effect=lambda x: [[1.0]] if x == ["test query"] else [[0.9]]
    )
    similarity_service.model.encode = mock_encode

    with patch(
        "sentence_transformers.util.semantic_search",
        return_value=[[{"corpus_id": 0, "score": 0.95}]],
    ):
        results = similarity_service.find_similar(["test query"], ["test product"], 1)

    # Verify encode was called for both queries and products
    assert mock_encode.call_count == 2
    mock_encode.assert_has_calls([call(["test query"]), call(["test product"])])

    assert len(results) == 1
    assert results[0][0]["product"] == "test product"
    assert results[0][0]["score"] == 0.95


@pytest.mark.unit  # type: ignore[misc]
def test_find_similar_model_not_loaded(similarity_service: SimilarityService) -> None:
    """Test find similar model not loaded.

    Args:
        similarity_service: Fixture providing a mocked similarity service.
    """
    similarity_service.model = None

    with pytest.raises(RuntimeError, match="Model not loaded"):
        similarity_service.find_similar(["query"], ["product"], 1)
