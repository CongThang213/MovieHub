from typing import List, Tuple

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.config import PAGE_DEFAULT, PAGE_SIZE_DEFAULT
from src.domain.models.film_review_with_author import FilmReviewWithAuthor
from src.domain.repositories.film_review_repository import FilmReviewRepository


class GetFilmReviewsByFilmIdUseCase:
    """Use case for retrieving all reviews for a specific film with pagination."""

    def __init__(
        self,
        film_review_repository: FilmReviewRepository,
        sessionmaker: async_sessionmaker[AsyncSession],
    ):
        self._film_review_repository = film_review_repository
        self._sessionmaker = sessionmaker

    async def execute(
        self,
        film_id: str,
        page: int = PAGE_DEFAULT,
        page_size: int = PAGE_SIZE_DEFAULT,
    ) -> Tuple[List[FilmReviewWithAuthor], int]:
        """Execute the use case to retrieve all reviews for a film with author details.

        Args:
            film_id: The ID of the film
            page: The page number
            page_size: The number of reviews per page

        Returns:
            Tuple of (List of FilmReviewWithAuthor domain models, total count)
        """
        async with self._sessionmaker() as session:
            reviews = await self._film_review_repository.get_by_film_id_with_author(
                film_id, session, page, page_size
            )
            total_count = await self._film_review_repository.count_by_film_id(
                film_id, session
            )
            return reviews, total_count
