from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.domain.models.film_cast import FilmCast
from src.domain.repositories.film_cast_repository import FilmCastRepository


class UpdateFilmCastUseCase:
    """Use case for updating a film-cast relationship."""

    def __init__(
        self,
        film_cast_repository: FilmCastRepository,
        sessionmaker: async_sessionmaker[AsyncSession],
    ):
        self._film_cast_repository = film_cast_repository
        self._sessionmaker = sessionmaker

    async def execute(self, film_id: str, cast_id: str, **kwargs) -> FilmCast:
        """Execute the use case to update a film-cast relationship.

        Args:
            film_id: The ID of the film
            cast_id: The ID of the cast member
            **kwargs: The fields to update with their new values.

        Keyword Args:
            role (str): The new role of the cast member. (optional)
            character_name (str): The new character name. (optional)

        Returns:
            The updated film_cast domain model
        """
        async with self._sessionmaker() as session:
            result = await self._film_cast_repository.update(
                film_id, cast_id, session, **kwargs
            )
            await session.commit()
            return result
