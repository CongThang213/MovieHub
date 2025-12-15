from datetime import datetime
from typing import Dict, Any, Optional

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.domain.repositories.showtime_repository import ShowTimeRepository


class GetShowTimesUseCase:
    """Use case for getting all showtimes with pagination and optional filtering."""

    def __init__(
        self,
        showtime_repository: ShowTimeRepository,
        sessionmaker: async_sessionmaker[AsyncSession],
    ):
        self._showtime_repository = showtime_repository
        self._sessionmaker = sessionmaker

    async def execute(
        self,
        page: int,
        page_size: int,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        film_id: Optional[str] = None,
        cinema_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Execute the use case to get all showtimes with pagination and optional filters.

        Args:
            page: The page number (1-based)
            page_size: The number of items per page
            start_date: Optional start date to filter showtimes
            end_date: Optional end date to filter showtimes
            film_id: Optional film ID filter
            cinema_id: Optional cinema ID filter

        Returns:
            Dict containing:
                - showtimes: List of showtime domain models
                - page: Current page number
                - page_size: Number of items per page
                - total: Total number of showtimes
        """
        async with self._sessionmaker() as session:
            return await self._showtime_repository.get_all(
                page=page,
                page_size=page_size,
                session=session,
                start_date=start_date,
                end_date=end_date,
                film_id=film_id,
                cinema_id=cinema_id,
            )
