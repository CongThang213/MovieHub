from src.domain.models.genre import Genre
from src.infrastructure.database.models.genre_entity import GenreEntity


class GenreEntityMappers:
    @staticmethod
    def from_domain(genre: Genre) -> GenreEntity:
        """Map a Genre domain model to a GenreEntity.

        Args:
            genre: The Genre domain model to map

        Returns:
            The corresponding GenreEntity
        """
        return GenreEntity(
            id=genre.id,
            name=genre.name,
        )

    @staticmethod
    def to_domain(genre_entity: GenreEntity) -> Genre:
        """Map a GenreEntity to a Genre domain model.

        Args:
            genre_entity: The GenreEntity to map

        Returns:
            The corresponding Genre domain model
        """
        return Genre(
            id=genre_entity.id,
            name=genre_entity.name,
        )

    @staticmethod
    def to_domains(genre_entities: list[GenreEntity]) -> list[Genre]:
        """Map a list of GenreEntity to a list of Genre domain models.

        Args:
            genre_entities: The list of GenreEntity to map

        Returns:
            The corresponding list of Genre domain models
        """
        return [GenreEntityMappers.to_domain(entity) for entity in genre_entities]
