from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from config.logging_config import logger
from src.application.exceptions.auth_exceptions import ServiceUserNotFoundError
from src.domain.models.user import User
from src.domain.repositories.user_repository import UserRepository


class GetUserUseCase:
    """
    Use case for retrieving user information.

    This use case handles the business logic for fetching user data,
    including validation and error handling.
    """

    def __init__(
        self,
        user_repository: UserRepository,
        sessionmaker: async_sessionmaker[AsyncSession],
    ):
        """
        Initialize the use case with required dependencies.

        Args:
            user_repository: Repository for user data operations
            sessionmaker: Database session factory
        """
        self._user_repository = user_repository
        self._sessionmaker = sessionmaker

    async def execute(self, user_id: str) -> User:
        """
        Execute the get user use case.

        Args:
            user_id: The ID of the user to retrieve

        Returns:
            User: The user domain model

        Raises:
            ServiceUserNotFoundError: If the user doesn't exist
        """
        logger.info(f"Retrieving user information for user ID: {user_id}")

        try:
            async with self._sessionmaker() as session:
                user = await self._user_repository.get_by_id(user_id, session)

                if not user:
                    logger.warning(f"User not found with ID: {user_id}")
                    raise ServiceUserNotFoundError(f"User with ID {user_id} not found")

                logger.info(f"Successfully retrieved user: {user.email}")
                return user

        except ServiceUserNotFoundError:
            raise
        except Exception as e:
            logger.error(f"Error retrieving user {user_id}: {str(e)}")
            raise
