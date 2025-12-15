from src.domain.models.film_trailer import FilmTrailer
from src.infrastructure.database.models import FilmTrailerEntity


class FilmTrailerEntityMappers:
    @staticmethod
    def from_domain(trailer: FilmTrailer) -> FilmTrailerEntity:
        """
        Maps a FilmTrailer domain model to a FilmTrailerEntity database model.

        Arg:
            trailer (FilmTrailer): The domain model to map.

        Returns:
            FilmTrailerEntity: The mapped database model.
        """
        return FilmTrailerEntity(
            id=trailer.id,
            film_id=trailer.film_id,
            title=trailer.title,
            url=trailer.url,
            order_index=trailer.order_index,
            uploaded_at=trailer.uploaded_at,
        )

    @staticmethod
    def to_domain(entity: FilmTrailerEntity) -> FilmTrailer:
        """
        Maps a FilmTrailerEntity database model to a FilmTrailer domain model.

        Arg:
            entity (FilmTrailerEntity): The database model to map.

        Returns:
            FilmTrailer: The mapped domain model.
        """
        return FilmTrailer(
            id=entity.id,
            film_id=entity.film_id,
            title=entity.title,
            url=entity.url,
            order_index=entity.order_index,
            uploaded_at=entity.uploaded_at,
        )
