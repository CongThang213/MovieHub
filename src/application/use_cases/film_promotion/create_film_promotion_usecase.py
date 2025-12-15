from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.domain.models.film_promotion import FilmPromotion
from src.domain.repositories.film_promotion_repository import FilmPromotionRepository


class CreateFilmPromotionUseCase:
    """Use case for creating a new film promotion."""

    def __init__(
        self,
        film_promotion_repository: FilmPromotionRepository,
        sessionmaker: async_sessionmaker[AsyncSession],
    ):
        self._film_promotion_repository = film_promotion_repository
        self._sessionmaker = sessionmaker

    async def execute(self, film_promotion: FilmPromotion) -> FilmPromotion:
        """Create a new film promotion.

        Args:
            film_promotion: The film promotion domain model to create.

        Returns:
            The created film promotion with the ID assigned.
        """
        async with self._sessionmaker() as session:
            result = await self._film_promotion_repository.create(
                film_promotion, session
            )
            await session.commit()
            return result
