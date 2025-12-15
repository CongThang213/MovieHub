from src.domain.models.film_cast import FilmCast
from src.infrastructure.database.models import FilmCastEntity


class FilmCastEntityMappers:
    @staticmethod
    def to_domain(entity: FilmCastEntity) -> FilmCast:
        """
        Convert a FilmCastEntity database model to a FilmCast domain model.

        Args:
            entity (FilmCastEntity): The FilmCastEntity database model to convert.

        Returns:
            FilmCast: The corresponding FilmCast domain model.
        """
        return FilmCast(
            film_id=entity.film_id,
            cast_id=entity.cast_id,
            role=entity.role,
            character_name=entity.character_name,
        )

    @staticmethod
    def from_domain(domain: FilmCast) -> FilmCastEntity:
        """
        Convert a FilmCast domain model to a FilmCastEntity database model.

        Args:
            domain (FilmCast): The FilmCast domain model to convert.

        Returns:
            FilmCastEntity: The corresponding FilmCastEntity database model.
        """
        return FilmCastEntity(
            film_id=domain.film_id,
            cast_id=domain.cast_id,
            role=domain.role,
            character_name=domain.character_name,
        )
