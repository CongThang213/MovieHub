from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.domain.exceptions.film_review_exceptions import (
    FilmNotWatchedByUserError,
    DuplicateReviewError,
)
from src.domain.models.film_review import FilmReview
from src.domain.repositories.film_review_repository import FilmReviewRepository


class CreateFilmReviewUseCase:
    """Use case for creating a new film review."""

    def __init__(
        self,
        film_review_repository: FilmReviewRepository,
        sessionmaker: async_sessionmaker[AsyncSession],
    ):
        self._film_review_repository = film_review_repository
        self._sessionmaker = sessionmaker

    async def execute(
        self, review: FilmReview, user_id: str, film_id: str
    ) -> FilmReview:
        """Execute the use case to create a new film review.

        Args:
            review: The review domain model to create
            user_id: The ID of the user creating the review
            film_id: The ID of the film being reviewed

        Returns:
            The created review domain model with ID populated

        Raises:
            FilmNotWatchedByUserError: If the user has not watched the film
            DuplicateReviewError: If the user has already reviewed this film
        """
        async with self._sessionmaker() as session:
            # Check if the user has watched the film
            has_watched = await self._film_review_repository.has_user_watched_film(
                user_id, film_id, session
            )
            if not has_watched:
                raise FilmNotWatchedByUserError(user_id, film_id)

            # Check if the user has already reviewed this film
            existing_review = (
                await self._film_review_repository.get_user_review_for_film(
                    user_id, film_id, session
                )
            )
            if existing_review:
                raise DuplicateReviewError(user_id, film_id)

            result = await self._film_review_repository.create(review, session)
            await session.commit()
            return result
