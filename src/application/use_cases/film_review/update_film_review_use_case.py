from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.domain.exceptions.film_review_exceptions import FilmReviewNotFoundError
from src.domain.models.film_review import FilmReview
from src.domain.repositories.film_review_repository import FilmReviewRepository


class UpdateFilmReviewUseCase:
    """Use case for updating an existing film review."""

    def __init__(
        self,
        film_review_repository: FilmReviewRepository,
        sessionmaker: async_sessionmaker[AsyncSession],
    ):
        self._film_review_repository = film_review_repository
        self._sessionmaker = sessionmaker

    async def execute(
        self,
        review_id: str,
        rating: int = None,
        content: str = None,
    ) -> FilmReview:
        """Execute the use case to update a film review.

        Args:
            review_id: The ID of the review to update
            rating: The new rating (optional)
            content: The new review content (optional)

        Returns:
            The updated review domain model

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

            # Build update dict with only provided fields
            update_data = {}
            if rating is not None:
                update_data["rating"] = rating
            if content is not None:
                update_data["content"] = content

            result = await self._film_review_repository.update(
                review_id, session, **update_data
            )
            await session.commit()
            return result
