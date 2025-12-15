from typing import Optional

from pydantic import BaseModel, Field


class HallSchema(BaseModel):
    id: str
    cinema_id: str
    name: str
    capacity: int
    description: Optional[str] = None

    class Config:
        from_attributes = True


class HallResponse(BaseModel):
    hall: HallSchema

    class Config:
        from_attributes = True


class HallsResponse(BaseModel):
    halls: list[HallSchema]

    class Config:
        from_attributes = True


class HallCreateRequest(BaseModel):
    cinema_id: str = Field(
        ..., description="The ID of the cinema where the hall is located"
    )
    name: str = Field(..., min_length=1, description="The name of the hall")
    capacity: int = Field(..., gt=0, description="The seating capacity of the hall")
    description: Optional[str] = Field(
        None, description="Optional description of the hall"
    )


class HallUpdateRequest(BaseModel):
    cinema_id: Optional[str] = Field(
        None, description="The ID of the cinema where the hall is located"
    )
    name: Optional[str] = Field(None, min_length=1, description="The name of the hall")
    capacity: Optional[int] = Field(
        None, gt=0, description="The seating capacity of the hall"
    )
    description: Optional[str] = Field(
        None, description="Optional description of the hall"
    )
