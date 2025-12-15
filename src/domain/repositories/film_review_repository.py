from abc import ABC, abstractmethod
from typing import Optional, List

from sqlalchemy.ext.asyncio import AsyncSession

from src.config import PAGE_DEFAULT, PAGE_SIZE_DEFAULT
from src.domain.models.film_review import FilmReview
from src.domain.models.film_review_with_author import FilmReviewWithAuthor
from src.domain.models.film_review_with_author import FilmReviewWithAuthor


class FilmReviewRepository(ABC):
    @abstractmethod
    async def get_by_id(
        self, review_id: str, session: AsyncSession
    ) -> Optional[FilmReview]:
        """
        Retrieve a film review by its ID.

        Args:
            review_id (str): The ID of the review.
            session: The database session to use

        Returns:
            Optional[FilmReview]: The review if found, otherwise None.
        """
        pass

    @abstractmethod
    async def create(self, review: FilmReview, session: AsyncSession) -> FilmReview:
        """
        Create a new film review.

        Args:
            review (FilmReview): The review to create.
            session: The database session to use

        Returns:
            FilmReview: The created review.
        """
        pass

    @abstractmethod
    async def update(
        self, review_id: str, session: AsyncSession, **kwargs
    ) -> FilmReview:
        """
        Update an existing film review.

        Args:
            review_id (str): The ID of the review to update.
            session: The database session to use
            **kwargs: The fields to update with their new values.

        Keyword Args:
            rating (int, optional): The new rating.
            content (str, optional): The new review content.

        Returns:
            FilmReview: The updated review.
        """
        pass

    @abstractmethod
    async def delete(self, review_id: str, session: AsyncSession) -> None:
        """
        Delete a film review.

        Args:
            review_id (str): The ID of the review to delete.
            session: The database session to use
        """
        pass

    @abstractmethod
    async def get_all(
        self,
        session: AsyncSession,
        page: int = PAGE_DEFAULT,
        page_size: int = PAGE_SIZE_DEFAULT,
    ) -> List[FilmReview]:
        """
        Retrieve all film reviews with pagination.

        Args:
            session: The database session to use
            page (int): The page number.
            page_size (int): The number of reviews per page.

        Returns:
            List[FilmReview]: The list of reviews.
        """
        pass

    @abstractmethod
    async def get_by_film_id(
        self,
        film_id: str,
        session: AsyncSession,
        page: int = PAGE_DEFAULT,
        page_size: int = PAGE_SIZE_DEFAULT,
    ) -> List[FilmReview]:
        """
        Retrieve all reviews for a specific film with pagination.

        Args:
            film_id (str): The ID of the film.
            session: The database session to use
            page (int): The page number.
            page_size (int): The number of reviews per page.

        Returns:
            List[FilmReview]: The list of reviews for the film.
        """
        pass

    @abstractmethod
    async def get_by_user_id(
        self,
        user_id: str,
        session: AsyncSession,
        page: int = PAGE_DEFAULT,
        page_size: int = PAGE_SIZE_DEFAULT,
    ) -> List[FilmReview]:
        """
        Retrieve all reviews by a specific user with pagination.

        Args:
            user_id (str): The ID of the user.
            session: The database session to use
            page (int): The page number.
            page_size (int): The number of reviews per page.

        Returns:
            List[FilmReview]: The list of reviews by the user.
        """
        pass

    @abstractmethod
    async def has_user_watched_film(
        self, user_id: str, film_id: str, session: AsyncSession
    ) -> bool:
        """
        Check if a user has watched a specific film (has a paid booking for it).

        Args:
            user_id (str): The ID of the user.
            film_id (str): The ID of the film.
            session: The database session to use

        Returns:
            bool: True if the user has watched the film, False otherwise.
        """
        pass

    @abstractmethod
    async def get_user_review_for_film(
        self, user_id: str, film_id: str, session: AsyncSession
    ) -> Optional[FilmReview]:
        """
        Get a user's review for a specific film if it exists.

        Args:
            user_id (str): The ID of the user.
            film_id (str): The ID of the film.
            session: The database session to use

        Returns:
            Optional[FilmReview]: The review if found, otherwise None.
        """
        pass

    async def get_by_film_id_with_author(
        film_id: str,
        session: AsyncSession,
        page: int = PAGE_DEFAULT,
        page_size: int = PAGE_SIZE_DEFAULT,
    ) -> List[FilmReviewWithAuthor]:
        """
        Retrieve all reviews for a specific film with author details and pagination.

        Args:
            film_id (str): The ID of the film.
            session: The database session to use
            page (int): The page number.
            page_size (int): The number of reviews per page.

        Returns:
            List[FilmReviewWithAuthor]: The list of reviews with author details.
        """
        pass

    @abstractmethod
    async def get_all_with_author(
        self,
        session: AsyncSession,
        page: int = PAGE_DEFAULT,
        page_size: int = PAGE_SIZE_DEFAULT,
    ) -> List[FilmReviewWithAuthor]:
        """
        Retrieve all film reviews with author details and pagination.

        Args:
            session: The database session to use
            page (int): The page number.
            page_size (int): The number of reviews per page.

        Returns:
            List[FilmReviewWithAuthor]: The list of reviews with author details.
        """
        pass
