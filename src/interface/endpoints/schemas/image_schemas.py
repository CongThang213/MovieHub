from typing import List, Optional

from pydantic import BaseModel, Field

from src.domain.models.image import ImageType


class ImageResponse(BaseModel):
    url: str = Field(..., description="The URL of the image in the storage provider")
    public_id: str = Field(
        ..., description="The public ID of the image in the storage provider"
    )
    type: ImageType = Field(
        ..., description="The type of the image (e.g., AVATAR, FILM_THUMBNAIL)"
    )

    class Config:
        from_attributes = True


class FailedImageUpload(BaseModel):
    """Information about a failed image upload"""

    type: ImageType = Field(
        ..., description="The type of the image that failed to upload"
    )
    error: str = Field(
        ..., description="Error message explaining why the upload failed"
    )
    filename: Optional[str] = Field(None, description="Original filename if available")


class ImageUploadResponse(BaseModel):
    """Response containing both successful and failed image uploads"""

    images: List[ImageResponse] = Field(
        default_factory=list, description="Successfully uploaded images"
    )
    failed: List[FailedImageUpload] = Field(
        default_factory=list, description="Failed image uploads with error details"
    )

    class Config:
        from_attributes = True


class ImageData(BaseModel):
    """Schema for image-related data in requests"""

    temp_public_ids: list[str] = Field(
        default=[], description="List of temporary image public IDs to finalize"
    )
