from abc import ABC, abstractmethod
from typing import Optional, List

from sqlalchemy.ext.asyncio import AsyncSession

from src.config import PAGE_DEFAULT, PAGE_SIZE_DEFAULT
from src.domain.models.film import Film


class FilmRepository(ABC):
    @abstractmethod
    async def get_all(
        self,
        session: AsyncSession,
        page: int = PAGE_DEFAULT,
        page_size: int = PAGE_SIZE_DEFAULT,
        **kwargs
    ) -> List[Film]:
        """Get all films with brief info, including genres and film_format.

        Args:
            session: The database session to use
            page (int): The page number (1-based). Defaults to PAGE_DEFAULT.
            page_size (int): The number of records per page. Defaults to PAGE_SIZE_DEFAULT.
            **kwargs: Optional filters such as genre, release_date, rating, etc.

        Keyword Args:
            genres (List): Filter films by genres.
            rating (float): Filter films by minimum rating.
            title (str): Filter films by title keyword.
            movie_begin_date (datetime): Filter films that start showing on or after this date.
            movie_end_date (datetime): Filter films that end showing on or before this date.

        Returns:
            List[FilmBrief]: A list of films for the specified page and filters.
        """
        pass

    @abstractmethod
    async def get_by_id(self, film_id: str, session: AsyncSession) -> Optional[Film]:
        """Get film by id

        Args:
            film_id (str): The id of the film to get.
            session: The database session to use

        Returns:
            Optional[Film]: The film if found, else None.
        """
        pass

    @abstractmethod
    async def search(
        self,
        session: AsyncSession,
        page: int = PAGE_DEFAULT,
        page_size: int = PAGE_SIZE_DEFAULT,
        **kwargs
    ) -> List[Film]:
        """Search films with advanced filters.

        Args:
            session: The database session to use
            page: The page number (1-based)
            page_size: The number of records per page
            **kwargs: Filter options

        Keyword Args:
            title (str): Filter by title (partial match, case-insensitive)
            genres (List[str]): Filter by list of genre names
            min_rating (float): Filter by minimum rating
            max_rating (float): Filter by maximum rating
            min_duration (int): Filter by minimum duration in minutes
            max_duration (int): Filter by maximum duration in minutes
            showing_from (date): Filter films showing from this date onwards
            showing_until (date): Filter films showing until this date

        Returns:
            List[Film]: A list of films matching the filters
        """
        pass

    @abstractmethod
    async def count(self, session: AsyncSession, **kwargs) -> int:
        """Count films matching the given filters.

        Args:
            session: The database session to use
            **kwargs: Filter options (same as search method)

        Returns:
            int: Total count of films matching the filters
        """
        pass

    @abstractmethod
    async def create(self, film: Film, session: AsyncSession) -> Film:
        """Create a new film

        Args:
            film (Film): The film to create.
            session: The database session to use

        Returns:
            Film: The created film with the id assigned.
        """
        pass

    @abstractmethod
    async def update(self, film_id: str, session: AsyncSession, **kwargs) -> Film:
        """Update film by id

        Args:
            film_id (str): The id of the film to update.
            session: The database session to use
            **kwargs: The fields to update with their new values.

        Keyword Args:
            title (str): The new title of the film. (optional)
            votes (int): The new number of votes. (optional)
            rating (float): The new rating of the film. (optional)
            description (str): The new description of the film. (optional)
            duration_minutes (int): The new duration in minutes. (optional)
            movie_begin_date (datetime): The new movie begin date. (optional)
            movie_end_date (datetime): The new movie end date. (optional)

        Returns:
            Film: The updated film.
        """
        pass

    @abstractmethod
    async def delete(self, film_id: str, session: AsyncSession):
        """Delete film by id

        Args:
            film_id (str): The id of the film to delete.
            session: The database session to use
        """
        pass
