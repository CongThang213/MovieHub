from abc import ABC, abstractmethod
from typing import List, Optional, Any

from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.models.user import User


class UserRepository(ABC):
    """Interface for user repository"""

    @abstractmethod
    async def get_by_id(self, user_id: str, session: AsyncSession) -> Optional[User]:
        """Get a user by ID

        Args:
            user_id: The user ID to look up
            session: The database session to use

        Returns:
            The user domain model or None if not found
        """
        pass

    @abstractmethod
    async def get_by_email(self, email: str, session: AsyncSession) -> User:
        """Get a user by email

        Args:
            email: The email address to look up
            session: The database session to use

        Returns:
            The user domain model
        """
        pass

    @abstractmethod
    async def create(self, user: User, session: AsyncSession) -> User:
        """Create a new user

        Args:
            user: The user to create
            session: The database session to use

        Returns:
            The created user
        """
        pass

    @abstractmethod
    async def update(self, user_id: str, session: AsyncSession, **kwargs: Any) -> User:
        """Update an existing user

        Args:
            user_id: The ID of the user to update
            session: The database session to use
            **kwargs: Fields to update on the user

        Returns:
            The updated user
        """
        pass

    @abstractmethod
    async def delete(self, user_id: str, session: AsyncSession) -> None:
        """Delete a user by ID

        Args:
            user_id: The ID of the user to delete
            session: The database session to use
        """
        pass

    @abstractmethod
    async def get_users(
        self, session: AsyncSession, skip: int = 0, limit: int = 100
    ) -> List[User]:
        """Get a list of users with pagination

        Args:
            session: The database session to use
            skip: Number of users to skip
            limit: Maximum number of users to return

        Returns:
            List of users
        """
        pass
