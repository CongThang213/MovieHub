from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class VoucherSchema(BaseModel):
    id: str
    code: str
    discount_rate: float
    valid_from: datetime
    valid_until: Optional[datetime] = None
    max_usage: int
    used_count: int

    class Config:
        from_attributes = True


class VoucherResponse(BaseModel):
    voucher: VoucherSchema

    class Config:
        from_attributes = True


class VouchersResponse(BaseModel):
    vouchers: list[VoucherSchema]

    class Config:
        from_attributes = True


class VoucherCreateRequest(BaseModel):
    code: str = Field(..., description="Unique voucher code")
    discount_rate: float = Field(
        ..., gt=0, le=100, description="Discount rate in percentage (0-100)"
    )
    valid_from: Optional[datetime] = Field(
        None, description="Start date of voucher validity"
    )
    valid_until: Optional[datetime] = Field(
        None, description="End date of voucher validity"
    )
    max_usage: int = Field(
        1, gt=0, description="Maximum number of times the voucher can be used"
    )


class VoucherUpdateRequest(BaseModel):
    code: Optional[str] = Field(None, description="Unique voucher code")
    discount_rate: Optional[float] = Field(
        None, gt=0, le=100, description="Discount rate in percentage (0-100)"
    )
    valid_from: Optional[datetime] = Field(
        None, description="Start date of voucher validity"
    )
    valid_until: Optional[datetime] = Field(
        None, description="End date of voucher validity"
    )
    max_usage: Optional[int] = Field(
        None, gt=0, description="Maximum number of times the voucher can be used"
    )
    used_count: Optional[int] = Field(
        None, ge=0, description="Number of times the voucher has been used"
    )


class VoucherValidateRequest(BaseModel):
    code: str = Field(..., description="Voucher code to validate")


class VoucherValidateResponse(BaseModel):
    valid: bool
    voucher_id: str
    code: str
    discount_rate: float
    remaining_uses: int

    class Config:
        from_attributes = True
