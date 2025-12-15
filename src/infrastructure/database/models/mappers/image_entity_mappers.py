from src.domain.models.image import Image
from src.infrastructure.database.models.image_entity import ImageEntity


class ImageEntityMappers:
    @staticmethod
    def from_model(image: Image) -> ImageEntity:
        return ImageEntity(
            id=image.id,
            owner_id=image.owner_id,
            type=image.type,
            public_id=image.public_id,
            is_temp=image.is_temp,
            created_at=image.created_at,
        )

    @staticmethod
    def to_model(image_entity: ImageEntity) -> Image:
        return Image(
            id=image_entity.id,
            owner_id=image_entity.owner_id,
            type=image_entity.type,
            public_id=image_entity.public_id,
            is_temp=image_entity.is_temp,
            created_at=image_entity.created_at,
        )

    @staticmethod
    def to_models(image_entities: list[ImageEntity]) -> list[Image]:
        return [ImageEntityMappers.to_model(entity) for entity in image_entities]
