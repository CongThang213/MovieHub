from typing import List

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.domain.models.film_trailer import FilmTrailer
from src.domain.repositories.film_trailer_repository import FilmTrailerRepository


class GetFilmTrailersByFilmIdUseCase:
    """Use case for retrieving all trailers for a specific film."""

    def __init__(
        self,
        film_trailer_repository: FilmTrailerRepository,
        sessionmaker: async_sessionmaker[AsyncSession],
    ):
        self._film_trailer_repository = film_trailer_repository
        self._sessionmaker = sessionmaker

    async def execute(self, film_id: str) -> List[FilmTrailer]:
        """Retrieve all trailers for a specific film.

        Args:
            film_id: The ID of the film to retrieve trailers for.

        Returns:
            A list of film trailer domain models associated with the film.
        """
        async with self._sessionmaker() as session:
            return await self._film_trailer_repository.get_by_film_id(film_id, session)
