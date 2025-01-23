from typing import List

from pydantic import BaseModel, Field, field_validator


class Query(BaseModel):
    """Request model for similarity search.

    Attributes:
        text (List[str]): List of query texts to search for.
        products (List[str]): List of product descriptions to search in.
        top_k (int): Number of top matches to return.
    """

    text: List[str] = Field(..., description="List of query texts to search for")
    products: List[str] = Field(
        ..., description="List of product descriptions to search in"
    )
    top_k: int = Field(..., description="Number of top matches to return")

    @field_validator("text")  # type: ignore[misc]
    def validate_text(cls, v: List[str]) -> List[str]:
        """Validate text field.

        Args:
            v (List[str]): The text list to validate.

        Returns:
            List[str]: The validated text list.

        Raises:
            ValueError: If the text list is empty.
        """
        if not v:
            raise ValueError("text list cannot be empty")
        return v

    @field_validator("products")  # type: ignore[misc]
    def validate_products(cls, v: List[str]) -> List[str]:
        """Validate products field.

        Args:
            v (List[str]): The products list to validate.

        Returns:
            List[str]: The validated products list.

        Raises:
            ValueError: If the products list is empty.
        """
        if not v:
            raise ValueError("products list cannot be empty")
        return v

    @field_validator("top_k")  # type: ignore[misc]
    def validate_top_k(cls, v: int, values: dict) -> int:
        """Validate top_k field.

        Args:
            v (int): The top_k value to validate
            values (dict): The values dict containing number of products

        Returns:
            int: The validated top_k value

        Raises:
            ValueError: If top_k is less than 1 or greater than number of products
        """
        if v < 1:
            raise ValueError("top_k must be greater than 0")

        # Check if top_k exceeds number of products
        if "products" in values.data and v > len(values.data["products"]):
            raise ValueError(
                f"top_k ({v}) cannot be greater than number of products ({len(values.data['products'])})"
            )
        return v


class SimilarityMatch(BaseModel):
    """Model for a single similarity match.

    Attributes:
        product (str): Matched product description.
        score (float): Similarity score between 0 and 1.
    """

    product: str = Field(..., description="Matched product description")
    score: float = Field(..., description="Similarity score", ge=0, le=1)


class SimilarityResult(BaseModel):
    """Response model for similarity search results.

    Attributes:
        query (str): Original query text.
        matches (List[SimilarityMatch]): List of matching products with scores.
    """

    query: str = Field(..., description="Original query text")
    matches: List[SimilarityMatch] = Field(..., description="List of matching products")
