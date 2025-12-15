from abc import ABC, abstractmethod


class AuthService(ABC):
    @abstractmethod
    def sign_up(self, **kwargs) -> str:
        """Create new user account with email and password

        Args:
            **kwargs: A series of keyword arguments.

        Keyword Args:
            email: The email address of the user.
            password: The password for the user account.
            photo_url: The URL of the user's profile photo (optional).

        Return:
            str: The ID of the newly created user account.

        Raises:
            AuthenticationError: If the account creation fails.
            UserAlreadyExistsError: If a user with the given email already exists.
        """
        pass

    @abstractmethod
    def delete_user(self, uid: str) -> None:
        """Delete a user account by user ID

        Args:
            uid: The ID of the user to delete.

        Raises:
            AuthenticationError: If the account deletion fails.
        """
        pass

    @abstractmethod
    def generate_password_reset_link(self, email: str) -> dict[str, str]:
        """Generate the password reset link

        Args:
            email: The email address of the user.

        Returns:
            dict[str, str]: A dictionary containing the password reset link and the display name

        Raises:
            AuthenticationError: If sending the password reset email fails.
            UserNotFoundError: If no user exists with the given email.
        """
        pass

    @abstractmethod
    async def validate_token(self, token: str) -> dict:
        """Validate an authentication token and return user data

        Args:
            token: The authentication token to validate

        Returns:
            dict: User data from the decoded token including uid, email, etc.

        Raises:
            AuthenticationError: If token validation fails
        """
        pass
