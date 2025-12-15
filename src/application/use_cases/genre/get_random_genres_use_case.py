from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from src.domain.models.genre import Genre
from src.domain.repositories.genre_repository import GenreRepository
import random


class GetRandomGenresUseCase:
    def __init__(
        self,
        genre_repository: GenreRepository,
        sessionmaker: async_sessionmaker[AsyncSession],
    ):
        self._genre_repository = genre_repository
        self._sessionmaker = sessionmaker

    async def execute(self, limit: int = 4) -> tuple[list[Genre], int]:
        async with self._sessionmaker() as session:
            genres = await self._genre_repository.get_all_genres(session)
            total_genres = len(genres)
            if limit > total_genres:
                limit = total_genres
            random_genres = random.sample(genres, limit) if total_genres > 0 else []
            return random_genres, total_genres
