from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.domain.models.cast import Cast
from src.domain.repositories.cast_repository import CastRepository


class GetCastUseCase:
    """Use case for retrieving a cast member by ID."""

    def __init__(
        self,
        cast_repository: CastRepository,
        sessionmaker: async_sessionmaker[AsyncSession],
    ):
        self._cast_repository = cast_repository
        self._sessionmaker = sessionmaker

    async def execute(self, cast_id: str) -> Optional[Cast]:
        """Execute the use case to retrieve a cast member by ID.

        Args:
            cast_id: The ID of the cast member to retrieve

        Returns:
            The cast domain model if found, None otherwise
        """
        async with self._sessionmaker() as session:
            return await self._cast_repository.get_by_id(cast_id, session)
