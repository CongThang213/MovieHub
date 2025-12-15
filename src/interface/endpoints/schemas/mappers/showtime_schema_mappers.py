from src.domain.models.show_time import ShowTime
from src.interface.endpoints.schemas.showtime_schemas import (
    ShowTimeCreateRequest,
    ShowTimeUpdateRequest,
)


class ShowTimeSchemaMappers:
    """Mappers for converting between ShowTime schemas and domain models."""

    @staticmethod
    def to_domain(schema: ShowTimeCreateRequest) -> ShowTime:
        """Convert ShowTimeCreateRequest to ShowTime domain model.

        Args:
            schema: The ShowTimeCreateRequest schema

        Returns:
            The ShowTime domain model
        """
        return ShowTime(
            hall_id=schema.hall_id,
            film_id=schema.film_id,
            film_format_id=schema.film_format_id,
            start_time=schema.start_time,
            end_time=schema.end_time,
            available_seats=schema.available_seats or 0,
        )

    @staticmethod
    def update_to_domain(
        showtime_id: str, schema: ShowTimeUpdateRequest, existing: ShowTime
    ) -> ShowTime:
        """Convert ShowTimeUpdateRequest to ShowTime domain model, merging with existing data.

        Args:
            showtime_id: The ID of the showtime to update
            schema: The ShowTimeUpdateRequest schema
            existing: The existing ShowTime domain model

        Returns:
            The ShowTime domain model with updated values
        """
        return ShowTime(
            id=showtime_id,
            hall_id=schema.hall_id if schema.hall_id is not None else existing.hall_id,
            film_id=schema.film_id if schema.film_id is not None else existing.film_id,
            film_format_id=(
                schema.film_format_id
                if schema.film_format_id is not None
                else existing.film_format_id
            ),
            start_time=(
                schema.start_time
                if schema.start_time is not None
                else existing.start_time
            ),
            end_time=(
                schema.end_time if schema.end_time is not None else existing.end_time
            ),
            available_seats=existing.available_seats,
        )
