from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.exc import MultipleResultsFound
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.exceptions.app_exception import DuplicateEntryException
from src.domain.exceptions.film_trailer_exceptions import FilmTrailerNotFoundException
from src.domain.models.film_trailer import FilmTrailer
from src.domain.repositories.film_trailer_repository import FilmTrailerRepository
from src.infrastructure.database.models import FilmTrailerEntity
from src.infrastructure.database.models.mappers.film_trailer_entity_mappers import (
    FilmTrailerEntityMappers,
)


class FilmTrailerRepositoryImpl(FilmTrailerRepository):
    """Implementation of FilmTrailerRepository using SQLAlchemy."""

    async def create(self, trailer: FilmTrailer, session: AsyncSession) -> FilmTrailer:
        """
        Create a new film trailer.

        Args:
            trailer: The film trailer to create
            session: The database session to use

        Returns:
            The created film trailer with ID
        """
        try:
            trailer_entity = FilmTrailerEntityMappers.from_domain(trailer)
            session.add(trailer_entity)
            await session.flush()
        except MultipleResultsFound as e:
            raise DuplicateEntryException(
                entry_type="FilmTrailer", identifier=trailer.id
            ) from e

        return FilmTrailerEntityMappers.to_domain(trailer_entity)

    async def get_by_id(
        self, trailer_id: str, session: AsyncSession
    ) -> Optional[FilmTrailer]:
        """
        Get a film trailer by its ID.

        Args:
            trailer_id: The ID of the trailer
            session: The database session to use

        Returns:
            The film trailer if found, None otherwise

        Raise:
            DuplicateEntryException: If multiple entries are found with the same ID
        """
        try:
            result = await session.execute(
                select(FilmTrailerEntity).where(FilmTrailerEntity.id == trailer_id)
            )
            trailer_entity = result.scalar_one_or_none()
        except MultipleResultsFound as e:
            raise DuplicateEntryException(
                entry_type="FilmTrailer", identifier=trailer_id
            ) from e

        return (
            FilmTrailerEntityMappers.to_domain(trailer_entity)
            if trailer_entity
            else None
        )

    async def get_by_film_id(
        self, film_id: str, session: AsyncSession
    ) -> List[FilmTrailer]:
        """
        Get all trailers for a specific film.

        Args:
            film_id: The ID of the film
            session: The database session to use

        Returns:
            List of film trailers associated with the film
        """
        result = await session.execute(
            select(FilmTrailerEntity).where(FilmTrailerEntity.film_id == film_id)
        )
        trailer_entities = result.scalars().all()

        return [
            FilmTrailerEntityMappers.to_domain(te)
            for te in trailer_entities
            if te is not None
        ]

    async def update(
        self, trailer_id: str, session: AsyncSession, **kwargs
    ) -> FilmTrailer:
        """
        Update a film trailer by its ID.

        Args:
            trailer_id: The ID of the trailer to update
            session: The database session to use
            **kwargs: Fields to update

        Keyword Args:
            title (str): New title for the trailer (Optional)
            url (str): New URL for the trailer (Optional)
            order_index (int): New order index for the trailer (Optional)

        Returns:
            The updated film trailer
        """
        try:
            result = await session.execute(
                select(FilmTrailerEntity).where(FilmTrailerEntity.id == trailer_id)
            )
            trailer_entity = result.scalar_one_or_none()
        except MultipleResultsFound as e:
            raise DuplicateEntryException(
                entry_type="FilmTrailer", identifier=trailer_id
            ) from e

        if not trailer_entity:
            raise FilmTrailerNotFoundException(trailer_id=trailer_id)

        for attr, value in kwargs.items():
            if value is not None and hasattr(trailer_entity, attr):
                setattr(trailer_entity, attr, value)

        await session.flush(trailer_entity)

        return FilmTrailerEntityMappers.to_domain(trailer_entity)

    async def delete(self, trailer_id: str, session: AsyncSession) -> None:
        """
        Delete a film trailer by its ID.

        Args:
            trailer_id: The ID of the trailer to delete
            session: The database session to use

        Raises:
            FilmTrailerNotFoundException: If the trailer with the given ID is not found
        """
        try:
            result = await session.execute(
                select(FilmTrailerEntity).where(FilmTrailerEntity.id == trailer_id)
            )
            trailer_entity = result.scalar_one_or_none()
        except MultipleResultsFound as e:
            raise DuplicateEntryException(
                entry_type="FilmTrailer", identifier=trailer_id
            ) from e

        if not trailer_entity:
            raise FilmTrailerNotFoundException(trailer_id=trailer_id)

        await session.delete(trailer_entity)
        await session.flush()

    async def reorder_trailers(
        self, film_id: str, trailer_ids: List[str], session: AsyncSession
    ) -> List[FilmTrailer]:
        """
        Reorder the trailers for a film based on the provided list of trailer IDs.

        Args:
            film_id: The ID of the film
            trailer_ids: List of trailer IDs in the desired order
            session: The database session to use

        Returns:
            List of reordered film trailers
        """
        # Get all trailers for the film
        result = await session.execute(
            select(FilmTrailerEntity).where(FilmTrailerEntity.film_id == film_id)
        )
        trailer_entities = result.scalars().all()

        # Create a dictionary of trailers by ID for faster lookup
        trailer_dict = {te.id: te for te in trailer_entities}

        # Verify all trailer IDs exist for the film
        missing_ids = [tid for tid in trailer_ids if tid not in trailer_dict]
        if missing_ids:
            raise FilmTrailerNotFoundException(trailer_id=missing_ids[0])

        # Update order_index based on the position in the trailer_ids list
        for index, trailer_id in enumerate(trailer_ids):
            trailer_dict[trailer_id].order_index = index

        await session.flush(list(trailer_dict.values()))

        # Return trailers in the new order as domain models
        return [
            FilmTrailerEntityMappers.to_domain(trailer_dict[tid]) for tid in trailer_ids
        ]
