from typing import Sequence, List

from src.domain.models.user import User
from src.infrastructure.database.models.user_entity import UserEntity


class UserEntityMapper:

    @staticmethod
    def from_domain(user: User) -> UserEntity:
        return UserEntity(
            id=user.id,
            email=user.email,
            name=user.name,
            account_type=user.account_type,
            created_at=user.created_at,
            date_of_birth=user.date_of_birth,
        )

    @staticmethod
    def to_domain(entity: UserEntity) -> User:
        return User(
            id=entity.id,
            name=entity.name,
            email=entity.email,
            account_type=entity.account_type,
            date_of_birth=entity.date_of_birth,
            created_at=entity.created_at,
        )

    @staticmethod
    def to_domains(entities: Sequence[UserEntity]) -> List[User]:
        return [UserEntityMapper.to_domain(entity) for entity in entities]
