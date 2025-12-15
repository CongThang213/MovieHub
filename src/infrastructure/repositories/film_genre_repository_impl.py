from typing import List

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.models.film_genre import FilmGenre
from src.domain.repositories.film_genre_repository import FilmGenreRepository
from src.infrastructure.database.models.film_genre_entity import FilmGenreEntity


class FilmGenreRepositoryImpl(FilmGenreRepository):
    """Implementation of FilmGenreRepository using SQLAlchemy."""

    async def create(self, film_genre: FilmGenre, session: AsyncSession) -> FilmGenre:
        """Create a new film-genre association.

        Args:
            film_genre: The film-genre association to create
            session: The database session to use

        Returns:
            FilmGenre: The created film-genre association
        """
        film_genre_entity = FilmGenreEntity(
            film_id=film_genre.film_id,
            genre_id=film_genre.genre_id,
        )
        session.add(film_genre_entity)
        await session.flush()
        return film_genre

    async def delete_by_film_id(self, film_id: str, session: AsyncSession) -> None:
        """Delete all genre associations for a film.

        Args:
            film_id: The ID of the film
            session: The database session to use
        """
        stmt = delete(FilmGenreEntity).where(FilmGenreEntity.film_id == film_id)
        await session.execute(stmt)
        await session.flush()

    async def get_by_film_id(
        self, film_id: str, session: AsyncSession
    ) -> List[FilmGenre]:
        """Get all genre associations for a film.

        Args:
            film_id: The ID of the film
            session: The database session to use

        Returns:
            List[FilmGenre]: List of film-genre associations
        """
        stmt = select(FilmGenreEntity).where(FilmGenreEntity.film_id == film_id)
        result = await session.execute(stmt)
        entities = result.scalars().all()

        return [
            FilmGenre(film_id=entity.film_id, genre_id=entity.genre_id)
            for entity in entities
        ]

    async def delete_by_film_and_genre(
        self, film_id: str, genre_id: str, session: AsyncSession
    ) -> None:
        """Delete a specific film-genre association.

        Args:
            film_id: The ID of the film
            genre_id: The ID of the genre
            session: The database session to use
        """
        stmt = delete(FilmGenreEntity).where(
            FilmGenreEntity.film_id == film_id, FilmGenreEntity.genre_id == genre_id
        )
        await session.execute(stmt)
        await session.flush()
