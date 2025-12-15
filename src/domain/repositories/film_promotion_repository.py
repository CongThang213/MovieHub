from abc import ABC, abstractmethod
from typing import Optional, List

from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.models.film_promotion import FilmPromotion


class FilmPromotionRepository(ABC):
    """Abstract base class for FilmPromotion repository."""

    @abstractmethod
    async def create(self, promotion: FilmPromotion, session: AsyncSession):
        """
        Create a new film promotion.

        Args:
            promotion (FilmPromotion): The film promotion to create
            session (AsyncSession): The database session to use

        Returns:
            The created film promotion with ID
        """
        pass

    @abstractmethod
    async def get_by_id(
        self, promotion_id: str, session: AsyncSession
    ) -> Optional[FilmPromotion]:
        """
        Get a film promotion by its ID.

        Args:
            promotion_id (str): The ID of the promotion
            session (AsyncSession): The database session to use

        Returns:
            The film promotion if found, None otherwise
        """
        pass

    @abstractmethod
    async def get_by_film_id(
        self, film_id: str, session: AsyncSession
    ) -> List[FilmPromotion]:
        """
        Get all promotions for a specific film.

        Args:
            film_id (str): The ID of the film
            session (AsyncSession): The database session to use
        Returns:
            List of film promotions associated with the film
        """
        pass

    @abstractmethod
    async def delete(self, promotion_id: str, session: AsyncSession) -> None:
        """
        Delete a film promotion by its ID.

        Args:
            promotion_id (str): The ID of the promotion to delete
            session (AsyncSession): The database session to use

        Returns:
            None
        """
        pass

    @abstractmethod
    async def update(
        self, promotion_id: str, session: AsyncSession, **kwargs
    ) -> FilmPromotion:
        """
        Update a film promotion by its ID.

        Args:
            promotion_id (str): The ID of the promotion to update
            session (AsyncSession): The database session to use
            **kwargs: Fields to update

        Keyword Args:
            title (str): New title for the promotion (Optional)
            content (str): New content for the promotion (Optional)
            valid_from (datetime): New valid_from date (Optional)
            valid_until (datetime): New valid_until date (Optional)
            type (str): New type for the promotion (Optional)

        Returns:
            The updated film promotion
        """
        pass
