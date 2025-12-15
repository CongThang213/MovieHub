from typing import Annotated

from fastapi import APIRouter, status, Depends

from config.logging_config import logger
from src.application.use_cases.authentication.forgot_password_use_case import (
    ForgotPasswordUseCase,
)
from src.application.use_cases.authentication.sign_up_use_case import SignUpUseCase
from src.application.use_cases.image.finalize_temp_image_use_case import (
    FinalizeTempImagesUseCase,
)
from src.domain.enums.image_type import ImageType
from src.domain.exceptions.app_exception import AppException
from src.interface.endpoints.dependencies.auth_dependencies import (
    get_sign_up_use_case,
    get_forgot_password_use_case,
)
from src.interface.endpoints.dependencies.image_dependencies import (
    get_finalize_temp_images_use_case,
)
from src.interface.endpoints.schemas.auth_schemas import (
    SignUpRequest,
    PasswordResetRequest,
    PasswordResetResponse,
)
from src.interface.endpoints.schemas.mappers.auth_schema_mappers import (
    AuthSchemaMappers,
)
from src.interface.endpoints.schemas.user_schemas import UserProfileResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/sign-up",
    response_model=UserProfileResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user account with optional image finalization",
)
async def register(
    request: SignUpRequest,
    sign_up_use_case: Annotated[SignUpUseCase, Depends(get_sign_up_use_case)],
    finalize_image_use_case: Annotated[
        FinalizeTempImagesUseCase, Depends(get_finalize_temp_images_use_case)
    ],
):
    # Log the full request to debug image data
    logger.debug(f"Temp public IDs: {request.image.temp_public_ids}")

    # Create user from the nested user data
    user = AuthSchemaMappers.to_domain(request.user)
    domain_user = await sign_up_use_case.execute(
        user=user,
        password=request.user.password,
    )

    # Check if there are temp_public_ids and log for debugging
    has_temp_ids = bool(request.image and request.image.temp_public_ids)
    logger.info(
        f"Has temp image IDs: {has_temp_ids}, count: {len(request.image.temp_public_ids) if has_temp_ids else 0}"
    )

    avatar_url = None
    if has_temp_ids:
        logger.info(
            f"Finalizing images for new user {domain_user.id}: {request.image.temp_public_ids}"
        )
        finalized_images = await finalize_image_use_case.execute(
            temp_image_ids=request.image.temp_public_ids, owner_id=domain_user.id
        )
        logger.info(f"Successfully finalized {len(finalized_images)} images")

        # If avatar images were finalized, get the URL for the response
        avatar_images = [
            img for img in finalized_images if img.type == ImageType.AVATAR
        ]
        logger.info(f"Found {len(avatar_images)} avatar image")

        if avatar_images:
            avatar_url = avatar_images[0].url
            logger.info(f"Found avatar URL for user {domain_user.id}: {avatar_url}")

    # Convert domain user to response schema and wrap in envelope
    user_response = AuthSchemaMappers.to_user_response(
        domain_user, avatar_url=avatar_url
    )
    return UserProfileResponse.model_validate({"user": user_response})


@router.post(
    "/forgot-password",
    response_model=PasswordResetResponse,
    status_code=status.HTTP_200_OK,
)
async def forgot_password(
    request: PasswordResetRequest,
    forgot_password_use_case: Annotated[
        ForgotPasswordUseCase, Depends(get_forgot_password_use_case)
    ],
) -> PasswordResetResponse:
    """
    Send a password reset email to the user.

    This endpoint allows users to request a password reset email when they have forgotten
    their password. An email with a password reset link will be sent to the provided email
    address if a user with that email exists in the system.

    For security reasons, the response doesn't indicate whether the email exists in the system
    or not, but will provide appropriate feedback for any technical issues.
    """
    try:
        await forgot_password_use_case.execute(email=request.email)
        return PasswordResetResponse(
            message="If a user with this email exists, a password reset link has been sent."
        )
    except Exception as e:
        # For any other unexpected errors, wrap in an AppException
        raise AppException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_code="PASSWORD_RESET_FAILED",
            message="An error occurred while processing your request",
            details={"reason": str(e)} if isinstance(e, Exception) else None,
        )
