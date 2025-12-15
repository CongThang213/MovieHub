from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class FilmReviewBase(BaseModel):
    """Base schema for film review."""

    rating: int = Field(..., ge=1, le=5, description="Rating from 1 to 5")
    content: str = Field("", description="Review content/comment")


class FilmReviewCreateRequest(FilmReviewBase):
    """Schema for creating a new film review."""

    film_id: str = Field(..., description="ID of the film being reviewed")


class FilmReviewUpdateRequest(BaseModel):
    """Schema for updating a film review."""

    rating: Optional[int] = Field(None, ge=1, le=5, description="Rating from 1 to 5")
    content: Optional[str] = Field(None, description="Review content/comment")


class FilmReviewSchema(FilmReviewBase):
    """Schema for film review response."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    film_id: str
    author_id: str
    author_name: str = Field(..., description="Author name")
    avatar_url: Optional[str] = Field(None, description="Author avatar URL")
    created_at: datetime = Field(..., description="Review creation timestamp")


class FilmReviewResponse(BaseModel):
    """Response model for single film review."""

    review: FilmReviewSchema


class FilmReviewsResponse(BaseModel):
    """Response model for list of film reviews."""

    reviews: list[FilmReviewSchema]
    page: int
    page_size: int
