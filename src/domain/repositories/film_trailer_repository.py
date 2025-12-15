from abc import ABC, abstractmethod
from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.models.film_trailer import FilmTrailer


class FilmTrailerRepository(ABC):
    """Abstract base class for FilmTrailer repository."""

    @abstractmethod
    async def create(
        self, film_trailer: FilmTrailer, session: AsyncSession
    ) -> FilmTrailer:
        """
        Create a new film trailer.

        Args:
            film_trailer: The film trailer to create
            session: The database session to use

        Returns:
            The created film trailer with ID
        """
        pass

    @abstractmethod
    async def get_by_id(
        self, trailer_id: str, session: AsyncSession
    ) -> Optional[FilmTrailer]:
        """
        Get a film trailer by its ID.

        Args:
            trailer_id: The ID of the trailer
            session: The database session to use

        Returns:
            The film trailer if found, None otherwise
        """
        pass

    @abstractmethod
    async def get_by_film_id(
        self, film_id: str, session: AsyncSession
    ) -> List[FilmTrailer]:
        """
        Get all trailers for a specific film.

        Args:
            film_id: The ID of the film
            session: The database session to use

        Returns:
            List of film trailers associated with the film
        """
        pass

    @abstractmethod
    async def update(
        self, trailer_id: str, session: AsyncSession, **kwargs
    ) -> FilmTrailer:
        """
        Update a film trailer by its ID.

        Args:
            trailer_id: The ID of the trailer to update
            session: The database session to use
            **kwargs: Fields to update

        Keyword Args:
            title (str): New title for the trailer (Optional)
            url (str): New URL for the trailer (Optional)
            order_index (int): New order index for the trailer (Optional)

        Returns:
            The updated film trailer
        """
        pass

    @abstractmethod
    async def delete(self, trailer_id: str, session: AsyncSession):
        """
        Delete a film trailer by its ID.

        Args:
            trailer_id: The ID of the trailer to delete
            session: The database session to use
        """
        pass

    @abstractmethod
    async def reorder_trailers(
        self, film_id: str, trailer_ids: List[str], session: AsyncSession
    ) -> List[FilmTrailer]:
        """
        Reorder the trailers for a film based on the provided list of trailer IDs.

        Args:
            film_id: The ID of the film
            trailer_ids: List of trailer IDs in the desired order
            session: The database session to use

        Returns:
            List of reordered film trailers
        """
        pass
