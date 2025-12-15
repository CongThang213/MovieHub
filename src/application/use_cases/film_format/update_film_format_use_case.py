from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.domain.models.flim_format import FilmFormat
from src.domain.repositories.film_format_repository import FilmFormatRepository


class UpdateFilmFormatUseCase:

    def __init__(
        self,
        film_format_repository: FilmFormatRepository,
        sessionmaker: async_sessionmaker[AsyncSession],
    ):
        self._film_format_repository = film_format_repository
        self._sessionmaker = sessionmaker

    async def execute(self, film_format_id: str, **kwargs) -> FilmFormat:
        """Update a film format by its ID.

        Args:
            film_format_id: The ID of the film format to update
            **kwargs: The fields to update with their new values

        Keyword Args:
            name: The new name of the film format (optional)
            surcharge: The new surcharge of the film format (optional)
            description: The new description of the film format (optional)

        Returns:
            The updated FilmFormat domain model
        """
        async with self._sessionmaker() as session:
            result = await self._film_format_repository.update(
                film_format_id, session, **kwargs
            )
            await session.commit()
            return result
