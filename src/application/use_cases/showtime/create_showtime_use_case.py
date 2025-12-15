from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.domain.exceptions.showtime_exceptions import (
    ShowTimeConflictException,
    InvalidShowTimeException,
)
from src.domain.models.show_time import ShowTime
from src.domain.repositories.showtime_repository import ShowTimeRepository


class CreateShowTimeUseCase:
    """Use case for creating a showtime."""

    def __init__(
        self,
        showtime_repository: ShowTimeRepository,
        sessionmaker: async_sessionmaker[AsyncSession],
    ):
        self._showtime_repository = showtime_repository
        self._sessionmaker = sessionmaker

    async def execute(self, showtime: ShowTime) -> ShowTime:
        """Execute the use case to create a showtime.

        Args:
            showtime: The showtime domain model to create

        Returns:
            The created showtime domain model

        Raises:
            InvalidShowTimeException: If showtime data is invalid
            ShowTimeConflictException: If there's a time conflict
        """
        # Validate showtime data
        if not showtime.start_time or not showtime.end_time:
            raise InvalidShowTimeException("Start time and end time are required")

        if showtime.end_time <= showtime.start_time:
            raise InvalidShowTimeException("End time must be after start time")

        async with self._sessionmaker() as session:
            # Check for time conflicts
            has_conflict = await self._showtime_repository.check_time_conflict(
                hall_id=showtime.hall_id,
                start_time=showtime.start_time,
                end_time=showtime.end_time,
                session=session,
            )

            if has_conflict:
                raise ShowTimeConflictException(
                    hall_id=showtime.hall_id,
                    start_time=str(showtime.start_time),
                    end_time=str(showtime.end_time),
                )

            result = await self._showtime_repository.create(showtime, session)
            await session.commit()
            return result
