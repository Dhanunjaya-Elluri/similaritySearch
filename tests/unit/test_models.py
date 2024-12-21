import pytest
from pydantic import ValidationError

from src.nexmart.api.models import Query, SimilarityMatch, SimilarityResult


@pytest.mark.unit
class TestQuery:
    def test_valid_query(self) -> None:
        """Test creating a valid Query instance."""
        query = Query(
            text=["sample query"], products=["product 1", "product 2"], top_k=2
        )
        assert query.text == ["sample query"]
        assert query.products == ["product 1", "product 2"]
        assert query.top_k == 2

    def test_empty_text_list(self) -> None:
        """Test validation error for empty text list."""
        with pytest.raises(ValidationError) as exc_info:
            Query(text=[], products=["product"], top_k=1)
        assert "text list cannot be empty" in str(exc_info.value)

    def test_empty_products_list(self) -> None:
        """Test validation error for empty products list."""
        with pytest.raises(ValidationError) as exc_info:
            Query(text=["query"], products=[], top_k=1)
        assert "products list cannot be empty" in str(exc_info.value)

    def test_invalid_top_k(self) -> None:
        """Test validation error for invalid top_k value."""
        with pytest.raises(ValidationError) as exc_info:
            Query(text=["query"], products=["product"], top_k=0)
        assert "top_k must be greater than 0" in str(exc_info.value)

    def test_default_top_k(self) -> None:
        """Test default value for top_k."""
        query = Query(text=["query"], products=["product"])
        assert query.top_k == 2


@pytest.mark.unit
class TestSimilarityMatch:
    def test_valid_match(self) -> None:
        """Test creating a valid SimilarityMatch instance."""
        match = SimilarityMatch(product="test product", score=0.85)
        assert match.product == "test product"
        assert match.score == 0.85

    def test_invalid_score_too_high(self) -> None:
        """Test validation error for score > 1."""
        with pytest.raises(ValidationError):
            SimilarityMatch(product="test", score=1.5)

    def test_invalid_score_too_low(self) -> None:
        """Test validation error for score < 0."""
        with pytest.raises(ValidationError):
            SimilarityMatch(product="test", score=-0.5)


@pytest.mark.unit
class TestSimilarityResult:
    def test_valid_result(self) -> None:
        """Test creating a valid SimilarityResult instance."""
        matches = [
            SimilarityMatch(product="product 1", score=0.9),
            SimilarityMatch(product="product 2", score=0.8),
        ]
        result = SimilarityResult(query="test query", matches=matches)
        assert result.query == "test query"
        assert len(result.matches) == 2
        assert result.matches[0].score == 0.9
