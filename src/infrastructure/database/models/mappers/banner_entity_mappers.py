from src.domain.models.banner import Banner
from src.infrastructure.database.models.banner_entity import BannerEntity


class BannerEntityMappers:
    @staticmethod
    def from_domain(banner: Banner) -> BannerEntity:
        """Map a Banner domain model to a BannerEntity.

        Args:
            banner: The Banner domain model to map

        Returns:
            The corresponding BannerEntity
        """
        return BannerEntity(
            id=banner.id,
            image_url=banner.image_url,
            fallback_image=banner.fallback_image,
            alt_text=banner.alt_text,
            title=banner.title,
            subtitle=banner.subtitle,
            cta_label=banner.cta_label,
            target_type=banner.target_type,
            target_id=banner.target_id,
            priority=banner.priority,
            start_at=banner.start_at,
            end_at=banner.end_at,
            aspect_ratio=banner.aspect_ratio,
        )

    @staticmethod
    def to_domain(banner_entity: BannerEntity) -> Banner:
        """Map a BannerEntity to a Banner domain model.

        Args:
            banner_entity: The BannerEntity to map

        Returns:
            The corresponding Banner domain model
        """
        return Banner(
            id=banner_entity.id,
            image_url=banner_entity.image_url,
            fallback_image=banner_entity.fallback_image,
            alt_text=banner_entity.alt_text,
            title=banner_entity.title,
            subtitle=banner_entity.subtitle,
            cta_label=banner_entity.cta_label,
            target_type=banner_entity.target_type,
            target_id=banner_entity.target_id,
            priority=banner_entity.priority,
            start_at=banner_entity.start_at,
            end_at=banner_entity.end_at,
            aspect_ratio=banner_entity.aspect_ratio,
        )

    @staticmethod
    def to_domains(banner_entities: list[BannerEntity]) -> list[Banner]:
        """Map a list of BannerEntity to a list of Banner domain models.

        Args:
            banner_entities: The list of BannerEntity to map

        Returns:
            The corresponding list of Banner domain models
        """
        return [BannerEntityMappers.to_domain(entity) for entity in banner_entities]
