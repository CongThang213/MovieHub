from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.domain.repositories.film_promotion_repository import FilmPromotionRepository


class DeleteFilmPromotionUseCase:
    """Use case for deleting a film promotion."""

    def __init__(
        self,
        film_promotion_repository: FilmPromotionRepository,
        sessionmaker: async_sessionmaker[AsyncSession],
    ):
        self._film_promotion_repository = film_promotion_repository
        self._sessionmaker = sessionmaker

    async def execute(self, promotion_id: str) -> None:
        """Delete a film promotion by its ID.

        Args:
            promotion_id: The ID of the film promotion to delete
        """
        async with self._sessionmaker() as session:
            await self._film_promotion_repository.delete(promotion_id, session)
            await session.commit()
