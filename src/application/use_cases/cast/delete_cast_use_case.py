from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.domain.repositories.cast_repository import CastRepository


class DeleteCastUseCase:
    """Use case for deleting a cast member."""

    def __init__(
        self,
        cast_repository: CastRepository,
        sessionmaker: async_sessionmaker[AsyncSession],
    ):
        self._cast_repository = cast_repository
        self._sessionmaker = sessionmaker

    async def execute(self, cast_id: str) -> None:
        """Execute the use case to delete a cast member.

        Args:
            cast_id: The ID of the cast member to delete
        """
        async with self._sessionmaker() as session:
            await self._cast_repository.delete(cast_id, session)
            await session.commit()
