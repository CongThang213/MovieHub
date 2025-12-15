from abc import ABC, abstractmethod
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.models.film_genre import FilmGenre


class FilmGenreRepository(ABC):
    """Repository interface for FilmGenre operations."""

    @abstractmethod
    async def create(self, film_genre: FilmGenre, session: AsyncSession) -> FilmGenre:
        """Create a new film-genre association.

        Args:
            film_genre: The film-genre association to create
            session: The database session to use

        Returns:
            FilmGenre: The created film-genre association
        """
        pass

    @abstractmethod
    async def delete_by_film_id(self, film_id: str, session: AsyncSession) -> None:
        """Delete all genre associations for a film.

        Args:
            film_id: The ID of the film
            session: The database session to use
        """
        pass

    @abstractmethod
    async def get_by_film_id(
        self, film_id: str, session: AsyncSession
    ) -> List[FilmGenre]:
        """Get all genre associations for a film.

        Args:
            film_id: The ID of the film
            session: The database session to use

        Returns:
            List[FilmGenre]: List of film-genre associations
        """
        pass

    @abstractmethod
    async def delete_by_film_and_genre(
        self, film_id: str, genre_id: str, session: AsyncSession
    ) -> None:
        """Delete a specific film-genre association.

        Args:
            film_id: The ID of the film
            genre_id: The ID of the genre
            session: The database session to use
        """
        pass
