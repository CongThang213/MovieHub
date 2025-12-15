from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.config import PAGE_DEFAULT, PAGE_SIZE_DEFAULT
from src.domain.models.genre import Genre
from src.domain.repositories.genre_repository import GenreRepository


class GetGenresUseCase:
    """Use case for retrieving all genres with pagination."""

    def __init__(
        self,
        genre_repository: GenreRepository,
        sessionmaker: async_sessionmaker[AsyncSession],
    ):
        self._genre_repository = genre_repository
        self._sessionmaker = sessionmaker

    async def execute(
        self, page: int = PAGE_DEFAULT, page_size: int = PAGE_SIZE_DEFAULT
    ) -> tuple[list[Genre], int]:
        """Execute the use case to get all genres with pagination and total count.

        Args:
            page: The page number for pagination
            page_size: The number of items per page

        Returns:
            A tuple containing a list of genre domain models for the specified page
            and the total count of genres
        """
        async with self._sessionmaker() as session:
            return await self._genre_repository.get_all(session, page, page_size)
