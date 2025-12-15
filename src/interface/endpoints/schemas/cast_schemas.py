from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


class CastSchema(BaseModel):
    """Schema for representing a Cast member in API responses."""

    id: str
    name: str
    avatar_image_url: Optional[str] = None
    date_of_birth: Optional[date] = None
    biography: Optional[str] = None

    class Config:
        from_attributes = True


class CastResponse(BaseModel):
    """Schema for a single Cast member API response."""

    cast: CastSchema

    class Config:
        from_attributes = True


class CastsResponse(BaseModel):
    """Schema for multiple Cast members API response."""

    casts: list[CastSchema]

    class Config:
        from_attributes = True


class CastCreateRequest(BaseModel):
    """Schema for creating a new Cast member."""

    name: str = Field(..., description="Full name of the cast member")
    date_of_birth: Optional[date] = Field(
        None, description="Date of birth in YYYY-MM-DD format"
    )
    biography: Optional[str] = Field(
        None, description="Biographical information about the cast member"
    )


class CastUpdateRequest(BaseModel):
    """Schema for updating an existing Cast member."""

    name: Optional[str] = Field(None, description="Full name of the cast member")
    date_of_birth: Optional[date] = Field(
        None, description="Date of birth in YYYY-MM-DD format"
    )
    biography: Optional[str] = Field(
        None, description="Biographical information about the cast member"
    )
