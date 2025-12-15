from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class BannerSchema(BaseModel):
    id: str = Field(..., description="ID of the banner")
    image_url: str = Field(..., alias="imageUrl", description="URL of the banner image")
    fallback_image: Optional[str] = Field(
        None,
        alias="fallbackImage",
        description="Fallback image URL for smaller screens",
    )
    alt_text: str = Field(..., alias="altText", description="Alt text for the image")
    title: str = Field(..., description="Banner title")
    subtitle: str = Field(..., description="Banner subtitle")
    cta_label: str = Field(
        ..., alias="ctaLabel", description="Call-to-action button label"
    )
    target_type: str = Field(
        ...,
        alias="targetType",
        description="Type of target (e.g., 'movie', 'promotion', 'external')",
    )
    target_id: str = Field(..., alias="targetId", description="ID of the target")
    priority: int = Field(
        ..., description="Priority for ordering (higher = shown first)"
    )
    start_at: Optional[datetime] = Field(
        None, alias="startAt", description="Start date and time for the banner"
    )
    end_at: Optional[datetime] = Field(
        None, alias="endAt", description="End date and time for the banner"
    )
    aspect_ratio: str = Field(
        ..., alias="aspectRatio", description="Aspect ratio of the banner image"
    )

    class Config:
        from_attributes = True
        populate_by_name = True


class BannerResponse(BaseModel):
    banner: BannerSchema = Field(..., description="Banner details")

    class Config:
        from_attributes = True


class BannersListResponse(BaseModel):
    banners: list[BannerSchema] = Field(..., description="List of active banners")

    class Config:
        from_attributes = True


class BannerCreateRequest(BaseModel):
    image_url: str = Field(..., alias="imageUrl", description="URL of the banner image")
    fallback_image: Optional[str] = Field(
        None,
        alias="fallbackImage",
        description="Fallback image URL for smaller screens",
    )
    alt_text: str = Field(..., alias="altText", description="Alt text for the image")
    title: str = Field(..., description="Banner title")
    subtitle: str = Field(..., description="Banner subtitle")
    cta_label: str = Field(
        ..., alias="ctaLabel", description="Call-to-action button label"
    )
    target_type: str = Field(
        ...,
        alias="targetType",
        description="Type of target (e.g., 'movie', 'promotion', 'external')",
    )
    target_id: str = Field(..., alias="targetId", description="ID of the target")
    priority: int = Field(
        default=0, description="Priority for ordering (higher = shown first)"
    )
    start_at: Optional[datetime] = Field(
        None, alias="startAt", description="Start date and time for the banner"
    )
    end_at: Optional[datetime] = Field(
        None, alias="endAt", description="End date and time for the banner"
    )
    aspect_ratio: str = Field(
        default="16:9",
        alias="aspectRatio",
        description="Aspect ratio of the banner image",
    )

    class Config:
        populate_by_name = True


class BannerUpdateRequest(BaseModel):
    image_url: Optional[str] = Field(
        None, alias="imageUrl", description="URL of the banner image"
    )
    fallback_image: Optional[str] = Field(
        None,
        alias="fallbackImage",
        description="Fallback image URL for smaller screens",
    )
    alt_text: Optional[str] = Field(
        None, alias="altText", description="Alt text for the image"
    )
    title: Optional[str] = Field(None, description="Banner title")
    subtitle: Optional[str] = Field(None, description="Banner subtitle")
    cta_label: Optional[str] = Field(
        None, alias="ctaLabel", description="Call-to-action button label"
    )
    target_type: Optional[str] = Field(
        None,
        alias="targetType",
        description="Type of target (e.g., 'movie', 'promotion', 'external')",
    )
    target_id: Optional[str] = Field(
        None, alias="targetId", description="ID of the target"
    )
    priority: Optional[int] = Field(
        None, description="Priority for ordering (higher = shown first)"
    )
    start_at: Optional[datetime] = Field(
        None, alias="startAt", description="Start date and time for the banner"
    )
    end_at: Optional[datetime] = Field(
        None, alias="endAt", description="End date and time for the banner"
    )
    aspect_ratio: Optional[str] = Field(
        None, alias="aspectRatio", description="Aspect ratio of the banner image"
    )

    class Config:
        populate_by_name = True
