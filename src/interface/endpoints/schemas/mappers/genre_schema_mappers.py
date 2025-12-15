from src.domain.models.genre import Genre
from src.interface.endpoints.schemas.genre_schemas import (
    GenreSchema,
)


class GenreSchemaMappers:
    @staticmethod
    def to_domain(schema) -> Genre:
        """Map schema objects to Genre domain model.

        Args:
            schema: The schema object to map (e.g., GenreCreateRequest).

        Returns:
            The corresponding Genre domain model instance with id and name.
        """
        return (
            Genre(id=schema.id, name=schema.name)
            if hasattr(schema, "id")
            else Genre(name=schema.name)
        )

    @staticmethod
    def from_domain(genre: Genre) -> GenreSchema:
        """Map Genre domain model to GenreSchema.

        Args:
            genre: The Genre domain model instance to map.

        Returns:
            The corresponding GenreSchema instance.
        """
        return GenreSchema(id=genre.id, name=genre.name)

    @staticmethod
    def from_domains(genres: list[Genre]) -> list[GenreSchema]:
        """Map a list of Genre domain models to a list of GenreSchemas.

        Args:
            genres: The list of Genre domain model instances to map.

        Returns:
            A list of corresponding GenreSchema instances.
        """
        return [GenreSchemaMappers.from_domain(genre) for genre in genres]
