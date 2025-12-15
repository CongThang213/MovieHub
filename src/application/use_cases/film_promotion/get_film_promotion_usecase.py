from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.domain.models.film_promotion import FilmPromotion
from src.domain.repositories.film_promotion_repository import FilmPromotionRepository


class GetFilmPromotionUseCase:
    """Use case for retrieving a film promotion by its ID."""

    def __init__(
        self,
        film_promotion_repository: FilmPromotionRepository,
        sessionmaker: async_sessionmaker[AsyncSession],
    ):
        self._film_promotion_repository = film_promotion_repository
        self._sessionmaker = sessionmaker

    async def execute(self, promotion_id: str) -> Optional[FilmPromotion]:
        """Retrieve a film promotion by its ID.

        Args:
            promotion_id: The ID of the film promotion to retrieve.

        Returns:
            The film promotion domain model or None if not found.
        """
        async with self._sessionmaker() as session:
            return await self._film_promotion_repository.get_by_id(
                promotion_id, session
            )
