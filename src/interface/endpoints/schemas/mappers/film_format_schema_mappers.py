from src.domain.models.flim_format import FilmFormat
from src.interface.endpoints.schemas.film_format_schemas import FilmFormatSchema


class FilmFormatSchemaMappers:
    @staticmethod
    def to_domain(schema) -> FilmFormat:
        """Map schema objects to FilmFormat domain model.

        Args:
            schema: The schema object to map (e.g., FilmFormatCreateRequest).

        Returns:
            The corresponding FilmFormat domain model instance with id, name, description, and surcharge.
        """
        return (
            FilmFormat(
                id=schema.id,
                name=schema.name,
                description=schema.description,
                surcharge=schema.surcharge,
            )
            if hasattr(schema, "id")
            else FilmFormat(
                name=schema.name,
                description=schema.description,
                surcharge=schema.surcharge,
            )
        )

    @staticmethod
    def from_domain(film_format: FilmFormat) -> FilmFormatSchema:
        """Map FilmFormat domain model to FilmFormatSchema.

        Args:
            film_format: The FilmFormat domain model instance to map.

        Returns:
            The corresponding FilmFormatSchema instance.
        """
        return FilmFormatSchema(
            id=film_format.id,
            name=film_format.name,
            description=film_format.description,
            surcharge=film_format.surcharge,
        )

    @staticmethod
    def from_domains(film_formats: list[FilmFormat]) -> list[FilmFormatSchema]:
        """Map a list of FilmFormat domain models to a list of FilmFormatSchemas.

        Args:
            film_formats: The list of FilmFormat domain model instances to map.

        Returns:
            A list of corresponding FilmFormatSchema instances.
        """
        return [
            FilmFormatSchemaMappers.from_domain(film_format)
            for film_format in film_formats
        ]
