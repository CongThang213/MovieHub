from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.config import PAGE_DEFAULT, PAGE_SIZE_DEFAULT
from src.domain.models.hall import Hall
from src.domain.repositories.hall_repository import HallRepository


class GetHallsByCinemaUseCase:
    """Use case for retrieving all halls in a specific cinema with pagination."""

    def __init__(
        self,
        hall_repository: HallRepository,
        sessionmaker: async_sessionmaker[AsyncSession],
    ):
        self._hall_repository = hall_repository
        self._sessionmaker = sessionmaker

    async def execute(
        self,
        cinema_id: str,
        page: int = PAGE_DEFAULT,
        page_size: int = PAGE_SIZE_DEFAULT,
    ) -> list[Hall]:
        """Execute the use case to get halls by cinema ID.

        Args:
            cinema_id: The ID of the cinema
            page: The page number (1-based)
            page_size: The number of items per page

        Returns:
            A list of hall domain models for the specified cinema
        """
        async with self._sessionmaker() as session:
            return await self._hall_repository.get_by_cinema_id(
                cinema_id, session, page=page, page_size=page_size
            )
