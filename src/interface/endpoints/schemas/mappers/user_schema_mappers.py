from src.domain.models.user import User
from src.interface.endpoints.schemas.user_schemas import UserResponse


class UserSchemaMappers:
    @staticmethod
    def to_user_response(user: User) -> UserResponse:
        """Maps domain User model to UserResponse schema.

        Args:
            user (User): The domain User model.

        Returns:
            UserResponse: The API response schema populated with data from the domain user.
        """
        return UserResponse(
            id=user.id,
            name=user.name,
            email=user.email,
            account_type=user.account_type,
            date_of_birth=user.date_of_birth,
            created_at=user.created_at,
        )
