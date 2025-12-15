from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field


class FilmSchema(BaseModel):
    id: Optional[str] = Field(None, description="ID of the film")
    title: str = Field(..., description="Title of the film")
    votes: int = Field(0, description="Total number of votes for the film")
    rating: float = Field(0.0, description="Average rating of the film (0-10)")
    description: Optional[str] = Field(None, description="Description of the film")
    duration_minutes: Optional[int] = Field(
        None, description="Duration of the film in minutes"
    )
    movie_begin_date: Optional[date] = Field(
        None, description="Date when the film starts showing"
    )
    movie_end_date: Optional[date] = Field(
        None, description="Date when the film stops showing"
    )
    thumbnail_image_url: Optional[str] = Field(
        None, description="URL of the thumbnail image for the film"
    )
    background_image_url: Optional[str] = Field(
        None, description="URL of the background image for the film"
    )
    poster_image_url: Optional[str] = Field(
        None, description="URL of the poster image for the film"
    )

    class Config:
        from_attributes = True


class FilmCast(BaseModel):
    id: str = Field(..., alias="cast_id", description="ID of the cast member")
    role: str = Field(
        ..., description="Role of the cast member in the film (user-defined string)"
    )
    character_name: str = Field(
        ..., description="Name of the character played by the cast member"
    )

    class Config:
        from_attributes = True
        populate_by_name = True


class FilmPromotion(BaseModel):
    type: str = Field(..., description="Type of promotion (e.g., discount, feature)")
    title: str = Field(..., description="Title of the promotion")
    content: str = Field(..., description="Content/details of the promotion")
    valid_from: datetime = Field(
        ..., description="Start date and time of the promotion's validity"
    )
    valid_until: datetime = Field(
        ..., description="End date and time of the promotion's validity"
    )

    class Config:
        from_attributes = True


class FilmTrailer(BaseModel):
    title: str = Field(..., description="Title of the trailer")
    url: str = Field(..., description="URL to the trailer video")
    order_index: int = Field(..., description="Order index for displaying trailers")

    class Config:
        from_attributes = True


class FilmCreateRequest(BaseModel):
    film: FilmSchema = Field(
        ...,
        description="Details of the film to be created",
    )
    genres: Optional[list[str]] = Field(
        None, description="List of genre IDs to associate with the film"
    )
    casts: Optional[list[FilmCast]] = Field(
        None, description="List of cast members associated with the film"
    )
    promotions: Optional[list[FilmPromotion]] = Field(
        None, description="List of promotions associated with the film"
    )
    trailers: Optional[list[FilmTrailer]] = Field(
        None, description="List of trailers associated with the film"
    )

    class Config:
        from_attributes = True


class FilmResponse(BaseModel):
    film: FilmSchema = Field(..., description="The created film details")

    class Config:
        from_attributes = True


class FilmDetailResponse(BaseModel):
    film: FilmSchema = Field(..., description="The film details")
    genres: Optional[list[str]] = Field(
        None, description="List of genres associated with the film"
    )
    casts: Optional[list[FilmCast]] = Field(
        None, description="List of cast members associated with the film"
    )
    promotions: Optional[list[FilmPromotion]] = Field(
        None, description="List of promotions associated with the film"
    )
    trailers: Optional[list[FilmTrailer]] = Field(
        None, description="List of trailers associated with the film"
    )

    class Config:
        from_attributes = True


class FilmsListResponse(BaseModel):
    films: list[FilmSchema] = Field(
        ..., description="List of films for the current page"
    )
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Number of items per page")
    total: int = Field(..., description="Total number of films available")

    class Config:
        from_attributes = True
