from typing import Optional

from pydantic import BaseModel


class GenreSchema(BaseModel):
    id: str
    name: str

    class Config:
        from_attributes = True


class GenreResponse(BaseModel):
    genre: GenreSchema

    class Config:
        from_attributes = True


class GenresResponse(BaseModel):
    genres: list[GenreSchema]
    page: int
    page_size: int
    total_pages: int

    class Config:
        from_attributes = True


class GenreCreateRequest(BaseModel):
    name: str


class GenreUpdateRequest(BaseModel):
    name: Optional[str] = None


class RandomGenresResponse(BaseModel):
    genres: list[GenreSchema]
    limit: int
    total_items: int

    class Config:
        from_attributes = True
