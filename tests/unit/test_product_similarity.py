from unittest.mock import MagicMock, call, patch

import pytest

from nexmart.services.product_similarity import SimilarityService


@pytest.mark.unit  # type: ignore[misc]
def test_similarity_service_initialization(
    similarity_service: SimilarityService,
) -> None:
    """Test service initialization."""
    assert similarity_service.model_name == "test-model"
    assert similarity_service.model is None


@pytest.mark.unit  # type: ignore[misc]
@pytest.mark.asyncio(loop_scope="session")  # type: ignore[misc]
async def test_model_loading() -> None:
    """Test model loading."""
    with patch("nexmart.services.product_similarity.SentenceTransformer") as mock:
        service = SimilarityService("test-model")
        await service.load_model()
        mock.assert_called_once_with("test-model")


@pytest.mark.unit  # type: ignore[misc]
@pytest.mark.asyncio(loop_scope="session")  # type: ignore[misc]
async def test_cleanup() -> None:
    """Test cleanup."""
    service = SimilarityService("test-model")
    service.model = MagicMock()
    await service.cleanup()
    assert service.model is None


@pytest.mark.unit  # type: ignore[misc]
def test_find_similar() -> None:
    """Test find similar."""
    service = SimilarityService("test-model")
    mock_model = MagicMock()
    mock_encode = MagicMock(
        side_effect=lambda x: [[1.0]] if x == ["test query"] else [[0.9]]
    )
    mock_model.encode = mock_encode
    service.model = mock_model

    with patch(
        "sentence_transformers.util.semantic_search",
        return_value=[[{"corpus_id": 0, "score": 0.95}]],
    ):
        results = service.find_similar(["test query"], ["test product"], 1)

    # Verify encode was called for both queries and products
    assert mock_encode.call_count == 2
    mock_encode.assert_has_calls([call(["test query"]), call(["test product"])])

    # Verify results
    assert len(results) == 1
    assert results[0][0]["product"] == "test product"
    assert results[0][0]["score"] == 0.95


@pytest.mark.unit  # type: ignore[misc]
def test_find_similar_model_not_loaded(similarity_service: SimilarityService) -> None:
    """Test find similar model not loaded."""
    similarity_service.model = None

    with pytest.raises(RuntimeError, match="Model not loaded"):
        similarity_service.find_similar(["query"], ["product"], 1)
