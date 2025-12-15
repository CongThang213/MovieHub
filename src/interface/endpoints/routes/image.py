from typing import Optional, List

from fastapi import APIRouter, UploadFile, Form, Depends, status

from config.logging_config import logger
from src.application.use_cases.image.upload_and_associate_images_use_case import (
    UploadAndAssociateImagesUseCase,
)
from src.application.use_cases.image.upload_temp_image_use_case import (
    UploadTempImagesUseCase,
)
from src.domain.models.image import ImageType
from src.interface.endpoints.dependencies.image_dependencies import (
    get_upload_temp_images_use_case,
    get_upload_and_associate_images_use_case,
)
from src.interface.endpoints.schemas.image_schemas import (
    ImageUploadResponse,
    FailedImageUpload,
)
from src.interface.endpoints.schemas.mappers.image_schema_mappers import (
    ImageSchemaMappers,
)

router = APIRouter(prefix="/images", tags=["Images"])


@router.post(
    "/",
    response_model=ImageUploadResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Upload one or more images to storage provider and save their records",
)
async def upload_images(
    entity_id: Optional[str] = Form(None, description="The ID of the entity (owner)"),
    files: List[UploadFile] = Form(
        ..., description="The list of image files to upload"
    ),
    types: List[ImageType] = Form(
        ..., description="The list of types corresponding to each file"
    ),
    upl_temps_use_case: UploadTempImagesUseCase = Depends(
        get_upload_temp_images_use_case
    ),
    upl_and_assoc_use_case: UploadAndAssociateImagesUseCase = Depends(
        get_upload_and_associate_images_use_case
    ),
):
    """
    Upload multiple images to storage provider and save their metadata in the database.

    If entity_id is provided, images are uploaded directly to permanent storage and
    associated with the entity in one step.

    If entity_id is not provided, images are uploaded to temporary storage.
    You can later finalize them using the /finalize endpoint when you have an entity_id.

    Returns information about both successful uploads and any failures that occurred.
    """
    if len(files) != len(types):
        failed_upload = FailedImageUpload(
            type=types[0] if types else None,
            error="The number of files and types must match",
            filename="multiple files",
        )
        return ImageUploadResponse(images=[], failed=[failed_upload])

    # Convert each UploadFile to bytes and pair with its type and filename
    paired_images = []
    for i, file in enumerate(files):
        try:
            content = await file.read()
            paired_images.append((content, types[i], file.filename))
        except Exception as e:
            logger.error(f"Failed to read file {file.filename}: {str(e)}")
            return ImageUploadResponse(
                images=[],
                failed=[
                    FailedImageUpload(
                        type=types[i],
                        error=f"Failed to read file with name {file.filename}",
                        filename=file.filename,
                    )
                ],
            )

    if not entity_id:
        # Upload as temporary images
        result = await upl_temps_use_case.execute(paired_images)

        # Convert the successful images to response format
        successful_images = [
            ImageSchemaMappers.to_image_response(image) for image in result.successful
        ]

        # Convert the failed uploads to response format
        failed_uploads = [
            FailedImageUpload(
                type=failed["type"], error=failed["error"], filename=failed["filename"]
            )
            for failed in result.failed
        ]

        return ImageUploadResponse(images=successful_images, failed=failed_uploads)
    else:
        # Upload and associate directly with entity
        result = await upl_and_assoc_use_case.execute(paired_images, owner_id=entity_id)

        # Convert the successful images to response format
        successful_images = [
            ImageSchemaMappers.to_image_response(image) for image in result.successful
        ]

        # Convert the failed uploads to response format
        failed_uploads = [
            FailedImageUpload(
                type=failed["type"], error=failed["error"], filename=failed["filename"]
            )
            for failed in result.failed
        ]

        return ImageUploadResponse(images=successful_images, failed=failed_uploads)
