from typing import List

from src.domain.models.film import Film
from src.domain.models.film_cast import FilmCast
from src.domain.models.film_promotion import FilmPromotion
from src.domain.models.film_trailer import FilmTrailer
from src.interface.endpoints.schemas.film_schemas import FilmSchema


class FilmSchemaMappers:
    """Mappers to convert between film schema and domain models."""

    @staticmethod
    def to_domain(request) -> Film:
        """Convert Film schemas to Film domain model.

        Args:
            request: The film schema

        Returns:
            Film: The film domain model
        """
        args = {
            "title": request.film.title,
            "description": request.film.description,
            "duration_minutes": request.film.duration_minutes,
            "movie_begin_date": request.film.movie_begin_date,
            "movie_end_date": request.film.movie_end_date,
        }

        optional_fields = [
            "id",
            "thumbnail_image_url",
            "poster_image_url",
            "background_image_url",
        ]
        for field in optional_fields:
            if value := getattr(request.film, field, None):
                args[field] = value

        return Film(**args)

    @staticmethod
    def cast_schemas_to_domain(
        cast_schemas: List, film_id: str = None
    ) -> List[FilmCast]:
        """Convert list of FilmCast schemas to domain models.

        Args:
            cast_schemas (List): List of FilmCast schemas
            film_id (str): ID of the film to associate with

        Returns:
            List[FilmCast]: List of FilmCast domain models
        """
        if not cast_schemas:
            return []

        return [
            FilmCast(
                film_id=film_id,
                cast_id=cast_schema.id,
                role=cast_schema.role,
                character_name=cast_schema.character_name,
            )
            for cast_schema in cast_schemas
        ]

    @staticmethod
    def promotion_schemas_to_domain(
        promotion_schemas: List, film_id: str = None
    ) -> List[FilmPromotion]:
        """Convert list of FilmPromotion schemas to domain models.

        Args:
            promotion_schemas (List): List of FilmPromotion schemas
            film_id (str): ID of the film to associate with

        Returns:
            List[FilmPromotion]: List of FilmPromotion domain models
        """
        if not promotion_schemas:
            return []

        return [
            FilmPromotion(
                film_id=film_id,
                type=promo_schema.type,
                title=promo_schema.title,
                content=promo_schema.content,
                valid_from=promo_schema.valid_from,
                valid_until=promo_schema.valid_until,
            )
            for promo_schema in promotion_schemas
        ]

    @staticmethod
    def trailer_schemas_to_domain(
        trailer_schemas: List, film_id: str = None
    ) -> List[FilmTrailer]:
        """Convert list of FilmTrailer schemas to domain models.

        Args:
            trailer_schemas (List): List of FilmTrailer schemas
            film_id (str): ID of the film to associate with

        Returns:
            List[FilmTrailer]: List of FilmTrailer domain models
        """
        if not trailer_schemas:
            return []

        return [
            FilmTrailer(
                film_id=film_id,
                title=trailer_schema.title,
                url=trailer_schema.url,
                order_index=trailer_schema.order_index,
            )
            for trailer_schema in trailer_schemas
        ]

    @staticmethod
    def film_to_schema(film: Film) -> FilmSchema:
        """Convert Film domain model to FilmSchema.

        Args:
            film (Film): The film domain model

        Returns:
            FilmSchema: The film schema
        """
        return FilmSchema(
            id=film.id,
            title=film.title,
            description=film.description,
            duration_minutes=film.duration_minutes,
            movie_begin_date=film.movie_begin_date,
            movie_end_date=film.movie_end_date,
            thumbnail_image_url=getattr(film, "thumbnail_image_url", None),
            background_image_url=getattr(film, "background_image_url", None),
            poster_image_url=getattr(film, "poster_image_url", None),
        )
