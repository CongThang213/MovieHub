from src.domain.models.cinema import Cinema
from src.interface.endpoints.schemas.cinema_schemas import CinemaSchema


class CinemaSchemaMappers:
    @staticmethod
    def to_domain(schema, cinema_id: str = None) -> Cinema:
        """Map schema objects to Cinema domain model.

        Args:
            schema: The schema object to map (e.g., CinemaCreateRequest, CinemaUpdateRequest).
            cinema_id: Optional cinema ID for updates.

        Returns:
            The corresponding Cinema domain model instance.
        """
        # Only set id if cinema_id is provided (for updates), otherwise let Cinema generate it
        cinema_data = {
            "city_id": getattr(schema, "city_id", None) or "",
            "name": getattr(schema, "name", None) or "",
            "address": getattr(schema, "address", None) or "",
            "lat": getattr(schema, "lat", None) or 0.0,
            "long": getattr(schema, "long", None) or 0.0,
            "rating": getattr(schema, "rating", None) or 0.0,
            "thumbnail_image_url": None,
        }

        if cinema_id:
            cinema_data["id"] = cinema_id

        return Cinema(**cinema_data)

    @staticmethod
    def from_domain(cinema: Cinema) -> CinemaSchema:
        """Map Cinema domain model to CinemaSchema.

        Args:
            cinema: The Cinema domain model to map

        Returns:
            The corresponding CinemaSchema
        """
        return CinemaSchema(
            id=cinema.id,
            city_id=cinema.city_id or "",
            name=cinema.name,
            address=cinema.address,
            lat=cinema.lat,
            long=cinema.long,
            rating=cinema.rating,
            thumbnail_image_url=cinema.thumbnail_image_url,
        )

    @staticmethod
    def from_domains(cinemas: list[Cinema]) -> list[CinemaSchema]:
        """Map a list of Cinema domain models to a list of CinemaSchema.

        Args:
            cinemas: The list of Cinema domain models to map

        Returns:
            The corresponding list of CinemaSchema
        """
        return [CinemaSchemaMappers.from_domain(cinema) for cinema in cinemas]
