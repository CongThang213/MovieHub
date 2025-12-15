from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from config.logging_config import logger
from src.domain.models.user import User
from src.domain.repositories.user_repository import UserRepository


class UpdateUserUseCase:
    def __init__(
        self,
        user_repository: UserRepository,
        sessionmaker: async_sessionmaker[AsyncSession],
    ) -> None:
        self.user_repository = user_repository
        self.sessionmaker = sessionmaker

    async def execute(self, user_id: str, **kwargs: Any) -> User:
        """Execute the update user use case to modify a user's profile information.

        Args:
            user_id (str): The ID of the user to update
            **kwargs: Arbitrary keyword arguments representing user fields to update.

        Keyword Args:
            name (str): The new name for the user
            date_of_birth (date): The new date of birth

        Returns:
            User: The updated user object
        """
        logger.info(f"Updating user information for user ID: {user_id}")

        async with self.sessionmaker() as session:
            logger.debug(f"Updating user with repository")
            updated_user = await self.user_repository.update(user_id, session, **kwargs)
            await session.commit()

            logger.info(f"Successfully updated information for user ID: {user_id}")
            return updated_user
