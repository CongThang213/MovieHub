from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ShowTimeSchema(BaseModel):
    """Schema for ShowTime response."""

    id: str
    hall_id: str
    film_id: str
    film_format_id: str
    start_time: datetime
    end_time: datetime
    available_seats: Optional[int] = None

    class Config:
        from_attributes = True


class ShowTimeResponse(BaseModel):
    """Response model for a single showtime."""

    showtime: ShowTimeSchema

    class Config:
        from_attributes = True


class ShowTimeGroupedSchema(BaseModel):
    """Simplified schema for ShowTime in grouped responses."""

    id: str
    film_format: str
    start_time: datetime
    end_time: datetime

    class Config:
        from_attributes = True


class ShowTimesListResponse(BaseModel):
    """Response model for a list of showtimes without pagination."""

    showtimes: list[ShowTimeSchema] = Field(..., description="List of showtimes")

    class Config:
        from_attributes = True


class HallShowTimesSchema(BaseModel):
    """Schema for showtimes grouped by hall."""

    hall_id: str = Field(..., description="The ID of the hall")
    hall_name: str = Field(..., description="The name of the hall")
    showtimes: list[ShowTimeGroupedSchema] = Field(
        ..., description="List of showtimes for this hall"
    )

    class Config:
        from_attributes = True


class CinemaShowTimesSchema(BaseModel):
    """Schema for showtimes grouped by cinema."""

    cinema_id: str = Field(..., description="The ID of the cinema")
    cinema_name: str = Field(..., description="The name of the cinema")
    cinema_address: Optional[str] = Field(None, description="The address of the cinema")
    lon: Optional[float] = Field(None, description="Longitude coordinate of the cinema")
    lat: Optional[float] = Field(None, description="Latitude coordinate of the cinema")
    halls: list[HallShowTimesSchema] = Field(
        ..., description="List of halls with their showtimes"
    )

    class Config:
        from_attributes = True


class ShowTimesByFilmResponse(BaseModel):
    """Response model for showtimes grouped by cinema and hall."""

    cinemas: list[CinemaShowTimesSchema] = Field(
        ..., description="List of cinemas with halls and showtimes"
    )

    class Config:
        from_attributes = True


class ShowTimesResponse(BaseModel):
    """Response model for multiple showtimes with pagination."""

    showtimes: list[ShowTimeSchema] = Field(
        ..., description="List of showtimes for the current page"
    )
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Number of items per page")
    total: int = Field(..., description="Total number of showtimes available")

    class Config:
        from_attributes = True


class ShowTimeCreateRequest(BaseModel):
    """Request model for creating a showtime."""

    hall_id: str = Field(..., description="The ID of the hall")
    film_id: str = Field(..., description="The ID of the film")
    film_format_id: str = Field(..., description="The ID of the film format")
    start_time: datetime = Field(..., description="The start time of the showtime")
    end_time: datetime = Field(..., description="The end time of the showtime")
    available_seats: Optional[int] = Field(
        None, ge=0, description="The number of available seats"
    )


class ShowTimeUpdateRequest(BaseModel):
    """Request model for updating a showtime."""

    hall_id: Optional[str] = Field(None, description="The ID of the hall")
    film_id: Optional[str] = Field(None, description="The ID of the film")
    film_format_id: Optional[str] = Field(None, description="The ID of the film format")
    start_time: Optional[datetime] = Field(
        None, description="The start time of the showtime"
    )
    end_time: Optional[datetime] = Field(
        None, description="The end time of the showtime"
    )
