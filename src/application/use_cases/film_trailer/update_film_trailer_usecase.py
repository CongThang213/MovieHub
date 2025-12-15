from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.domain.models.film_trailer import FilmTrailer
from src.domain.repositories.film_trailer_repository import FilmTrailerRepository


class UpdateFilmTrailerUseCase:
    """Use case for updating an existing film trailer."""

    def __init__(
        self,
        film_trailer_repository: FilmTrailerRepository,
        sessionmaker: async_sessionmaker[AsyncSession],
    ):
        self._film_trailer_repository = film_trailer_repository
        self._sessionmaker = sessionmaker

    async def execute(self, trailer_id: str, **kwargs) -> FilmTrailer:
        """Update an existing film trailer.

        Args:
            trailer_id: The ID of the film trailer to update.
            **kwargs: Fields to update.

        Keyword Args:
            title (str): New title for the trailer (Optional)
            url (str): New URL for the trailer (Optional)
            order_index (int): New order index for the trailer (Optional)

        Returns:
            The updated film trailer.
        """
        async with self._sessionmaker() as session:
            result = await self._film_trailer_repository.update(
                trailer_id, session, **kwargs
            )
            await session.commit()
            return result
