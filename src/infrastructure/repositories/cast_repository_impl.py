from typing import Optional

from sqlalchemy import select
from sqlalchemy.exc import MultipleResultsFound
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import PAGE_DEFAULT, PAGE_SIZE_DEFAULT
from src.domain.exceptions.app_exception import DuplicateEntryException
from src.domain.exceptions.cast_exceptions import CastNotFoundException
from src.domain.models.cast import Cast
from src.domain.repositories.cast_repository import CastRepository
from src.infrastructure.database.models.cast_entity import CastEntity
from src.infrastructure.database.models.mappers.cast_entity_mappers import (
    CastEntityMappers,
)


class CastRepositoryImpl(CastRepository):

    async def get_by_id(self, cast_id: str, session: AsyncSession) -> Optional[Cast]:
        """
        Retrieve a cast member by their ID.

        Args:
            cast_id (str): The ID of the cast member.
            session: The database session to use

        Returns:
            Optional[Cast]: The cast member if found, otherwise None.

        Raises:
            DuplicateEntryException: If multiple cast members with the same ID are found.
        """
        result = await session.execute(
            select(CastEntity).where(CastEntity.id == cast_id)
        )
        try:
            entity = result.scalar_one_or_none()
        except MultipleResultsFound as e:
            raise DuplicateEntryException(entry_type="Cast", identifier=cast_id) from e
        return CastEntityMappers.to_domain(entity) if entity else None

    async def create(self, cast: Cast, session: AsyncSession) -> Cast:
        """
        Create a new cast member.

        Args:
            cast (Cast): The cast member to create.
            session: The database session to use

        Returns:
            Cast: The created cast member.
        """
        entity = CastEntityMappers.from_domain(cast)
        session.add(entity)
        await session.flush()
        return CastEntityMappers.to_domain(entity)

    async def update(self, cast_id: str, session: AsyncSession, **kwargs) -> Cast:
        """
        Update an existing cast member.

        Args:
            cast_id (str): The ID of the cast member to update.
            session: The database session to use
            **kwargs: The fields to update with their new values.

        Keyword Args:
            name (str, optional): The new name of the cast member.
            avatar_image_url (str, optional): The new avatar image URL.
            date_of_birth (date, optional): The new date of birth.
            biography (str, optional): The new biography text.

        Returns:
            Cast: The updated cast member domain model.

        Raises:
            CastNotFoundException: If the cast member with the given ID does not exist.
            DuplicateEntryException: If multiple cast members with the same ID are found.
        """
        result = await session.execute(
            select(CastEntity).where(CastEntity.id == cast_id)
        )
        try:
            cast_entity = result.scalar_one_or_none()
        except MultipleResultsFound as e:
            raise DuplicateEntryException(entry_type="Cast", identifier=cast_id) from e

        if not cast_entity:
            raise CastNotFoundException(cast_id=cast_id)

        for attr, value in kwargs.items():
            if value is not None and hasattr(cast_entity, attr):
                setattr(cast_entity, attr, value)

        await session.flush()
        return CastEntityMappers.to_domain(cast_entity)

    async def delete(self, cast_id: str, session: AsyncSession) -> None:
        """
        Delete a cast member by their ID.

        Args:
            cast_id (str): The ID of the cast member to delete.
            session: The database session to use

        Raises:
            CastNotFoundException: If the cast member with the given ID does not exist.
            DuplicateEntryException: If multiple cast members with the same ID are found.
        """
        result = await session.execute(
            select(CastEntity).where(CastEntity.id == cast_id)
        )
        try:
            cast_entity = result.scalar_one_or_none()
        except MultipleResultsFound as e:
            raise DuplicateEntryException(entry_type="Cast", identifier=cast_id) from e

        if not cast_entity:
            raise CastNotFoundException(cast_id=cast_id)

        await session.delete(cast_entity)

    async def get_all(
        self,
        session: AsyncSession,
        page: int = PAGE_DEFAULT,
        page_size: int = PAGE_SIZE_DEFAULT,
    ) -> list[Cast]:
        """
        Retrieve all cast members with pagination.

        Args:
            session: The database session to use
            page (int): The page number to retrieve.
            page_size (int): The number of items per page.

        Returns:
            list[Cast]: A list of cast members for the specified page.
        """
        offset = (page - 1) * page_size

        result = await session.execute(
            select(CastEntity).offset(offset).limit(page_size)
        )
        cast_entities = result.scalars().all()

        return CastEntityMappers.to_domains(cast_entities)
