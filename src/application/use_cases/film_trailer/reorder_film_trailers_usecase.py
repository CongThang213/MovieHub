from typing import List

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.domain.models.film_trailer import FilmTrailer
from src.domain.repositories.film_trailer_repository import FilmTrailerRepository


class ReorderFilmTrailersUseCase:
    """Use case for reordering trailers for a specific film."""

    def __init__(
        self,
        film_trailer_repository: FilmTrailerRepository,
        sessionmaker: async_sessionmaker[AsyncSession],
    ):
        self._film_trailer_repository = film_trailer_repository
        self._sessionmaker = sessionmaker

    async def execute(self, film_id: str, trailer_ids: List[str]) -> List[FilmTrailer]:
        """Reorder the trailers for a film based on the provided list of trailer IDs.

        Args:
            film_id: The ID of the film.
            trailer_ids: Ordered list of trailer IDs representing the new order.

        Returns:
            The updated list of film trailers in the new order.
        """
        async with self._sessionmaker() as session:
            result = await self._film_trailer_repository.reorder_trailers(
                film_id, trailer_ids, session
            )
            await session.commit()
            return result
