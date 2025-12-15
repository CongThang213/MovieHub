from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.domain.models.cast import Cast
from src.domain.repositories.cast_repository import CastRepository


class UpdateCastUseCase:
    """Use case for updating an existing cast member."""

    def __init__(
        self,
        cast_repository: CastRepository,
        sessionmaker: async_sessionmaker[AsyncSession],
    ):
        self._cast_repository = cast_repository
        self._sessionmaker = sessionmaker

    async def execute(self, cast_id: str, **kwargs) -> Cast:
        """Execute the use case to update a cast member.

        Args:
            cast_id: The ID of the cast member to update
            **kwargs: Fields to update with their new values

        Keyword Args:
            name (str, optional): The new name of the cast member
            avatar_image_url (str, optional): The new avatar image URL
            date_of_birth (date, optional): The new date of birth
            biography (str, optional): The new biography text

        Returns:
            The updated cast domain model
        """
        async with self._sessionmaker() as session:
            result = await self._cast_repository.update(cast_id, session, **kwargs)
            await session.commit()
            return result
