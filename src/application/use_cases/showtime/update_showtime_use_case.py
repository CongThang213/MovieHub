from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.domain.exceptions.showtime_exceptions import (
    ShowTimeNotFoundException,
    ShowTimeConflictException,
    InvalidShowTimeException,
)
from src.domain.models.show_time import ShowTime
from src.domain.repositories.showtime_repository import ShowTimeRepository


class UpdateShowTimeUseCase:
    """Use case for updating a showtime."""

    def __init__(
        self,
        showtime_repository: ShowTimeRepository,
        sessionmaker: async_sessionmaker[AsyncSession],
    ):
        self._showtime_repository = showtime_repository
        self._sessionmaker = sessionmaker

    async def execute(self, showtime: ShowTime) -> ShowTime:
        """Execute the use case to update a showtime.

        Args:
            showtime: The showtime domain model with updated data

        Returns:
            The updated showtime domain model

        Raises:
            ShowTimeNotFoundException: If showtime is not found
            InvalidShowTimeException: If showtime data is invalid
            ShowTimeConflictException: If there's a time conflict
        """
        async with self._sessionmaker() as session:
            # Check if showtime exists
            existing = await self._showtime_repository.get_by_id(showtime.id, session)
            if not existing:
                raise ShowTimeNotFoundException(showtime.id)

            # Validate showtime data
            if showtime.start_time and showtime.end_time:
                if showtime.end_time <= showtime.start_time:
                    raise InvalidShowTimeException("End time must be after start time")

                # Check for time conflicts
                has_conflict = await self._showtime_repository.check_time_conflict(
                    hall_id=showtime.hall_id,
                    start_time=showtime.start_time,
                    end_time=showtime.end_time,
                    session=session,
                    exclude_showtime_id=showtime.id,
                )

                if has_conflict:
                    raise ShowTimeConflictException(
                        hall_id=showtime.hall_id,
                        start_time=str(showtime.start_time),
                        end_time=str(showtime.end_time),
                    )

            result = await self._showtime_repository.update(showtime, session)
            await session.commit()
            return result
