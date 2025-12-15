from src.domain.models.cinema import Cinema
from src.infrastructure.database.models.cinema_entity import CinemaEntity


class CinemaEntityMappers:
    @staticmethod
    def from_domain(cinema: Cinema) -> CinemaEntity:
        """Map a Cinema domain model to a CinemaEntity.

        Args:
            cinema: The Cinema domain model to map

        Returns:
            The corresponding CinemaEntity
        """
        return CinemaEntity(
            id=cinema.id,
            city_id=cinema.city_id,
            name=cinema.name,
            address=cinema.address,
            lat=cinema.lat,
            long=cinema.long,
            rating=cinema.rating,
        )

    @staticmethod
    def to_domain(cinema_entity: CinemaEntity) -> Cinema:
        """Map a CinemaEntity to a Cinema domain model.

        Args:
            cinema_entity: The CinemaEntity to map

        Returns:
            The corresponding Cinema domain model
        """
        return Cinema(
            id=cinema_entity.id,
            city_id=cinema_entity.city_id,
            name=cinema_entity.name,
            address=cinema_entity.address or "",
            lat=cinema_entity.lat or 0.0,
            long=cinema_entity.long or 0.0,
            rating=cinema_entity.rating or 0.0,
            thumbnail_image_url=None,  # Will be set separately if needed
        )

    @staticmethod
    def to_domains(cinema_entities: list[CinemaEntity]) -> list[Cinema]:
        """Map a list of CinemaEntity to a list of Cinema domain models.

        Args:
            cinema_entities: The list of CinemaEntity to map

        Returns:
            The corresponding list of Cinema domain models
        """
        return [
            CinemaEntityMappers.to_domain(cinema_entity)
            for cinema_entity in cinema_entities
        ]
