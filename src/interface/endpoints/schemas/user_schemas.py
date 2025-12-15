from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator

from src.domain.enums.account_type import AccountType
from src.interface.utilities.validators import validate_name, validate_dob


class UserUpdateData(BaseModel):
    """Schema for user profile update data"""

    name: Optional[str] = Field(
        None,
        description="Full name of the user",
    )
    avatar_image_url: Optional[str] = Field(
        None,
        description="URL for the user's avatar image",
    )
    date_of_birth: Optional[date] = Field(
        None,
        description="Date of birth for the user",
    )

    _validate_name = field_validator("name")(validate_name)
    _validate_date_of_birth = field_validator("date_of_birth")(validate_dob)


class ImageData(BaseModel):
    """Schema for image-related data in requests"""

    temp_public_ids: list[str] = Field(
        default=[], description="List of temporary image public IDs to finalize"
    )
    owner_id: Optional[str] = Field(None, description="Owner ID for the images")


class UserUpdateRequest(BaseModel):
    """Schema for user profile update requests with image support"""

    user: UserUpdateData = Field(..., description="User profile data to update")
    image: ImageData = Field(..., description="Image-related data")


class UserResponse(BaseModel):
    """Schema for user data in responses"""

    id: str
    name: str
    email: str
    account_type: AccountType
    avatar_image_url: Optional[str] = None
    date_of_birth: Optional[date] = None
    created_at: datetime

    class Config:
        from_attributes = True


class UserProfileResponse(BaseModel):
    user: UserResponse

    class Config:
        from_attributes = True
