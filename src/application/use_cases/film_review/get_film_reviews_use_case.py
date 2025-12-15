from typing import List, Tuple

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.config import PAGE_DEFAULT, PAGE_SIZE_DEFAULT
from src.domain.models.film_review_with_author import FilmReviewWithAuthor
from src.domain.repositories.film_review_repository import FilmReviewRepository


class GetFilmReviewsUseCase:
    """Use case for retrieving all film reviews with pagination."""

    def __init__(
        self,
        film_review_repository: FilmReviewRepository,
        sessionmaker: async_sessionmaker[AsyncSession],
    ):
        self._film_review_repository = film_review_repository
        self._sessionmaker = sessionmaker

    async def execute(
        self, page: int = PAGE_DEFAULT, page_size: int = PAGE_SIZE_DEFAULT
    ) -> Tuple[List[FilmReviewWithAuthor], int]:
        """Execute the use case to retrieve all film reviews with author details.

        Args:
            page: The page number
            page_size: The number of reviews per page

        Returns:
            Tuple of (List of FilmReviewWithAuthor domain models, total count)
        """
        async with self._sessionmaker() as session:
            reviews = await self._film_review_repository.get_all_with_author(
                session, page, page_size
            )
            total_count = await self._film_review_repository.count_all(session)
            return reviews, total_count
