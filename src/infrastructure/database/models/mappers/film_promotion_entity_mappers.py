from src.domain.models.film_promotion import FilmPromotion
from src.infrastructure.database.models.film_promotion_entity import FilmPromotionEntity


class FilmPromotionEntityMappers:
    """Mappers for converting between FilmPromotion domain model and FilmPromotionEntity."""

    @staticmethod
    def to_domain(entity: FilmPromotionEntity) -> FilmPromotion:
        """
        Convert from database entity to domain model.

        Args:
            entity (FilmPromotionEntity): The database entity

        Returns:
            FilmPromotion: The domain model
        """
        return FilmPromotion(
            id=entity.id,
            film_id=entity.film_id,
            type=entity.type,
            title=entity.title,
            content=entity.content,
            valid_from=entity.valid_from,
            valid_until=entity.valid_until,
        )

    @staticmethod
    def from_domain(domain: FilmPromotion) -> FilmPromotionEntity:
        """
        Convert from domain model to database entity.

        Args:
            domain (FilmPromotion): The domain model

        Returns:
            FilmPromotionEntity: The database entity
        """
        return FilmPromotionEntity(
            id=domain.id,
            film_id=domain.film_id,
            type=domain.type,
            title=domain.title,
            content=domain.content,
            valid_from=domain.valid_from,
            valid_until=domain.valid_until,
        )
