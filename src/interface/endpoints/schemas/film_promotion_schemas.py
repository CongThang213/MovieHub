from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class FilmPromotionSchema(BaseModel):
    """Schema for representing a film promotion in API responses."""

    id: str = Field(..., description="ID of the promotion")
    film_id: Optional[str] = Field(None, description="ID of the associated film")
    type: str = Field(..., description="Type of promotion (e.g., discount, featured)")
    title: str = Field(..., description="Title of the promotion")
    content: str = Field(..., description="Content/details of the promotion")
    valid_from: datetime = Field(
        ..., description="Start date and time of the promotion's validity"
    )
    valid_until: Optional[datetime] = Field(
        None, description="End date and time of the promotion's validity"
    )

    class Config:
        from_attributes = True


class FilmPromotionResponse(BaseModel):
    """Schema for a single film promotion API response."""

    promotion: FilmPromotionSchema

    class Config:
        from_attributes = True


class FilmPromotionsResponse(BaseModel):
    """Schema for multiple film promotions API response."""

    promotions: list[FilmPromotionSchema]

    class Config:
        from_attributes = True


class FilmPromotionCreateRequest(BaseModel):
    """Schema for creating a new film promotion."""

    film_id: str = Field(..., description="ID of the film this promotion belongs to")
    type: str = Field(
        ...,
        description="Type of promotion (discount, featured, premiere, special_event)",
    )
    title: str = Field(..., description="Title of the promotion")
    content: str = Field(..., description="Content/details of the promotion")
    valid_from: datetime = Field(
        ..., description="Start date and time of the promotion's validity"
    )
    valid_until: Optional[datetime] = Field(
        None, description="End date and time of the promotion's validity"
    )


class FilmPromotionUpdateRequest(BaseModel):
    """Schema for updating an existing film promotion."""

    film_id: Optional[str] = Field(
        None, description="ID of the film this promotion belongs to"
    )
    type: Optional[str] = Field(
        None,
        description="Type of promotion (discount, featured, premiere, special_event)",
    )
    title: Optional[str] = Field(None, description="Title of the promotion")
    content: Optional[str] = Field(None, description="Content/details of the promotion")
    valid_from: Optional[datetime] = Field(
        None, description="Start date and time of the promotion's validity"
    )
    valid_until: Optional[datetime] = Field(
        None, description="End date and time of the promotion's validity"
    )
