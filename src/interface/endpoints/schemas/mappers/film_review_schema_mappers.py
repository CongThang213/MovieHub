from typing import Union

from src.domain.models.film_review import FilmReview
from src.domain.models.film_review_with_author import FilmReviewWithAuthor
from src.interface.endpoints.schemas.film_review_schemas import (
    FilmReviewCreateRequest,
    FilmReviewSchema,
)


class FilmReviewSchemaMappers:
    """Mappers for converting between film review schemas and domain models."""

    @staticmethod
    def to_domain(schema: FilmReviewCreateRequest, author_id: str) -> FilmReview:
        """Convert schema to domain model.

        Args:
            schema: The schema to convert
            author_id: The ID of the user creating the review

        Returns:
            FilmReview domain model
        """
        return FilmReview(
            film_id=schema.film_id,
            author_id=author_id,
            rating=schema.rating,
            content=schema.content,
        )

    @staticmethod
    def to_schema(domain: FilmReview) -> FilmReviewSchema:
        """Convert domain model to schema.

        def to_schema(domain: Union[FilmReview, FilmReviewWithAuthor]) -> FilmReviewSchema:
                domain: The domain model to convert

            Returns:
                domain: The domain model to convert (FilmReview or FilmReviewWithAuthor)
        """
        # Check if it's a FilmReviewWithAuthor
        if isinstance(domain, FilmReviewWithAuthor):
            return FilmReviewSchema(
                id=domain.id,
                film_id=domain.film_id,
                author_id=domain.author_id,
                author_name=domain.author_name,
                avatar_url=domain.avatar_url,
                rating=domain.rating,
                content=domain.content,
                created_at=domain.created_at,
            )
        else:
            # FilmReview - provide default values for author fields
            return FilmReviewSchema(
                id=domain.id,
                film_id=domain.film_id,
                author_id=domain.author_id,
                author_name="Unknown",
                avatar_url=None,
                rating=domain.rating,
                content=domain.content,
                created_at=domain.created_at,
            )
