from typing import Optional, List

from sqlalchemy import select, func
from sqlalchemy.exc import MultipleResultsFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.config import PAGE_DEFAULT, PAGE_SIZE_DEFAULT
from src.domain.exceptions.app_exception import DuplicateEntryException
from src.domain.exceptions.film_exceptions import FilmNotFoundException
from src.domain.models.film import Film
from src.domain.models.film_brief import FilmBrief
from src.domain.models.film_detail import FilmDetail
from src.domain.repositories.film_repository import FilmRepository
from src.infrastructure.database.models import (
    FilmGenreEntity,
    FilmEntity,
    FilmCastEntity,
)
from src.infrastructure.database.models.mappers.film_entity_mappers import (
    FilmEntityMappers,
)


class FilmRepositoryImpl(FilmRepository):
    """Implementation of FilmRepository using SQLAlchemy."""

    async def get_all(
        self,
        session: AsyncSession,
        page: int = PAGE_DEFAULT,
        page_size: int = PAGE_SIZE_DEFAULT,
        **kwargs,
    ) -> List[FilmBrief]:
        """Get all films with brief info, including genres and film_format.

        Args:
            session: The database session to use
            page (int): The page number (1-based). Defaults to PAGE_DEFAULT.
            page_size (int): The number of records per page. Defaults to PAGE_SIZE_DEFAULT.
            **kwargs: Optional filters such as genre, release_date, rating, etc.

        Keyword Args:
            genres (List): Filter films by genres.
            rating (float): Filter films by minimum rating.
            title (str): Filter films by title keyword.
            movie_begin_date (datetime): Filter films that start showing on or after this date.
            movie_end_date (datetime): Filter films that end showing on or before this date.

        Returns:
            List[FilmBrief]: A list of films for the specified page and filters.
        """
        offset = (page - 1) * page_size

        query = (
            select(FilmEntity)
            .options(
                joinedload(FilmEntity.film_genres).joinedload(FilmGenreEntity.genre),
                joinedload(FilmEntity.images),
            )
            .offset(offset)
            .limit(page_size)
        )

        # Apply filters based on kwargs if provided.
        if rating := kwargs.get("rating"):
            query = query.where(FilmEntity.rating >= rating)

        if title := kwargs.get("title"):
            query = query.where(FilmEntity.title == title)

        if movie_begin_date := kwargs.get("movie_begin_date"):
            query = query.where(FilmEntity.movie_begin_date == movie_begin_date)

        if movie_end_date := kwargs.get("movie_end_date"):
            query = query.where(FilmEntity.movie_end_date == movie_end_date)

        genres = kwargs.get("genres")
        if genres and isinstance(genres, list):
            query = query.join(
                FilmGenreEntity, FilmGenreEntity.film_id == FilmEntity.id
            ).where(FilmGenreEntity.genre.in_(genres))

        # Execute the query and fetch results.
        result = await session.execute(query)
        film_entities = result.unique().scalars().all()

        # Use mappers to convert entities to domain models
        return [FilmEntityMappers.to_domain_brief(entity) for entity in film_entities]

    async def get_by_id(
        self, film_id: str, session: AsyncSession
    ) -> Optional[FilmDetail]:
        """Retrieve a film by its ID, including all related data for detailed view."""
        query = (
            select(FilmEntity)
            .where(FilmEntity.id == film_id)
            .options(
                joinedload(FilmEntity.film_genres).joinedload(FilmGenreEntity.genre),
                joinedload(FilmEntity.film_casts).joinedload(FilmCastEntity.cast),
                joinedload(FilmEntity.trailers),
                joinedload(FilmEntity.showtimes),
                joinedload(FilmEntity.reviews),
                joinedload(FilmEntity.promotions),
                joinedload(FilmEntity.images),
            )
        )
        try:
            result = await session.execute(query)
            film_entity = result.unique().scalar_one_or_none()
        except MultipleResultsFound as e:
            raise DuplicateEntryException(entry_type="Film", identifier=film_id) from e

        # Use mapper to convert entity to domain model
        return FilmEntityMappers.to_domain_detail(film_entity) if film_entity else None

    async def create(self, film: Film, session: AsyncSession) -> Film:
        """Create a new film in the database.

        Args:
            film: The film domain model to create
            session: The database session to use

        Returns:
            Film: The created film with updated ID
        """
        try:
            film_entity = FilmEntityMappers.from_domain(film)
            session.add(film_entity)
            await session.flush()

            result = await session.execute(
                select(FilmEntity)
                .options(joinedload(FilmEntity.images))
                .where(FilmEntity.id == film_entity.id)
            )

            # Use unique() to deduplicate rows from joined collections before scalar_one()
            film_entity_with_images = result.unique().scalar_one()
        except MultipleResultsFound as e:
            raise DuplicateEntryException(entry_type="Film", identifier=film.id) from e

        # Return the domain model with the updated ID
        return FilmEntityMappers.to_domain(film_entity_with_images)

    async def update(self, film_id: str, session: AsyncSession, **kwargs) -> Film:
        """Update film by id

        Args:
            film_id (str): The id of the film to update.
            session: The database session to use
            **kwargs: The fields to update with their new values.

        Keyword Args:
            title (str): The new title of the film. (optional)
            votes (int): The new number of votes. (optional)
            rating (float): The new rating of the film. (optional)
            description (str): The new description of the film. (optional)
            duration_minutes (int): The new duration in minutes. (optional)
            movie_begin_date (datetime): The new movie begin date. (optional)
            movie_end_date (datetime): The new movie end date. (optional)

        Returns:
            Film: The updated film.
        """
        result = await session.execute(
            select(FilmEntity).where(FilmEntity.id == film_id)
        )
        try:
            film_entity = result.scalar_one_or_none()
        except MultipleResultsFound as e:
            raise DuplicateEntryException(entry_type="Film", identifier=film_id) from e

        if not film_entity:
            raise FilmNotFoundException(film_id=film_id)

        for attr, value in kwargs.items():
            if value is not None and hasattr(film_entity, attr):
                setattr(film_entity, attr, value)

        await session.flush()

        # Return the updated domain model
        return FilmEntityMappers.to_domain(film_entity)

    async def delete(self, film_id: str, session: AsyncSession):
        """Delete film by id

        Args:
            film_id (str): The id of the film to delete.
            session: The database session to use
        """
        try:
            result = await session.execute(
                select(FilmEntity).where(FilmEntity.id == film_id)
            )
            film_entity = result.scalars().first()
        except MultipleResultsFound as e:
            raise DuplicateEntryException(entry_type="Film", identifier=film_id) from e

        if not film_entity:
            raise FilmNotFoundException(film_id=film_id)

        await session.delete(film_entity)
        await session.flush()

    async def search(
        self,
        session: AsyncSession,
        page: int = PAGE_DEFAULT,
        page_size: int = PAGE_SIZE_DEFAULT,
        **kwargs,
    ) -> List[FilmBrief]:
        """Search films with advanced filters.

        Args:
            session: The database session to use
            page: The page number (1-based)
            page_size: The number of records per page
            **kwargs: Filter options

        Returns:
            List[FilmBrief]: A list of films matching the filters
        """
        offset = (page - 1) * page_size

        query = (
            select(FilmEntity)
            .options(
                joinedload(FilmEntity.film_genres).joinedload(FilmGenreEntity.genre),
                joinedload(FilmEntity.images),
            )
            .offset(offset)
            .limit(page_size)
        )

        # Apply filters
        query = self._apply_filters(query, **kwargs)

        # Execute the query and fetch results
        result = await session.execute(query)
        film_entities = result.unique().scalars().all()

        # Use mappers to convert entities to domain models
        return [FilmEntityMappers.to_domain_brief(entity) for entity in film_entities]

    async def count(self, session: AsyncSession, **kwargs) -> int:
        """Count films matching the given filters.

        Args:
            session: The database session to use
            **kwargs: Filter options

        Returns:
            int: Total count of films matching the filters
        """
        query = select(func.count(FilmEntity.id))

        # Apply filters
        query = self._apply_filters(query, **kwargs)

        result = await session.execute(query)
        return result.scalar_one()

    def _apply_filters(self, query, **kwargs):
        """Apply filters to a query based on kwargs.

        Args:
            query: The SQLAlchemy query to filter
            **kwargs: Filter options

        Returns:
            The filtered query
        """
        # Title filter (partial match, case-insensitive)
        if title := kwargs.get("title"):
            query = query.where(FilmEntity.title.ilike(f"%{title}%"))

        # Rating filters
        if min_rating := kwargs.get("min_rating"):
            query = query.where(FilmEntity.rating >= min_rating)

        if max_rating := kwargs.get("max_rating"):
            query = query.where(FilmEntity.rating <= max_rating)

        # Duration filters
        if min_duration := kwargs.get("min_duration"):
            query = query.where(FilmEntity.duration_minutes >= min_duration)

        if max_duration := kwargs.get("max_duration"):
            query = query.where(FilmEntity.duration_minutes <= max_duration)

        # Date filters (films showing in a specific time period)
        if showing_from := kwargs.get("showing_from"):
            query = query.where(FilmEntity.movie_end_date >= showing_from)

        if showing_until := kwargs.get("showing_until"):
            query = query.where(FilmEntity.movie_begin_date <= showing_until)

        # Genre filter (films with any of the specified genres)
        if genres := kwargs.get("genres"):
            if isinstance(genres, list) and genres:
                from src.infrastructure.database.models.genre_entity import GenreEntity

                query = (
                    query.join(
                        FilmGenreEntity, FilmGenreEntity.film_id == FilmEntity.id
                    )
                    .join(GenreEntity, GenreEntity.id == FilmGenreEntity.genre_id)
                    .where(GenreEntity.name.in_(genres))
                )

        return query
