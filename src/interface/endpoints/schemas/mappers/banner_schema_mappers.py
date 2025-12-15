from src.domain.models.banner import Banner
from src.interface.endpoints.schemas.banner_schemas import (
    BannerSchema,
    BannerCreateRequest,
)


class BannerSchemaMappers:
    """Mappers to convert between banner schema and domain models."""

    @staticmethod
    def to_schema(banner: Banner) -> BannerSchema:
        """Convert Banner domain model to BannerSchema.

        Args:
            banner: The banner domain model

        Returns:
            BannerSchema: The banner schema
        """
        return BannerSchema(
            id=banner.id,
            imageUrl=banner.image_url,
            fallbackImage=banner.fallback_image,
            altText=banner.alt_text,
            title=banner.title,
            subtitle=banner.subtitle,
            ctaLabel=banner.cta_label,
            targetType=banner.target_type,
            targetId=banner.target_id,
            priority=banner.priority,
            startAt=banner.start_at,
            endAt=banner.end_at,
            aspectRatio=banner.aspect_ratio,
        )

    @staticmethod
    def to_domain(request: BannerCreateRequest) -> Banner:
        """Convert BannerCreateRequest to Banner domain model.

        Args:
            request: The banner create request

        Returns:
            Banner: The banner domain model
        """
        return Banner(
            image_url=request.image_url,
            fallback_image=request.fallback_image,
            alt_text=request.alt_text,
            title=request.title,
            subtitle=request.subtitle,
            cta_label=request.cta_label,
            target_type=request.target_type,
            target_id=request.target_id,
            priority=request.priority,
            start_at=request.start_at,
            end_at=request.end_at,
            aspect_ratio=request.aspect_ratio,
        )
