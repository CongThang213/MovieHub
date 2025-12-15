from typing import Optional

from pydantic import BaseModel, Field


class CinemaSchema(BaseModel):
    id: str
    city_id: str
    name: str
    address: str
    lat: float
    long: float
    rating: float
    thumbnail_image_url: Optional[str] = None

    class Config:
        from_attributes = True


class CinemaResponse(BaseModel):
    cinema: CinemaSchema

    class Config:
        from_attributes = True


class CinemasResponse(BaseModel):
    cinemas: list[CinemaSchema]

    class Config:
        from_attributes = True


class CinemaCreateRequest(BaseModel):
    city_id: str = Field(
        ..., description="The ID of the city where the cinema is located"
    )
    name: str = Field(..., min_length=1, description="The name of the cinema")
    address: str = Field(..., description="The address of the cinema")
    lat: float = Field(..., ge=-90, le=90, description="Latitude coordinate")
    long: float = Field(..., ge=-180, le=180, description="Longitude coordinate")
    rating: Optional[float] = Field(0.0, ge=0, le=5, description="Cinema rating (0-5)")


class CinemaUpdateRequest(BaseModel):
    city_id: Optional[str] = Field(
        None, description="The ID of the city where the cinema is located"
    )
    name: Optional[str] = Field(
        None, min_length=1, description="The name of the cinema"
    )
    address: Optional[str] = Field(None, description="The address of the cinema")
    lat: Optional[float] = Field(None, ge=-90, le=90, description="Latitude coordinate")
    long: Optional[float] = Field(
        None, ge=-180, le=180, description="Longitude coordinate"
    )
    rating: Optional[float] = Field(None, ge=0, le=5, description="Cinema rating (0-5)")
