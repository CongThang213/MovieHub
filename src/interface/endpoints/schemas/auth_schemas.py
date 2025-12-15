from datetime import date
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator

from src.domain.enums.account_type import AccountType
from src.interface.endpoints.schemas.image_schemas import ImageData
from src.interface.utilities.validators import (
    validate_name,
    validate_password,
    validate_dob,
)


class SignUpUserData(BaseModel):
    """Schema for user data in sign-up requests"""

    name: str = Field(..., description="Full name of the user")
    email: EmailStr = Field(..., description="Email address of the user")
    password: str = Field(..., description="Password for the user account")
    account_type: AccountType = Field(
        AccountType.CUSTOMER,
        description="Type of account being created, defaults to CUSTOMER",
    )
    date_of_birth: Optional[date] = Field(
        None, description="Optional date of birth for the user"
    )

    _validate_name = field_validator("name")(validate_name)
    _validate_password = field_validator("password")(validate_password)
    _validate_date_of_birth = field_validator("date_of_birth")(validate_dob)


class SignUpRequest(BaseModel):
    """Schema for user sign-up requests with image support"""

    user: SignUpUserData = Field(..., description="User registration data")
    image: ImageData = Field(
        default_factory=ImageData, description="Image-related data"
    )


class SignInRequest(BaseModel):
    email: EmailStr
    password: str


class PasswordResetRequest(BaseModel):
    email: EmailStr


class PasswordChangeRequest(BaseModel):
    current_password: str
    new_password: str

    @classmethod
    @field_validator("new_password")
    def _validate_new_password(cls, v, info):
        current_password = info.data.get("current_password")
        return validate_password(v, current_password=current_password)


class UserProfileUpdateRequest(BaseModel):
    name: Optional[str] = None
    avatar_image_url: Optional[str] = None
    date_of_birth: Optional[date] = None

    _validate_name = field_validator("name")(validate_name)
    _validate_date_of_birth = field_validator("date_of_birth")(validate_dob)


class PasswordResetResponse(BaseModel):
    """Schema for successful password reset request responses"""

    message: str = Field(
        ...,
        description="A message indicating the result of the password reset request",
        examples=[
            "If a user with this email exists, a password reset link has been sent."
        ],
    )
