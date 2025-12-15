from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.config import PAGE_DEFAULT, PAGE_SIZE_DEFAULT
from src.domain.models.flim_format import FilmFormat
from src.domain.repositories.film_format_repository import FilmFormatRepository


class GetFilmFormatsUseCase:
    """Use case for retrieving all film formats."""

    def __init__(
        self,
        film_format_repository: FilmFormatRepository,
        sessionmaker: async_sessionmaker[AsyncSession],
    ):
        self._film_format_repository = film_format_repository
        self._sessionmaker = sessionmaker

    async def execute(
        self, page: int = PAGE_DEFAULT, page_size: int = PAGE_SIZE_DEFAULT
    ) -> list[FilmFormat]:
        """Execute the use case to get all film formats with pagination.

        Args:
            page: The page number (1-based)
            page_size: The number of records per page

        Returns:
            A list of film format domain models for the specified page
        """
        async with self._sessionmaker() as session:
            return await self._film_format_repository.get_all(
                session, page=page, page_size=page_size
            )
