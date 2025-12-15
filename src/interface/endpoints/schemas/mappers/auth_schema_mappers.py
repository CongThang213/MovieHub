from src.domain.models.user import User
from src.interface.endpoints.schemas.auth_schemas import SignUpUserData
from src.interface.endpoints.schemas.user_schemas import UserResponse


class AuthSchemaMappers:
    @staticmethod
    def to_domain(sign_up_data: SignUpUserData) -> User:
        """Maps SignUpUserData to User model.
        Args:
            sign_up_data (SignUpUserData): The sign-up user data.

        Returns:
            User: The User model populated with data from the sign-up request.
        """
        return User(
            email=str(sign_up_data.email),
            name=sign_up_data.name,
        )

    @staticmethod
    def to_user_response(user: User, avatar_url: str = None) -> UserResponse:
        """Maps domain User model to UserResponse schema.

        Args:
            user (User): The domain User model.
            avatar_url (str, optional): The avatar URL from the Image table.

        Returns:
            UserResponse: The API response schema populated with data from the domain user.
        """
        return UserResponse(
            id=user.id,
            name=user.name,
            email=user.email,
            account_type=user.account_type,
            avatar_image_url=avatar_url,
            date_of_birth=user.date_of_birth,
            created_at=user.created_at,
        )
