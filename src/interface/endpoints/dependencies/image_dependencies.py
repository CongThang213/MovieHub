from dependency_injector.wiring import inject, Provide
from fastapi.params import Depends

from src.application.use_cases.image.finalize_temp_image_use_case import (
    FinalizeTempImagesUseCase,
)
from src.application.use_cases.image.upload_and_associate_images_use_case import (
    UploadAndAssociateImagesUseCase,
)
from src.application.use_cases.image.upload_temp_image_use_case import (
    UploadTempImagesUseCase,
)
from src.containers import AppContainer


@inject
def get_upload_temp_images_use_case(
    use_case: UploadTempImagesUseCase = Depends(
        Provide[AppContainer.use_cases.upload_temp_images_use_case]
    ),
) -> UploadTempImagesUseCase:
    """Dependency function that provides an UploadTempImageUseCase instance with injected dependencies."""
    return use_case


@inject
def get_finalize_temp_images_use_case(
    use_case: FinalizeTempImagesUseCase = Depends(
        Provide[AppContainer.use_cases.finalize_temp_images_use_case]
    ),
) -> FinalizeTempImagesUseCase:
    """Dependency function that provides an FinalizeTempImageUseCase instance with injected dependencies."""
    return use_case


@inject
def get_upload_and_associate_images_use_case(
    use_case: UploadAndAssociateImagesUseCase = Depends(
        Provide[AppContainer.use_cases.upload_and_associate_images_use_case]
    ),
) -> UploadAndAssociateImagesUseCase:
    """Dependency function that provides an UploadAndAssociateImagesUseCase instance with injected dependencies."""
    return use_case
