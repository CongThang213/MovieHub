from abc import ABC, abstractmethod
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from src.config import PAGE_DEFAULT, PAGE_SIZE_DEFAULT
from src.domain.models.cast import Cast


class CastRepository(ABC):
    @abstractmethod
    async def get_by_id(self, cast_id: str, session: AsyncSession) -> Optional[Cast]:
        """
        Retrieve a cast member by their ID.

        Args:
            cast_id (str): The ID of the cast member.
            session: The database session to use

        Returns:
            Optional[Cast]: The cast member if found, otherwise None.
        """
        pass

    @abstractmethod
    async def create(self, cast: Cast, session: AsyncSession) -> Cast:
        """
        Create a new cast member.

        Args:
            cast (Cast): The cast member to create.
            session: The database session to use

        Returns:
            Cast: The created cast member.
        """
        pass

    @abstractmethod
    async def update(self, cast_id: str, session: AsyncSession, **kwargs) -> Cast:
        """
        Update an existing cast member.

        Args:
            cast_id (str): The ID of the cast member to update.
            session: The database session to use
            **kwargs: The fields to update with their new values.

        Keyword Args:
            name (str, optional): The new name of the cast member.
            avatar_image_url (str, optional): The new avatar image URL.
            date_of_birth (date, optional): The new date of birth.
            biography (str, optional): The new biography text.

        Returns:
            Cast: The updated cast member.
        """
        pass

    @abstractmethod
    async def delete(self, cast_id: str, session: AsyncSession) -> None:
        """
        Delete a cast member by their ID.

        Args:
            cast_id (str): The ID of the cast member to delete.
            session: The database session to use
        """
        pass

    @abstractmethod
    async def get_all(
        self,
        session: AsyncSession,
        page: int = PAGE_DEFAULT,
        page_size: int = PAGE_SIZE_DEFAULT,
    ) -> list[Cast]:
        """
        Retrieve all cast members with pagination.

        Args:
            session: The database session to use
            page (int): The page number to retrieve.
            page_size (int): The number of items per page.

        Returns:
            list[Cast]: A list of cast members for the specified page.
        """
        pass
