from src.domain.models.show_time import ShowTime
from src.infrastructure.database.models.showtime_entity import ShowTimeEntity


class ShowTimeEntityMappers:
    """Mappers for converting between ShowTime domain models and ShowTimeEntity."""

    @staticmethod
    def from_domain(showtime: ShowTime) -> ShowTimeEntity:
        """Map a ShowTime domain model to a ShowTimeEntity.

        Args:
            showtime: The ShowTime domain model to map

        Returns:
            The corresponding ShowTimeEntity
        """
        return ShowTimeEntity(
            id=showtime.id,
            hall_id=showtime.hall_id,
            film_id=showtime.film_id,
            film_format_id=showtime.film_format_id,
            start_time=showtime.start_time,
            end_time=showtime.end_time,
            available_seats=showtime.available_seats,
        )

    @staticmethod
    def to_domain(showtime_entity: ShowTimeEntity) -> ShowTime:
        """Map a ShowTimeEntity to a ShowTime domain model.

        Args:
            showtime_entity: The ShowTimeEntity to map

        Returns:
            The corresponding ShowTime domain model
        """
        return ShowTime(
            id=showtime_entity.id,
            hall_id=showtime_entity.hall_id,
            film_id=showtime_entity.film_id,
            film_format_id=showtime_entity.film_format_id,
            start_time=showtime_entity.start_time,
            end_time=showtime_entity.end_time,
            available_seats=showtime_entity.available_seats or 0,
        )

    @staticmethod
    def to_domains(showtime_entities: list[ShowTimeEntity]) -> list[ShowTime]:
        """Map a list of ShowTimeEntity to a list of ShowTime domain models.

        Args:
            showtime_entities: The list of ShowTimeEntity to map

        Returns:
            The corresponding list of ShowTime domain models
        """
        return [ShowTimeEntityMappers.to_domain(entity) for entity in showtime_entities]
