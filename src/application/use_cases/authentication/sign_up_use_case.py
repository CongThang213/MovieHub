from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from config.logging_config import logger
from src.application.services.auth_service import AuthService
from src.domain.models.user import User
from src.domain.repositories.user_repository import UserRepository


class SignUpUseCase:

    def __init__(
        self,
        auth_service: AuthService,
        user_repository: UserRepository,
        sessionmaker: async_sessionmaker[AsyncSession],
    ) -> None:
        self._auth_service = auth_service
        self._user_repository = user_repository
        self._sessionmaker = sessionmaker

    async def execute(self, user: User, password: str) -> User:
        """Execute the sign-up use case to register a new user.

        This method performs the following steps:
            1. Validate the user data (email, password, etc.)
            2. Create the user in Firebase Authentication.
            3. Store the user information in the application database.
            4. Return the created User object with the Firebase user ID.

        The operations are coordinated in a way that if database persistence fails,
        we have a way to handle the rollback appropriately.

        Args:
            user (User): The user object containing user details.
            password (str): The password for the user account.
        Returns:
            User: The created user object with the Firebase user ID.

        Raises:
            AuthenticationError: If there is an error during authentication.
            UserAlreadyExistsError: If the user already exists in Firebase.
        """
        logger.info(f"Starting sign-up process for user with email: {user.email}")

        # Step 1: Create the user in Firebase Authentication
        logger.debug("Calling Firebase authentication service to create user")
        firebase_user_id = self._auth_service.sign_up(
            email=user.email,
            password=password,
            display_name=user.name,
        )

        # Step 2: Add the Firebase user ID to the User model
        logger.debug(f"Assigning Firebase UID to user: {firebase_user_id}")
        user.id = firebase_user_id

        # Step 3: Store the user in the database
        logger.debug("Saving user to database")
        try:
            async with self._sessionmaker() as session:
                created_user = await self._user_repository.create(user, session)
                await session.commit()
                logger.success(f"User successfully created with ID: {created_user.id}")
                return created_user
        except Exception:
            # If there is an error, roll back by deleting the Firebase user.
            self._auth_service.delete_user(firebase_user_id)
            raise
