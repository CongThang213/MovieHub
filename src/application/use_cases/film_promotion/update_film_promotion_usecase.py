from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.domain.models.film_promotion import FilmPromotion
from src.domain.repositories.film_promotion_repository import FilmPromotionRepository


class UpdateFilmPromotionUseCase:
    """Use case for updating a film promotion."""

    def __init__(
        self,
        film_promotion_repository: FilmPromotionRepository,
        sessionmaker: async_sessionmaker[AsyncSession],
    ):
        self._film_promotion_repository = film_promotion_repository
        self._sessionmaker = sessionmaker

    async def execute(self, promotion_id: str, **kwargs) -> FilmPromotion:
        """Update a film promotion by its ID.

        Args:
            promotion_id: The ID of the film promotion to update
            **kwargs: The fields to update with their new values

        Keyword Args:
            title (str): New title for the promotion (Optional)
            content (str): New content for the promotion (Optional)
            valid_from (datetime): New valid_from date (Optional)
            valid_until (datetime): New valid_until date (Optional)
            type (str): New type for the promotion (Optional)
            film_id (str): New film ID for the promotion (Optional)

        Returns:
            The updated FilmPromotion domain model
        """
        async with self._sessionmaker() as session:
            result = await self._film_promotion_repository.update(
                promotion_id, session, **kwargs
            )
            await session.commit()
            return result
