from datetime import datetime
from typing import Optional, List

from sqlalchemy import select, delete, and_, or_, func
from sqlalchemy.exc import MultipleResultsFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.domain.exceptions.app_exception import DuplicateEntryException
from src.domain.exceptions.showtime_exceptions import ShowTimeNotFoundException
from src.domain.models.show_time import ShowTime
from src.domain.repositories.showtime_repository import ShowTimeRepository
from src.infrastructure.database.models.hall_entity import HallEntity
from src.infrastructure.database.models.mappers.showtime_entity_mappers import (
    ShowTimeEntityMappers,
)
from src.infrastructure.database.models.showtime_entity import ShowTimeEntity


class ShowTimeRepositoryImpl(ShowTimeRepository):
    """Implementation of ShowTimeRepository using SQLAlchemy."""

    async def create(self, showtime: ShowTime, session: AsyncSession) -> ShowTime:
        """Create a new showtime.

        Args:
            showtime: The showtime domain model to create
            session: The database session

        Returns:
            The created showtime domain model
        """
        showtime_entity = ShowTimeEntityMappers.from_domain(showtime)
        session.add(showtime_entity)
        await session.flush()

        return ShowTimeEntityMappers.to_domain(showtime_entity)

    async def get_by_id(
        self, showtime_id: str, session: AsyncSession
    ) -> Optional[ShowTime]:
        """Get a showtime by ID.

        Args:
            showtime_id: The ID of the showtime
            session: The database session

        Returns:
            The showtime domain model if found, None otherwise
        """
        result = await session.execute(
            select(ShowTimeEntity).where(ShowTimeEntity.id == showtime_id)
        )
        try:
            showtime_entity = result.scalar_one_or_none()
        except MultipleResultsFound as e:
            raise DuplicateEntryException(
                entry_type="ShowTime", identifier=showtime_id
            ) from e

        return (
            ShowTimeEntityMappers.to_domain(showtime_entity)
            if showtime_entity
            else None
        )

    async def get_all(
        self,
        page: int,
        page_size: int,
        session: AsyncSession,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        film_id: Optional[str] = None,
        cinema_id: Optional[str] = None,
    ) -> dict:
        """Get all showtimes with pagination and optional filtering.

        Args:
            page: The page number (1-based)
            page_size: The number of items per page
            session: The database session
            start_date: Optional start date to filter showtimes
            end_date: Optional end date to filter showtimes
            film_id: Optional film ID filter
            cinema_id: Optional cinema ID filter

        Returns:
            Dict containing:
                - showtimes: List of showtime domain models
                - page: Current page number
                - page_size: Number of items per page
                - total: Total number of showtimes
        """
        # Build base query with optional filters and eager loading
        query = select(ShowTimeEntity).options(
            joinedload(ShowTimeEntity.film),
            joinedload(ShowTimeEntity.hall).joinedload(HallEntity.cinema),
            joinedload(ShowTimeEntity.film_format),
        )
        count_query = select(func.count(ShowTimeEntity.id))

        filters = []

        # Apply date range filter
        if start_date:
            filters.append(ShowTimeEntity.start_time >= start_date)
        if end_date:
            filters.append(ShowTimeEntity.start_time <= end_date)

        # Apply film filter
        if film_id:
            filters.append(ShowTimeEntity.film_id == film_id)

        # Apply cinema filter (requires join)
        if cinema_id:
            query = query.join(HallEntity, ShowTimeEntity.hall_id == HallEntity.id)
            count_query = count_query.join(
                HallEntity, ShowTimeEntity.hall_id == HallEntity.id
            )
            filters.append(HallEntity.cinema_id == cinema_id)

        # Add all filters if any exist
        if filters:
            query = query.where(and_(*filters))
            count_query = count_query.where(and_(*filters))

        # Get total count
        count_result = await session.execute(count_query)
        total = count_result.scalar() or 0

        # Get paginated results
        offset = (page - 1) * page_size
        result = await session.execute(query.offset(offset).limit(page_size))
        showtime_entities = result.scalars().all()

        showtimes = ShowTimeEntityMappers.to_domains(showtime_entities)

        return {
            "showtimes": showtimes,
            "page": page,
            "page_size": page_size,
            "total": total,
        }

    async def get_by_film_id(
        self, film_id: str, session: AsyncSession
    ) -> List[ShowTime]:
        """Get all showtimes for a specific film.

        Args:
            film_id: The ID of the film
            session: The database session

        Returns:
            List of showtime domain models
        """
        result = await session.execute(
            select(ShowTimeEntity)
            .options(
                joinedload(ShowTimeEntity.film),
                joinedload(ShowTimeEntity.hall).joinedload(HallEntity.cinema),
                joinedload(ShowTimeEntity.film_format),
            )
            .where(ShowTimeEntity.film_id == film_id)
        )
        showtime_entities = result.scalars().all()

        return ShowTimeEntityMappers.to_domains(showtime_entities)

    async def get_by_hall_id(
        self, hall_id: str, session: AsyncSession
    ) -> List[ShowTime]:
        """Get all showtimes for a specific hall.

        Args:
            hall_id: The ID of the hall
            session: The database session

        Returns:
            List of showtime domain models
        """
        result = await session.execute(
            select(ShowTimeEntity)
            .options(
                joinedload(ShowTimeEntity.film),
                joinedload(ShowTimeEntity.hall).joinedload(HallEntity.cinema),
                joinedload(ShowTimeEntity.film_format),
            )
            .where(ShowTimeEntity.hall_id == hall_id)
        )
        showtime_entities = result.scalars().all()

        return ShowTimeEntityMappers.to_domains(showtime_entities)

    async def get_by_cinema_id(
        self, cinema_id: str, session: AsyncSession
    ) -> List[ShowTime]:
        """Get all showtimes for a specific cinema.

        Args:
            cinema_id: The ID of the cinema
            session: The database session

        Returns:
            List of showtime domain models
        """
        result = await session.execute(
            select(ShowTimeEntity)
            .options(
                joinedload(ShowTimeEntity.film),
                joinedload(ShowTimeEntity.hall).joinedload(HallEntity.cinema),
                joinedload(ShowTimeEntity.film_format),
            )
            .join(HallEntity, ShowTimeEntity.hall_id == HallEntity.id)
            .where(HallEntity.cinema_id == cinema_id)
        )
        showtime_entities = result.scalars().all()

        return ShowTimeEntityMappers.to_domains(showtime_entities)

    async def get_by_date_range(
        self,
        start_date: datetime,
        end_date: datetime,
        session: AsyncSession,
        film_id: Optional[str] = None,
        cinema_id: Optional[str] = None,
    ) -> List[ShowTime]:
        """Get showtimes within a date range with optional filters.

        Args:
            start_date: The start date
            end_date: The end date
            session: The database session
            film_id: Optional film ID filter
            cinema_id: Optional cinema ID filter

        Returns:
            List of showtime domain models
        """
        query = (
            select(ShowTimeEntity)
            .options(
                joinedload(ShowTimeEntity.film),
                joinedload(ShowTimeEntity.hall).joinedload(HallEntity.cinema),
                joinedload(ShowTimeEntity.film_format),
            )
            .where(
                and_(
                    ShowTimeEntity.start_time >= start_date,
                    ShowTimeEntity.start_time <= end_date,
                )
            )
        )

        # Apply optional filters
        if film_id:
            query = query.where(ShowTimeEntity.film_id == film_id)

        if cinema_id:
            query = query.join(
                HallEntity, ShowTimeEntity.hall_id == HallEntity.id
            ).where(HallEntity.cinema_id == cinema_id)

        result = await session.execute(query)
        showtime_entities = result.scalars().all()

        return ShowTimeEntityMappers.to_domains(showtime_entities)

    async def update(self, showtime: ShowTime, session: AsyncSession) -> ShowTime:
        """Update an existing showtime.

        Args:
            showtime: The showtime domain model with updated data
            session: The database session

        Returns:
            The updated showtime domain model
        """
        result = await session.execute(
            select(ShowTimeEntity).where(ShowTimeEntity.id == showtime.id)
        )
        showtime_entity = result.scalar_one_or_none()

        if not showtime_entity:
            raise ShowTimeNotFoundException(showtime.id)

        # Update fields
        if showtime.hall_id:
            showtime_entity.hall_id = showtime.hall_id
        if showtime.film_id:
            showtime_entity.film_id = showtime.film_id
        if showtime.film_format_id:
            showtime_entity.film_format_id = showtime.film_format_id
        if showtime.start_time:
            showtime_entity.start_time = showtime.start_time
        if showtime.end_time:
            showtime_entity.end_time = showtime.end_time
        if showtime.available_seats is not None:
            showtime_entity.available_seats = showtime.available_seats

        await session.flush()

        # Refresh with eager loading to get related entities
        await session.refresh(
            showtime_entity, attribute_names=["film", "hall", "film_format"]
        )
        return ShowTimeEntityMappers.to_domain(showtime_entity)

    async def delete(self, showtime_id: str, session: AsyncSession) -> bool:
        """Delete a showtime.

        Args:
            showtime_id: The ID of the showtime to delete
            session: The database session

        Returns:
            True if deleted successfully, False otherwise
        """
        result = await session.execute(
            select(ShowTimeEntity).where(ShowTimeEntity.id == showtime_id)
        )
        showtime_entity = result.scalar_one_or_none()

        if not showtime_entity:
            raise ShowTimeNotFoundException(showtime_id)

        await session.execute(
            delete(ShowTimeEntity).where(ShowTimeEntity.id == showtime_id)
        )
        await session.flush()
        return True

    async def check_time_conflict(
        self,
        hall_id: str,
        start_time: datetime,
        end_time: datetime,
        session: AsyncSession,
        exclude_showtime_id: Optional[str] = None,
    ) -> bool:
        """Check if there's a time conflict for a hall.

        Args:
            hall_id: The ID of the hall
            start_time: The start time
            end_time: The end time
            session: The database session
            exclude_showtime_id: Optional showtime ID to exclude from conflict check

        Returns:
            True if there's a conflict, False otherwise
        """
        query = select(ShowTimeEntity).where(
            and_(
                ShowTimeEntity.hall_id == hall_id,
                or_(
                    # New showtime starts during an existing showtime
                    and_(
                        ShowTimeEntity.start_time <= start_time,
                        ShowTimeEntity.end_time > start_time,
                    ),
                    # New showtime ends during an existing showtime
                    and_(
                        ShowTimeEntity.start_time < end_time,
                        ShowTimeEntity.end_time >= end_time,
                    ),
                    # New showtime completely contains an existing showtime
                    and_(
                        ShowTimeEntity.start_time >= start_time,
                        ShowTimeEntity.end_time <= end_time,
                    ),
                ),
            )
        )

        # Exclude the showtime being updated from conflict check
        if exclude_showtime_id:
            query = query.where(ShowTimeEntity.id != exclude_showtime_id)

        result = await session.execute(query)
        conflicts = result.scalars().all()

        return len(conflicts) > 0

    # Methods for returning entities with relationships (for responses)
    async def get_entity_by_id(
        self, showtime_id: str, session: AsyncSession
    ) -> Optional[ShowTimeEntity]:
        """Get a showtime entity by ID with all relationships loaded.

        Args:
            showtime_id: The ID of the showtime
            session: The database session

        Returns:
            The showtime entity with relationships if found, None otherwise
        """
        result = await session.execute(
            select(ShowTimeEntity)
            .options(
                joinedload(ShowTimeEntity.film),
                joinedload(ShowTimeEntity.hall).joinedload(HallEntity.cinema),
                joinedload(ShowTimeEntity.film_format),
            )
            .where(ShowTimeEntity.id == showtime_id)
        )
        return result.scalar_one_or_none()

    async def get_entities_all(
        self,
        page: int,
        page_size: int,
        session: AsyncSession,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        film_id: Optional[str] = None,
        cinema_id: Optional[str] = None,
    ) -> dict:
        """Get all showtime entities with pagination and optional filtering.

        Args:
            page: The page number (1-based)
            page_size: The number of items per page
            session: The database session
            start_date: Optional start date to filter showtimes
            end_date: Optional end date to filter showtimes
            film_id: Optional film ID filter
            cinema_id: Optional cinema ID filter

        Returns:
            Dict containing:
                - showtimes: List of showtime entities
                - page: Current page number
                - page_size: Number of items per page
                - total: Total number of showtimes
        """
        query = select(ShowTimeEntity).options(
            joinedload(ShowTimeEntity.film),
            joinedload(ShowTimeEntity.hall).joinedload(HallEntity.cinema),
            joinedload(ShowTimeEntity.film_format),
        )
        count_query = select(func.count(ShowTimeEntity.id))

        filters = []

        if start_date:
            filters.append(ShowTimeEntity.start_time >= start_date)
        if end_date:
            filters.append(ShowTimeEntity.start_time <= end_date)
        if film_id:
            filters.append(ShowTimeEntity.film_id == film_id)
        if cinema_id:
            query = query.join(HallEntity, ShowTimeEntity.hall_id == HallEntity.id)
            count_query = count_query.join(
                HallEntity, ShowTimeEntity.hall_id == HallEntity.id
            )
            filters.append(HallEntity.cinema_id == cinema_id)

        if filters:
            query = query.where(and_(*filters))
            count_query = count_query.where(and_(*filters))

        count_result = await session.execute(count_query)
        total = count_result.scalar() or 0

        offset = (page - 1) * page_size
        result = await session.execute(query.offset(offset).limit(page_size))
        showtime_entities = result.scalars().all()

        return {
            "showtimes": showtime_entities,
            "page": page,
            "page_size": page_size,
            "total": total,
        }

    async def get_entities_by_film_id(
        self, film_id: str, session: AsyncSession
    ) -> List[ShowTimeEntity]:
        """Get all showtime entities for a specific film with relationships loaded.

        Args:
            film_id: The ID of the film
            session: The database session

        Returns:
            List of showtime entities
        """
        result = await session.execute(
            select(ShowTimeEntity)
            .options(
                joinedload(ShowTimeEntity.film),
                joinedload(ShowTimeEntity.hall).joinedload(HallEntity.cinema),
                joinedload(ShowTimeEntity.film_format),
            )
            .where(ShowTimeEntity.film_id == film_id)
        )
        return result.scalars().all()

    async def get_entities_by_hall_id(
        self, hall_id: str, session: AsyncSession
    ) -> List[ShowTimeEntity]:
        """Get all showtime entities for a specific hall with relationships loaded.

        Args:
            hall_id: The ID of the hall
            session: The database session

        Returns:
            List of showtime entities
        """
        result = await session.execute(
            select(ShowTimeEntity)
            .options(
                joinedload(ShowTimeEntity.film),
                joinedload(ShowTimeEntity.hall).joinedload(HallEntity.cinema),
                joinedload(ShowTimeEntity.film_format),
            )
            .where(ShowTimeEntity.hall_id == hall_id)
        )
        return result.scalars().all()

    async def get_entities_by_cinema_id(
        self, cinema_id: str, session: AsyncSession
    ) -> List[ShowTimeEntity]:
        """Get all showtime entities for a specific cinema with relationships loaded.

        Args:
            cinema_id: The ID of the cinema
            session: The database session

        Returns:
            List of showtime entities
        """
        result = await session.execute(
            select(ShowTimeEntity)
            .options(
                joinedload(ShowTimeEntity.film),
                joinedload(ShowTimeEntity.hall).joinedload(HallEntity.cinema),
                joinedload(ShowTimeEntity.film_format),
            )
            .join(HallEntity, ShowTimeEntity.hall_id == HallEntity.id)
            .where(HallEntity.cinema_id == cinema_id)
        )
        return result.scalars().all()

    async def get_showtimes_grouped_by_cinema_and_hall(
        self, film_id: str, session: AsyncSession
    ) -> dict:
        """Get showtimes for a film grouped by cinema and hall.

        Args:
            film_id: The ID of the film
            session: The database session

        Returns:
            Dict containing:
                - film_id: The film ID
                - cinemas: List of cinemas with their halls and showtimes
        """
        # Get all showtimes for the film with relationships
        result = await session.execute(
            select(ShowTimeEntity)
            .options(
                joinedload(ShowTimeEntity.film),
                joinedload(ShowTimeEntity.hall).joinedload(HallEntity.cinema),
                joinedload(ShowTimeEntity.film_format),
            )
            .where(ShowTimeEntity.film_id == film_id)
            .order_by(ShowTimeEntity.start_time)
        )
        showtime_entities = result.scalars().all()

        # Group by cinema and hall
        cinema_dict = {}
        for showtime in showtime_entities:
            cinema = showtime.hall.cinema
            hall = showtime.hall

            # Initialize cinema if not exists
            if cinema.id not in cinema_dict:
                cinema_dict[cinema.id] = {
                    "cinema_id": cinema.id,
                    "cinema_name": cinema.name,
                    "cinema_address": cinema.address,
                    "lon": cinema.long,
                    "lat": cinema.lat,
                    "halls": {},
                }

            # Initialize hall if not exists
            if hall.id not in cinema_dict[cinema.id]["halls"]:
                cinema_dict[cinema.id]["halls"][hall.id] = {
                    "hall_id": hall.id,
                    "hall_name": hall.name,
                    "showtimes": [],
                }

            # Add showtime to hall with simplified format
            cinema_dict[cinema.id]["halls"][hall.id]["showtimes"].append(
                {
                    "id": showtime.id,
                    "film_format": (
                        showtime.film_format.name if showtime.film_format else None
                    ),
                    "start_time": showtime.start_time,
                    "end_time": showtime.end_time,
                }
            )

        # Convert dict to list format
        cinemas = []
        for cinema_data in cinema_dict.values():
            halls = []
            for hall_data in cinema_data["halls"].values():
                halls.append(hall_data)

            cinemas.append(
                {
                    "cinema_id": cinema_data["cinema_id"],
                    "cinema_name": cinema_data["cinema_name"],
                    "cinema_address": cinema_data["cinema_address"],
                    "lon": cinema_data["lon"],
                    "lat": cinema_data["lat"],
                    "halls": halls,
                }
            )

        return {"cinemas": cinemas}
