from typing import List

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.domain.models.film_promotion import FilmPromotion
from src.domain.repositories.film_promotion_repository import FilmPromotionRepository


class GetFilmPromotionsByFilmIdUseCase:
    """Use case for retrieving all promotions for a specific film."""

    def __init__(
        self,
        film_promotion_repository: FilmPromotionRepository,
        sessionmaker: async_sessionmaker[AsyncSession],
    ):
        self._film_promotion_repository = film_promotion_repository
        self._sessionmaker = sessionmaker

    async def execute(self, film_id: str) -> List[FilmPromotion]:
        """Retrieve all promotions for a specific film.

        Args:
            film_id: The ID of the film to retrieve promotions for.

        Returns:
            A list of film promotion domain models associated with the film.
        """
        async with self._sessionmaker() as session:
            return await self._film_promotion_repository.get_by_film_id(
                film_id, session
            )
