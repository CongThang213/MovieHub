from typing import Optional

import cloudinary
from sqlalchemy.inspection import inspect
from sqlalchemy.orm.base import NO_VALUE

from src.domain.enums.image_type import ImageType
from src.domain.models.film import Film
from src.domain.models.film_brief import FilmBrief
from src.domain.models.film_cast import FilmCast
from src.domain.models.film_detail import FilmDetail
from src.domain.models.film_promotion import FilmPromotion
from src.domain.models.film_trailer import FilmTrailer
from src.infrastructure.database.models import FilmEntity


class FilmEntityMappers:
    @staticmethod
    def to_domain(entity: FilmEntity) -> Film:
        """Convert a FilmEntity to a Film domain model.

        Args:
            entity (FilmEntity): The FilmEntity instance to convert.

        Returns:
            Film: The corresponding Film domain model.
        """
        thumbnail_url = None
        background_url = None
        poster_url = None

        # Check if images relationship is loaded to avoid triggering lazy load which can cause MissingGreenlet error in async contexts
        inspector = inspect(entity)
        if (
            hasattr(inspector.attrs, "images")
            and inspector.attrs.images.loaded_value is not NO_VALUE
        ):
            for image in entity.images:
                # Build URL from public_id using Cloudinary
                url = cloudinary.CloudinaryImage(image.public_id).build_url(secure=True)

                if image.type == ImageType.FILM_THUMBNAIL:
                    thumbnail_url = url
                elif image.type == ImageType.FILM_BACKGROUND:
                    background_url = url
                elif image.type == ImageType.FILM_POSTER:
                    poster_url = url

        return Film(
            id=entity.id,
            title=entity.title,
            votes=entity.votes,
            rating=entity.rating,
            description=entity.description,
            duration_minutes=entity.duration_minutes,
            thumbnail_image_url=thumbnail_url,
            background_image_url=background_url,
            poster_image_url=poster_url,
            movie_begin_date=entity.movie_begin_date,
            movie_end_date=entity.movie_end_date,
        )

    @staticmethod
    def from_domain(film: Film) -> FilmEntity:
        """Convert a Film domain model to a FilmEntity.

        Args:
            film (Film): The Film domain model to convert.

        Returns:
            FilmEntity: The corresponding FilmEntity instance.
        """
        return FilmEntity(
            id=film.id,
            title=film.title,
            votes=film.votes,
            rating=film.rating,
            description=film.description,
            duration_minutes=film.duration_minutes,
            movie_begin_date=film.movie_begin_date,
            movie_end_date=film.movie_end_date,
        )

    @staticmethod
    def to_domain_brief(entity: FilmEntity) -> FilmBrief:
        """Convert a FilmEntity to a FilmBrief domain model with genres.

        Args:
            entity (FilmEntity): The FilmEntity instance to convert.

        Returns:
            FilmBrief: The corresponding FilmBrief domain model.
        """
        film = FilmEntityMappers.to_domain(entity)

        genres = [fg.genre.name for fg in entity.film_genres if fg.genre is not None]

        return FilmBrief(film=film, genres=genres)

    @staticmethod
    def to_domain_detail(entity: FilmEntity) -> Optional[FilmDetail]:
        """Convert a FilmEntity to a FilmDetail domain model with all related entities.

        Args:
            entity (FilmEntity): The FilmEntity instance to convert.

        Returns:
            FilmDetail: The corresponding FilmDetail domain model.
        """
        if not entity:
            return None

        film = FilmEntityMappers.to_domain(entity)

        # Safely access relationships to avoid MissingGreenlet errors
        inspector = inspect(entity)

        genres = []
        if (
            hasattr(inspector.attrs, "film_genres")
            and inspector.attrs.film_genres.loaded_value is not NO_VALUE
        ):
            genres = [
                fg.genre.name for fg in entity.film_genres if fg.genre is not None
            ]

        cast = []
        if (
            hasattr(inspector.attrs, "film_casts")
            and inspector.attrs.film_casts.loaded_value is not NO_VALUE
        ):
            for film_cast in entity.film_casts:
                film_cast_inspector = inspect(film_cast)
                if (
                    hasattr(film_cast_inspector.attrs, "cast")
                    and film_cast_inspector.attrs.cast.loaded_value is not NO_VALUE
                    and film_cast.cast
                ):
                    cast.append(
                        FilmCast(
                            cast_id=film_cast.cast_id,
                            role=film_cast.role or "Actor",
                            character_name=film_cast.character_name or "",
                        )
                    )

        trailers = []
        if (
            hasattr(inspector.attrs, "trailers")
            and inspector.attrs.trailers.loaded_value is not NO_VALUE
        ):
            trailers = [
                FilmTrailer(
                    id=trailer.id,
                    film_id=trailer.film_id,
                    title=trailer.title or "",
                    url=trailer.url,
                    order_index=trailer.order_index or 0,
                    uploaded_at=trailer.uploaded_at,
                )
                for trailer in entity.trailers
            ]

        showtimes = []
        if (
            hasattr(inspector.attrs, "showtimes")
            and inspector.attrs.showtimes.loaded_value is not NO_VALUE
        ):
            showtimes = [showtime.start_time for showtime in entity.showtimes]

        reviews = []
        if (
            hasattr(inspector.attrs, "reviews")
            and inspector.attrs.reviews.loaded_value is not NO_VALUE
        ):
            reviews = [review.content for review in entity.reviews]

        promotions = []
        if (
            hasattr(inspector.attrs, "promotions")
            and inspector.attrs.promotions.loaded_value is not NO_VALUE
        ):
            promotions = [
                FilmPromotion(
                    id=promo.id,
                    film_id=promo.film_id,
                    type=promo.type.value if promo.type else "",
                    title=promo.title,
                    content=promo.content or "",
                    valid_from=promo.valid_from,
                    valid_until=promo.valid_until,
                )
                for promo in entity.promotions
            ]

        return FilmDetail(
            film=film,
            genres=genres,
            casts=cast,
            trailers=trailers,
            showtimes=showtimes,
            reviews=reviews,
            promotions=promotions,
        )
