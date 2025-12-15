from abc import ABC, abstractmethod
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from src.config import PAGE_DEFAULT, PAGE_SIZE_DEFAULT
from src.domain.models.flim_format import FilmFormat


class FilmFormatRepository(ABC):
    @abstractmethod
    async def get_all(
        self,
        session: AsyncSession,
        page: int = PAGE_DEFAULT,
        page_size: int = PAGE_SIZE_DEFAULT,
    ) -> list[FilmFormat]:
        """Get all film formats with pagination

        Args:
            session: The database session to use
            page (int): The page number (1-based). Defaults to PAGE_DEFAULT.
            page_size (int): The number of records per page. Defaults to PAGE_SIZE_DEFAULT.

        Returns:
            list[FilmFormat]: A list of film formats for the specified page.
        """
        pass

    @abstractmethod
    async def get_by_id(
        self, format_id: str, session: AsyncSession
    ) -> Optional[FilmFormat]:
        """Get film format by id

        Args:
            format_id (str): The id of the film format to get.
            session: The database session to use

        Returns:
            Optional[FilmFormat]: The film format if found, else None.
        """
        pass

    @abstractmethod
    async def create(
        self, film_format: FilmFormat, session: AsyncSession
    ) -> FilmFormat:
        """Create a new film format

        Args:
            film_format (FilmFormat): The film format to create.
            session: The database session to use

        Returns:
            FilmFormat: The created film format with the id assigned.
        """
        pass

    @abstractmethod
    async def update(
        self, format_id: str, session: AsyncSession, **kwargs
    ) -> FilmFormat:
        """Update film format by id

        Args:
            format_id (str): The id of the film format to update.
            session: The database session to use
            **kwargs: The fields to update and their new values.

        Keyword Args:
            name (str): The new name of the film format. (optional)
            description (str): The new description of the film format. (optional)
            surcharge (float): The new surcharge of the film format. (optional)

        Returns:
            FilmFormat: The updated film format.
        """
        pass

    @abstractmethod
    async def delete(self, format_id: str, session: AsyncSession):
        """Delete film format by id

        Args:
            format_id (str): The id of the film format to delete.
            session: The database session to use
        """
        pass
