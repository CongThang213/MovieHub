from src.domain.models.image import Image
from src.interface.endpoints.schemas.image_schemas import ImageResponse


class ImageSchemaMappers:
    @staticmethod
    def to_image_response(image: Image) -> ImageResponse:
        return ImageResponse(type=image.type, public_id=image.public_id, url=image.url)
