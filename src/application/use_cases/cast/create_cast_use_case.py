from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.domain.models.cast import Cast
from src.domain.repositories.cast_repository import CastRepository


class CreateCastUseCase:
    """Use case for creating a new cast member."""

    def __init__(
        self,
        cast_repository: CastRepository,
        sessionmaker: async_sessionmaker[AsyncSession],
    ):
        self._cast_repository = cast_repository
        self._sessionmaker = sessionmaker

    async def execute(self, cast: Cast) -> Cast:
        """Execute the use case to create a new cast member.

        Args:
            cast: The cast domain model to create

        Returns:
            The created cast domain model with ID populated
        """
        async with self._sessionmaker() as session:
            result = await self._cast_repository.create(cast, session)
            await session.commit()
            return result
