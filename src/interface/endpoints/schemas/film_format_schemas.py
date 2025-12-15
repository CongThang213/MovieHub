from typing import Optional

from pydantic import BaseModel, Field


class FilmFormatSchema(BaseModel):
    id: str
    name: str
    description: str
    surcharge: float

    class Config:
        from_attributes = True


class FilmFormatResponse(BaseModel):
    film_format: FilmFormatSchema

    class Config:
        from_attributes = True


class FilmFormatsResponse(BaseModel):
    film_formats: list[FilmFormatSchema]

    class Config:
        from_attributes = True


class FilmFormatCreateRequest(BaseModel):
    name: str = Field(..., description="Name of the film format (e.g., IMAX, 3D, 4DX)")
    description: str = Field(..., description="Description of the film format")
    surcharge: float = Field(0.0, ge=0.0, description="Additional cost for this format")


class FilmFormatUpdateRequest(BaseModel):
    name: Optional[str] = Field(None, description="New name of the film format")
    description: Optional[str] = Field(
        None, description="New description of the film format"
    )
    surcharge: Optional[float] = Field(
        None, ge=0.0, description="New surcharge for this format"
    )
