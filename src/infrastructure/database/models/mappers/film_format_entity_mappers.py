from src.domain.models.flim_format import FilmFormat
from src.infrastructure.database.models.film_format_entity import FilmFormatEntity


class FilmFormatEntityMappers:
    @staticmethod
    def to_domain(entity: FilmFormatEntity) -> FilmFormat:
        """Convert a FilmFormatEntity to a FilmFormat domain model.

        Args:
            entity (FilmFormatEntity): The FilmFormatEntity instance to convert.

        Returns:
            FilmFormat: The corresponding FilmFormat domain model.
        """
        return FilmFormat(
            id=entity.id,
            name=entity.name,
            description=entity.description,
            surcharge=entity.surcharge,
        )

    @staticmethod
    def to_domains(entities: list[FilmFormatEntity]) -> list[FilmFormat]:
        """Convert a list of FilmFormatEntity instances to a list of FilmFormat domain models.

        Args:
            entities (list[FilmFormatEntity]): The list of FilmFormatEntity instances to convert.

        Returns:
            list[FilmFormat]: The corresponding list of FilmFormat domain models.
        """
        return [FilmFormatEntityMappers.to_domain(entity) for entity in entities]

    @staticmethod
    def from_domain(domain: FilmFormat) -> FilmFormatEntity:
        """Convert a FilmFormat domain model to a FilmFormatEntity.

        Args:
            domain (FilmFormat): The FilmFormat domain model to convert.

        Returns:
            FilmFormatEntity: The corresponding FilmFormatEntity instance.
        """
        return FilmFormatEntity(
            id=domain.id,
            name=domain.name,
            description=domain.description,
            surcharge=domain.surcharge,
        )
