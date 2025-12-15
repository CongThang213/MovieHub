from typing import Optional

from pydantic import BaseModel, Field


class ServiceSchema(BaseModel):
    id: str
    name: str
    detail: str
    image_url: Optional[str] = None
    price: float
    is_available: bool

    class Config:
        from_attributes = True


class ServiceResponse(BaseModel):
    service: ServiceSchema

    class Config:
        from_attributes = True


class ServicesResponse(BaseModel):
    services: list[ServiceSchema]

    class Config:
        from_attributes = True


class ServiceCreateRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, description="Service name")
    detail: str = Field(..., min_length=1, description="Service details/description")
    price: float = Field(..., ge=0, description="Service price")


class ServiceUpdateRequest(BaseModel):
    name: Optional[str] = Field(
        None, min_length=1, max_length=255, description="Service name"
    )
    detail: Optional[str] = Field(
        None, min_length=1, description="Service details/description"
    )
    price: Optional[float] = Field(None, ge=0, description="Service price")
