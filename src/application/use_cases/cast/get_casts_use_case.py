from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.config import PAGE_DEFAULT, PAGE_SIZE_DEFAULT
from src.domain.models.cast import Cast
from src.domain.repositories.cast_repository import CastRepository


class GetCastsUseCase:
    """Use case for retrieving all cast members."""

    def __init__(
        self,
        cast_repository: CastRepository,
        sessionmaker: async_sessionmaker[AsyncSession],
    ):
        self._cast_repository = cast_repository
        self._sessionmaker = sessionmaker

    async def execute(
        self, page: int = PAGE_DEFAULT, page_size: int = PAGE_SIZE_DEFAULT
    ) -> list[Cast]:
        """Execute the use case to retrieve all cast members with pagination.

        Args:
            page: The page number (1-based)
            page_size: The number of records per page

        Returns:
            A list of cast domain models for the specified page
        """
        async with self._sessionmaker() as session:
            return await self._cast_repository.get_all(session, page, page_size)
