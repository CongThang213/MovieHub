from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.domain.models.film import Film
from src.domain.models.film_cast import FilmCast
from src.domain.models.film_genre import FilmGenre
from src.domain.models.film_promotion import FilmPromotion
from src.domain.models.film_trailer import FilmTrailer
from src.domain.repositories.film_cast_repository import FilmCastRepository
from src.domain.repositories.film_genre_repository import FilmGenreRepository
from src.domain.repositories.film_promotion_repository import FilmPromotionRepository
from src.domain.repositories.film_repository import FilmRepository
from src.domain.repositories.film_trailer_repository import FilmTrailerRepository


class CreateFilmUseCase:
    """Orchestrates creation of a film and its related casts, promotions, and trailers."""

    def __init__(
        self,
        film_repository: FilmRepository,
        film_genre_repository: FilmGenreRepository,
        film_cast_repository: FilmCastRepository,
        film_promotion_repository: FilmPromotionRepository,
        film_trailer_repository: FilmTrailerRepository,
        sessionmaker: async_sessionmaker[AsyncSession],
    ):
        self._film_repository = film_repository
        self._film_genre_repository = film_genre_repository
        self._film_cast_repository = film_cast_repository
        self._film_promotion_repository = film_promotion_repository
        self._film_trailer_repository = film_trailer_repository
        self._sessionmaker = sessionmaker

    async def execute(
        self,
        film: Film,
        genres: Optional[List[str]] = None,
        casts: Optional[List[FilmCast]] = None,
        promotions: Optional[List[FilmPromotion]] = None,
        trailers: Optional[List[FilmTrailer]] = None,
    ) -> Film:
        """Create a film and its related information in a single transaction.

        Args:
            film (Film): Film domain model to create
            genres (List[str]): List of genre IDs to associate with the film (Optional)
            casts (List[FilmCast]): List of FilmCast models to associate (Optional)
            promotions (List[FilmPromotion]): List of FilmPromotion models to associate (Optional)
            trailers (List[FilmTrailer]): List of FilmTrailer models to associate (Optional)

        Returns:
            Film: The created Film model (with related objects attached if needed)
        """
        async with self._sessionmaker() as session:
            try:
                film = await self._film_repository.create(film, session)
                film_id = film.id

                # Associate genres with the film
                if genres:
                    for genre_id in genres:
                        film_genre = FilmGenre(film_id=film_id, genre_id=genre_id)
                        await self._film_genre_repository.create(film_genre, session)

                # Associate casts with the film
                if casts:
                    for cast in casts:
                        cast.film_id = film_id
                        await self._film_cast_repository.create(cast, session)

                # Associate promotions with the film
                if promotions:
                    for promo in promotions:
                        promo.film_id = film_id
                        await self._film_promotion_repository.create(promo, session)

                # Associate trailers with the film
                if trailers:
                    for trailer in trailers:
                        trailer.film_id = film_id
                        await self._film_trailer_repository.create(trailer, session)

                await session.commit()
                return film
            except Exception:
                await session.rollback()
                raise
