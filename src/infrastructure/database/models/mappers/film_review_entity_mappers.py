from typing import List

from src.domain.models.film_review import FilmReview
from src.domain.models.film_review_with_author import FilmReviewWithAuthor
from src.infrastructure.database.models.film_review_entity import FilmReviewEntity


class FilmReviewEntityMappers:
    @staticmethod
    def to_domain(entity: FilmReviewEntity) -> FilmReview:
        """Convert a FilmReviewEntity to a FilmReview domain model.

        Args:
            entity (FilmReviewEntity): The FilmReviewEntity instance to convert.

        Returns:
            FilmReview: The corresponding FilmReview domain model.
        """
        return FilmReview(
            id=entity.id,
            film_id=entity.film_id,
            author_id=entity.author_id,
            rating=entity.rating,
            content=entity.content or "",
            created_at=entity.created_at,
        )

    @staticmethod
    def to_domains(entities: List[FilmReviewEntity]) -> List[FilmReview]:
        """Convert a list of FilmReviewEntity instances to a list of FilmReview domain models.

        Args:
            entities (List[FilmReviewEntity]): The list of FilmReviewEntity instances to convert.

        Returns:
            List[FilmReview]: The corresponding list of FilmReview domain models.
        """
        return [FilmReviewEntityMappers.to_domain(entity) for entity in entities]

    @staticmethod
    @staticmethod
    def to_domain_with_author(entity: FilmReviewEntity) -> FilmReviewWithAuthor:
        """Convert a FilmReviewEntity to a FilmReviewWithAuthor domain model with author details.

        Args:
            entity (FilmReviewEntity): The FilmReviewEntity instance to convert.

        Returns:
            FilmReviewWithAuthor: The corresponding FilmReviewWithAuthor domain model.
        """
        # Get avatar URL from author's image if available
        avatar_url = None
        if hasattr(entity, "author") and entity.author:
            author_name = entity.author.name
            # Check if author has an image relationship
            if hasattr(entity.author, "image") and entity.author.image:
                # Build Cloudinary URL from public_id
                public_id = entity.author.image.public_id
                avatar_url = (
                    f"https://res.cloudinary.com/seatsync/image/upload/{public_id}"
                )
        else:
            author_name = "Unknown"

        return FilmReviewWithAuthor(
            id=entity.id,
            film_id=entity.film_id,
            author_id=entity.author_id,
            author_name=author_name,
            avatar_url=avatar_url,
            rating=entity.rating,
            content=entity.content or "",
            created_at=entity.created_at,
        )

    @staticmethod
    def to_domains_with_author(
        entities: List[FilmReviewEntity],
    ) -> List[FilmReviewWithAuthor]:
        """Convert a list of FilmReviewEntity instances to a list of FilmReviewWithAuthor domain models.

        Args:
            entities (List[FilmReviewEntity]): The list of FilmReviewEntity instances to convert.

        Returns:
            List[FilmReviewWithAuthor]: The corresponding list of FilmReviewWithAuthor domain models.
        """
        return [
            FilmReviewEntityMappers.to_domain_with_author(entity) for entity in entities
        ]
