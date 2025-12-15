from typing import Optional

from pydantic import BaseModel, Field


class PaymentMethodSchema(BaseModel):
    id: str
    name: str
    active: bool
    surcharge: float

    class Config:
        from_attributes = True


class PaymentMethodResponse(BaseModel):
    payment_method: PaymentMethodSchema

    class Config:
        from_attributes = True


class PaymentMethodsResponse(BaseModel):
    payment_methods: list[PaymentMethodSchema]

    class Config:
        from_attributes = True


class PaymentMethodCreateRequest(BaseModel):
    name: str = Field(
        ..., min_length=1, max_length=255, description="Payment method name"
    )
    active: bool = Field(default=True, description="Payment method active status")
    surcharge: float = Field(
        default=0.0, ge=0, le=100, description="Surcharge percentage (0-100)"
    )


class PaymentMethodUpdateRequest(BaseModel):
    name: Optional[str] = Field(
        None, min_length=1, max_length=255, description="Payment method name"
    )
    active: Optional[bool] = Field(None, description="Payment method active status")
    surcharge: Optional[float] = Field(
        None, ge=0, le=100, description="Surcharge percentage (0-100)"
    )
