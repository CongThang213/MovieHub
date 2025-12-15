from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.config import PAGE_DEFAULT, PAGE_SIZE_DEFAULT
from src.domain.models.film import Film
from src.domain.repositories.film_repository import FilmRepository


class GetFilmsUseCase:
    """Use case for retrieving all films with pagination."""

    def __init__(
        self,
        film_repository: FilmRepository,
        sessionmaker: async_sessionmaker[AsyncSession],
    ):
        self._film_repository = film_repository
        self._sessionmaker = sessionmaker

    async def execute(
        self, page: int = PAGE_DEFAULT, page_size: int = PAGE_SIZE_DEFAULT
    ) -> list[Film]:
        """Execute the use case to retrieve all films with pagination.

        Args:
            page: The page number (1-based)
            page_size: The number of records per page

        Returns:
            A list of film domain models for the specified page
        """
        async with self._sessionmaker() as session:
            return await self._film_repository.get_all(session, page, page_size)
