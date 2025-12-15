from typing import Optional

from pydantic import BaseModel, Field


class SeatCategorySchema(BaseModel):
    id: str
    name: str
    base_price: float
    attributes: Optional[str] = None

    class Config:
        from_attributes = True


class SeatCategoryResponse(BaseModel):
    seat_category: SeatCategorySchema

    class Config:
        from_attributes = True


class SeatCategoriesResponse(BaseModel):
    seat_categories: list[SeatCategorySchema]

    class Config:
        from_attributes = True


class SeatCategoryCreateRequest(BaseModel):
    name: str = Field(..., min_length=1, description="The name of the seat category")
    base_price: float = Field(
        ..., ge=0, description="The base price for this seat category"
    )
    attributes: Optional[str] = Field(
        None, description="Optional attributes or description of the seat category"
    )


class SeatCategoryUpdateRequest(BaseModel):
    name: Optional[str] = Field(
        None, min_length=1, description="The name of the seat category"
    )
    base_price: Optional[float] = Field(
        None, ge=0, description="The base price for this seat category"
    )
    attributes: Optional[str] = Field(
        None, description="Optional attributes or description of the seat category"
    )
