from firebase_admin import auth
from firebase_admin.exceptions import FirebaseError

from config.logging_config import logger
from src.application.exceptions.auth_exceptions import (
    AuthenticationError,
    UserAlreadyExistsError,
)
from src.application.services.auth_service import AuthService


class FirebaseAuthService(AuthService):

    def sign_up(self, **kwargs) -> str:
        email = kwargs.get("email")
        password = kwargs.get("password")

        if not email or not password:
            raise AuthenticationError("Email and password are required for sign up")

        try:
            # Check if the user already exists
            logger.debug(f"Checking if user already exists with email: {email}")
            auth.get_user_by_email(email)
            logger.warning(f"User with email {email} already exists")
            raise UserAlreadyExistsError(email=email)
        except auth.UserNotFoundError:
            logger.debug(f"User with email {email} not found, proceeding with creation")
        except UserAlreadyExistsError:
            raise  # Re-raise the specific exception to avoid being caught by the generic handler
        except Exception as e:
            logger.error(f"Error checking if user exists: {str(e)}")
            raise AuthenticationError(f"Error checking if user exists: {str(e)}")

        try:
            # Create a new user
            firebase_user = auth.create_user(
                email=email,
                password=password,
                display_name=kwargs.get("display_name", ""),
                photo_url=kwargs.get("photo_url") or None,
            )
            logger.success(
                f"Successfully created Firebase user with UID: {firebase_user.uid}"
            )
            return firebase_user.uid
        except ValueError as e:
            logger.error(f"Invalid input: {str(e)}")
            raise AuthenticationError(f"Invalid input: {str(e)}")
        except FirebaseError as e:
            logger.error(f"Failed to create user: {str(e)}")
            raise AuthenticationError(f"Failed to create user: {str(e)}")

    def delete_user(self, uid: str) -> None:
        """Delete a Firebase user account by UID

        Args:
            uid: The Firebase user ID to delete

        Raises:
            AuthenticationError: If the account deletion fails
        """
        try:
            logger.debug(f"Attempting to delete Firebase user with UID: {uid}")
            auth.delete_user(uid)
            logger.success(f"Successfully deleted Firebase user with UID: {uid}")
        except ValueError as e:
            logger.error(f"Invalid user ID format: {str(e)}")
            raise AuthenticationError(f"Invalid user ID format: {str(e)}")
        except auth.UserNotFoundError:
            logger.warning(f"User with UID {uid} not found, nothing to delete")
            # Not raising an exception as the end goal (user not existing) is achieved
        except FirebaseError as e:
            logger.error(f"Failed to delete user: {str(e)}")
            raise AuthenticationError(f"Failed to delete user: {str(e)}")

    def generate_password_reset_link(self, email: str) -> dict[str, str]:
        """Generate a password reset link for the given email

        Args:
            email: The email address of the user to send the password reset link to

        Returns:
            dict: A dictionary containing the following keys:
                - action_url: The password reset link URL
                - name: The corresponding user's display name

        Raises:
            AuthenticationError: If generating the password reset link fails
        """
        try:
            user = auth.get_user_by_email(email)
            action_url = auth.generate_password_reset_link(email)
            return {"action_url": action_url, "name": user.display_name}
        except auth.UserNotFoundError:
            # For security reasons, we do not reveal whether the user exists or not
            logger.warning(f"User with email {email} not found")
        except ValueError as e:
            logger.error(f"Invalid email format: {str(e)}")
            raise AuthenticationError(f"Invalid email format: {str(e)}")
        except FirebaseError as e:
            logger.error(f"Failed to send password reset email: {str(e)}")
            raise AuthenticationError(f"Failed to send password reset email: {str(e)}")

    async def validate_token(self, token: str) -> dict:
        """Validate Firebase ID token and return decoded token data

        Args:
            token: The Firebase ID token to validate

        Returns:
            dict: Decoded token data including uid, email, custom claims, etc.

        Raises:
            AuthenticationError: If token validation fails
        """
        try:
            logger.debug(f"Validating Firebase token")
            decoded_token = auth.verify_id_token(token)
            logger.debug(
                f"Token validation successful for user: {decoded_token.get('uid')}"
            )
            return decoded_token
        except ValueError as e:
            logger.error(f"Invalid token format: {str(e)}")
            raise AuthenticationError(f"Invalid token format: {str(e)}")
        except FirebaseError as e:
            logger.error(f"Token validation failed: {str(e)}")
            raise AuthenticationError(f"Token validation failed: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error during token validation: {str(e)}")
            raise AuthenticationError(f"Token validation failed: {str(e)}")
