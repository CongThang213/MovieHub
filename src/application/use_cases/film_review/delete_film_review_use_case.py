from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.domain.exceptions.film_review_exceptions import FilmReviewNotFoundError
from src.domain.repositories.film_review_repository import FilmReviewRepository


class DeleteFilmReviewUseCase:
    """Use case for deleting a film review."""

    def __init__(
        self,
        film_review_repository: FilmReviewRepository,
        sessionmaker: async_sessionmaker[AsyncSession],
    ):
        self._film_review_repository = film_review_repository
        self._sessionmaker = sessionmaker

    async def execute(self, review_id: str) -> None:
        """Execute the use case to delete a film review.

        Args:
            review_id: The ID of the review to delete

        Raises:
            FilmReviewNotFoundError: If the review is not found
        """
        async with self._sessionmaker() as session:
            # Check if review exists
            existing_review = await self._film_review_repository.get_by_id(
                review_id, session
            )
            if not existing_review:
                raise FilmReviewNotFoundError(review_id)

            await self._film_review_repository.delete(review_id, session)
            await session.commit()
