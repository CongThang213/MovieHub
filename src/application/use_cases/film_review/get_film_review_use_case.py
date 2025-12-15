from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.domain.exceptions.film_review_exceptions import FilmReviewNotFoundError
from src.domain.models.film_review import FilmReview
from src.domain.repositories.film_review_repository import FilmReviewRepository


class GetFilmReviewUseCase:
    """Use case for retrieving a single film review by ID."""

    def __init__(
        self,
        film_review_repository: FilmReviewRepository,
        sessionmaker: async_sessionmaker[AsyncSession],
    ):
        self._film_review_repository = film_review_repository
        self._sessionmaker = sessionmaker

    async def execute(self, review_id: str) -> FilmReview:
        """Execute the use case to retrieve a film review.

        Args:
            review_id: The ID of the review to retrieve

        Returns:
            The review domain model

        Raises:
            FilmReviewNotFoundError: If the review is not found
        """
        async with self._sessionmaker() as session:
            result = await self._film_review_repository.get_by_id(review_id, session)
            if not result:
                raise FilmReviewNotFoundError(review_id)
            return result
