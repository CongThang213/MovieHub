from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from src.domain.models.film import Film
from src.domain.repositories.film_repository import FilmRepository


class GetFilmUseCase:
    def __init__(
        self,
        film_repository: FilmRepository,
        sessionmaker: async_sessionmaker[AsyncSession],
    ):
        self._film_repository = film_repository
        self._sessionmaker = sessionmaker

    async def execute(self, film_id: str) -> Film:
        async with self._sessionmaker() as session:
            return await self._film_repository.get_by_id(film_id, session)
