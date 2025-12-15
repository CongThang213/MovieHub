from datetime import date
from typing import Optional, List

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.config import PAGE_DEFAULT, PAGE_SIZE_DEFAULT
from src.domain.models.film_brief import FilmBrief
from src.domain.repositories.film_repository import FilmRepository


class SearchFilmsUseCase:
    """Use case for searching films with filters and pagination."""

    def __init__(
        self,
        film_repository: FilmRepository,
        sessionmaker: async_sessionmaker[AsyncSession],
    ):
        self._film_repository = film_repository
        self._sessionmaker = sessionmaker

    async def execute(
        self,
        page: int = PAGE_DEFAULT,
        page_size: int = PAGE_SIZE_DEFAULT,
        title: Optional[str] = None,
        genres: Optional[List[str]] = None,
        min_rating: Optional[float] = None,
        max_rating: Optional[float] = None,
        min_duration: Optional[int] = None,
        max_duration: Optional[int] = None,
        showing_from: Optional[date] = None,
        showing_until: Optional[date] = None,
    ) -> tuple[List[FilmBrief], int]:
        """Execute the use case to search films with filters and pagination.

        Args:
            page: The page number (1-based)
            page_size: The number of records per page
            title: Filter by film title (partial match, case-insensitive)
            genres: Filter by list of genre names
            min_rating: Filter by minimum rating
            max_rating: Filter by maximum rating
            min_duration: Filter by minimum duration in minutes
            max_duration: Filter by maximum duration in minutes
            showing_from: Filter films showing from this date onwards
            showing_until: Filter films showing until this date

        Returns:
            A tuple of (list of film brief models, total count)
        """
        async with self._sessionmaker() as session:
            # Build filter dictionary
            filters = {}
            if title:
                filters["title"] = title
            if genres:
                filters["genres"] = genres
            if min_rating is not None:
                filters["min_rating"] = min_rating
            if max_rating is not None:
                filters["max_rating"] = max_rating
            if min_duration is not None:
                filters["min_duration"] = min_duration
            if max_duration is not None:
                filters["max_duration"] = max_duration
            if showing_from:
                filters["showing_from"] = showing_from
            if showing_until:
                filters["showing_until"] = showing_until

            # Get films with filters
            films = await self._film_repository.search(
                session=session, page=page, page_size=page_size, **filters
            )

            # Get total count for pagination
            total = await self._film_repository.count(session=session, **filters)

            return films, total
