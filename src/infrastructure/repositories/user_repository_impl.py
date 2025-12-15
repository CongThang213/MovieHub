from typing import List, Optional, Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.domain.exceptions.user_exceptions import (
    UserNotFoundException,
    UserDeletionFailedException,
)
from src.domain.models.user import User
from src.domain.repositories.user_repository import UserRepository
from src.infrastructure.database.models.mappers.user_entity_mappers import (
    UserEntityMapper,
)
from src.infrastructure.database.models.user_entity import UserEntity


class UserRepositoryImpl(UserRepository):
    """Implementation of the user repository using SQLAlchemy."""

    def __init__(self, sessionmaker: async_sessionmaker[AsyncSession]):
        """Initialize the user repository with a session factory.

        Args:
            sessionmaker: Factory for creating database sessions
        """
        self._sessionmaker = sessionmaker

    async def get_by_id(self, user_id: str, session: AsyncSession) -> Optional[User]:
        """Get a user by ID.

        Args:
            user_id: The user ID to look up
            session: The database session to use

        Returns:
            The user domain model

        Raises:
            UserNotFoundException: If user with given ID is not found
        """
        result = await session.execute(
            select(UserEntity).where(UserEntity.id == user_id)
        )
        user_entity = result.scalars().first()

        if not user_entity:
            raise UserNotFoundException(identifier=user_id)

        return UserEntityMapper.to_domain(user_entity)

    async def get_by_email(self, email: str, session: AsyncSession) -> User:
        """Get a user by email address.

        Args:
            email: The email address to look up
            session: The database session to use

        Returns:
            The user domain model

        Raises:
            UserNotFoundException: If user with given email is not found
        """
        result = await session.execute(
            select(UserEntity).where(UserEntity.email == email)
        )
        user_entity = result.scalars().first()

        if not user_entity:
            raise UserNotFoundException(identifier=email)

        return UserEntityMapper.to_domain(user_entity)

    async def create(self, user: User, session: AsyncSession) -> User:
        """Create a new user.

        Args:
            user: The user domain model to persist
            session: The database session to use

        Returns:
            The user domain model with updated info
        """
        # Create entity from domain model
        user_entity = UserEntityMapper.from_domain(user)

        # Add to session and flush to get generated values
        session.add(user_entity)
        await session.flush()

        # Return domain model from updated entity
        return UserEntityMapper.to_domain(user_entity)

    async def update(self, user_id: str, session: AsyncSession, **kwargs: Any) -> User:
        """Update an existing user.

        Args:
            user_id: The ID of the user to update
            session: The database session to use
            **kwargs: Fields to update on the user

        Returns:
            The updated user domain model

        Raises:
            UserNotFoundException: If user with given ID is not found
        """
        # Find the user entity
        result = await session.execute(
            select(UserEntity).where(UserEntity.id == user_id)
        )
        user_entity = result.scalars().first()

        if not user_entity:
            raise UserNotFoundException(identifier=user_id)

        # Update entity attributes with non-None values from kwargs
        for attr, value in kwargs.items():
            if value is not None and hasattr(user_entity, attr):
                setattr(user_entity, attr, value)

        # Flush to ensure ORM updates
        await session.flush()

        # Return domain model from updated entity
        return UserEntityMapper.to_domain(user_entity)

    async def delete(self, user_id: str, session: AsyncSession) -> None:
        """Delete a user by ID.

        Args:
            user_id: The user ID to delete
            session: The database session to use

        Raises:
            UserDeletionFailedException: If user deletion fails
        """
        result = await session.execute(
            select(UserEntity).where(UserEntity.id == user_id)
        )
        user_entity = result.scalars().first()

        if not user_entity:
            raise UserDeletionFailedException(id=user_id)

        await session.delete(user_entity)

    async def get_users(
        self, session: AsyncSession, skip: int = 0, limit: int = 100
    ) -> List[User]:
        """Get a list of users with pagination.

        Args:
            session: The database session to use
            skip: Number of users to skip (for pagination)
            limit: Maximum number of users to return

        Returns:
            List of user domain models
        """
        result = await session.execute(select(UserEntity).offset(skip).limit(limit))
        user_entities = result.scalars().all()
        return [UserEntityMapper.to_domain(entity) for entity in user_entities]
