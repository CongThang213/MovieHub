from typing import Annotated

from fastapi import APIRouter, Depends, status

from src.application.use_cases.image.finalize_temp_image_use_case import (
    FinalizeTempImagesUseCase,
)
from src.application.use_cases.user.get_user_use_case import GetUserUseCase
from src.application.use_cases.user.update_user_use_case import UpdateUserUseCase
from src.interface.endpoints.dependencies.auth_dependencies import (
    get_current_user,
    TokenData,
)
from src.interface.endpoints.dependencies.image_dependencies import (
    get_finalize_temp_images_use_case,
)
from src.interface.endpoints.dependencies.user_dependencies import (
    get_update_user_use_case,
    get_get_user_use_case,
)
from src.interface.endpoints.schemas.mappers.user_schema_mappers import (
    UserSchemaMappers,
)
from src.interface.endpoints.schemas.user_schemas import (
    UserUpdateRequest,
    UserProfileResponse,
)

router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "/profile",
    response_model=UserProfileResponse,
    summary="Get current user's profile information",
    description="Retrieve the authenticated user's complete profile information including name, email, avatar, and other details.",
    responses={
        status.HTTP_200_OK: {
            "description": "User profile retrieved successfully",
            "model": UserProfileResponse,
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Authentication required",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "User not found",
        },
    },
)
async def get_current_user_profile(
    current_user: Annotated[TokenData, Depends(get_current_user)],
    get_user_use_case: Annotated[GetUserUseCase, Depends(get_get_user_use_case)],
) -> UserProfileResponse:
    """
    Retrieve the authenticated user's profile information.

    This endpoint returns the complete profile information for the currently
    authenticated user. The user ID is extracted from the authentication token
    by the middleware, ensuring users can only access their own profile.

    Authentication is handled automatically by the AuthenticationMiddleware.

    Args:
        current_user: The authenticated user making the request
        get_user_use_case: The use case for retrieving user information

    Returns:
        UserProfileResponse: The user's complete profile information
    """
    # Execute the get user use case with the user ID from the token
    user = await get_user_use_case.execute(user_id=current_user.user_id)

    # Convert the domain model to a response schema
    user_response = UserSchemaMappers.to_user_response(user)

    # Return the response wrapped in the profile response
    return UserProfileResponse(user=user_response)


@router.get(
    "/{user_id}",
    response_model=UserProfileResponse,
    summary="Get user profile information",
    description="Retrieve user profile information. Users can access their own profile, admins can access any profile.",
    responses={
        status.HTTP_200_OK: {
            "description": "User profile retrieved successfully",
            "model": UserProfileResponse,
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Authentication required",
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "Forbidden - can only access your own profile or admin access required",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "User not found",
        },
    },
)
async def get_user_by_id(
    user_id: str,
    current_user: Annotated[TokenData, Depends(get_current_user)],
    get_user_use_case: Annotated[GetUserUseCase, Depends(get_get_user_use_case)],
) -> UserProfileResponse:
    """
    Retrieve user profile information.

    Access control:
        - Users can access their own profile
        - Admins can access any user's profile

    The RBAC middleware handles basic resource access, while this endpoint
    implements ownership-based access control for user resources.

    Args:
        user_id: The ID of the user to retrieve
        current_user: The authenticated user making the request
        get_user_use_case: The use case for retrieving user information

    Returns:
        UserProfileResponse: The requested user's profile information

    Raises:
        InsufficientPermissionsError: If user tries to access another user's profile without admin rights
    """
    from src.application.exceptions.auth_exceptions import InsufficientPermissionsError
    from src.domain.enums.account_type import AccountType

    # Check if user is accessing their own profile or is an admin
    if (
        current_user.user_id != user_id
        and current_user.account_type != AccountType.ADMIN
    ):
        raise InsufficientPermissionsError(resource="users", action="read")

    # Execute the get user use case with the provided user ID
    user = await get_user_use_case.execute(user_id=user_id)

    # Convert the domain model to a response schema
    user_response = UserSchemaMappers.to_user_response(user)

    # Return the response wrapped in the profile response
    return UserProfileResponse(user=user_response)


@router.patch(
    "/profile",
    response_model=UserProfileResponse,
    summary="Update current user's profile information with optional image finalization",
    description="""
    Update the authenticated user's profile information with optional temporary image finalization.
    
    Request format:
    {
        "user": {
            "name": "Updated Name",
            "date_of_birth": "1990-01-01"
        },
        "image": {
            "temp_public_ids": ["temp_image_id_1", "temp_image_id_2"],
            "owner_id": null  // Will be set automatically to the current user's ID
        }
    }
    
    Workflow:
    1. Upload temporary images using POST /images/temp (optional)
    2. Update user profile with temp_public_ids from step 1
    3. Temporary images are automatically promoted to permanent and associated with the user
    """,
    responses={
        status.HTTP_200_OK: {
            "description": "User profile updated successfully",
            "model": UserProfileResponse,
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Authentication required",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "User not found",
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Validation error in request data",
        },
    },
)
async def update_current_user_profile(
    request: UserUpdateRequest,
    current_user: Annotated[TokenData, Depends(get_current_user)],
    update_user_use_case: Annotated[
        UpdateUserUseCase, Depends(get_update_user_use_case)
    ],
    finalize_image_use_case: Annotated[
        FinalizeTempImagesUseCase, Depends(get_finalize_temp_images_use_case)
    ],
) -> UserProfileResponse:
    """
    Update the authenticated user's profile information with optional temporary image finalization.

    This endpoint allows for updating specific fields of the current user's profile.
    Only the fields provided in the request will be updated; any fields
    not included will remain unchanged.

    If temp_public_ids are provided in the image object, those temporary images will be finalized
    and associated with the user. Avatar images will automatically update the
    user's avatar_image_url field.

    Args:
        request: The update request with nested user and image data
        current_user: The authenticated user making the request
        update_user_use_case: The use case for updating user information
        finalize_image_use_case: The use case for finalizing temporary images

    Returns:
        UserProfileResponse: The updated user profile
    """
    # Prepare update data from the nested user object
    update_data = request.user.model_dump(exclude_unset=True)

    # Finalize any temporary images if provided
    if request.image.temp_public_ids:
        try:
            finalized_images = await finalize_image_use_case.execute(
                temp_image_ids=request.image.temp_public_ids,
                owner_id=current_user.user_id,
            )

            # If avatar images were finalized, update the avatar_image_url in update_data
            avatar_images = [
                img for img in finalized_images if img.type.value == "avatar"
            ]
            if avatar_images:
                # Use the first avatar image URL
                update_data["avatar_image_url"] = avatar_images[0].url

        except Exception as e:
            # Log the error but continue with profile update
            import logging

            logging.error(
                f"Failed to finalize images during profile update for user {current_user.user_id}: {e}"
            )

    # Execute the update use case with the user ID from the token and update data
    updated_user = await update_user_use_case.execute(
        user_id=current_user.user_id, **update_data
    )

    # Convert the domain model to a response schema
    user_response = UserSchemaMappers.to_user_response(updated_user)

    # Return the response
    return UserProfileResponse(user=user_response)


@router.patch(
    "/{user_id}",
    response_model=UserProfileResponse,
    summary="Update user profile information with optional image finalization",
    description="""
    Update user profile information with optional temporary image finalization.
    Users can update their own profile, admins can update any profile.
    
    Request format same as /profile endpoint.
    """,
    responses={
        status.HTTP_200_OK: {
            "model": UserProfileResponse,
            "description": "User profile updated successfully",
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Authentication required",
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "Forbidden - can only update your own profile or admin access required",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "User not found",
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Validation error in request data",
        },
    },
)
async def update_user_profile(
    user_id: str,
    request: UserUpdateRequest,
    current_user: Annotated[TokenData, Depends(get_current_user)],
    update_user_use_case: Annotated[
        UpdateUserUseCase, Depends(get_update_user_use_case)
    ],
    finalize_image_use_case: Annotated[
        FinalizeTempImagesUseCase, Depends(get_finalize_temp_images_use_case)
    ],
) -> UserProfileResponse:
    """
    Update user profile information with optional temporary image finalization.

    Access control:
        - Users can update their own profile
        - Admins can update any user's profile

    Args:
        user_id: The ID of the user to update
        request: The update request with nested user and image data
        current_user: The authenticated user making the request
        update_user_use_case: The use case for updating user information
        finalize_image_use_case: The use case for finalizing temporary images

    Returns:
        UserProfileResponse: The updated user profile
    """
    from src.application.exceptions.auth_exceptions import InsufficientPermissionsError
    from src.domain.enums.account_type import AccountType

    # Check if user is updating their own profile or is an admin
    if (
        current_user.user_id != user_id
        and current_user.account_type != AccountType.ADMIN
    ):
        raise InsufficientPermissionsError(resource="users", action="update")

    # Prepare update data from the nested user object
    update_data = request.user.model_dump(exclude_unset=True)

    # Finalize any temporary images if provided
    if request.image.temp_public_ids:
        try:
            finalized_images = await finalize_image_use_case.execute(
                temp_image_ids=request.image.temp_public_ids, owner_id=user_id
            )

            # If avatar images were finalized, update the avatar_image_url in update_data
            avatar_images = [
                img for img in finalized_images if img.type.value == "avatar"
            ]
            if avatar_images:
                # Use the first avatar image URL
                update_data["avatar_image_url"] = avatar_images[0].url

        except Exception as e:
            # Log the error but continue with profile update
            import logging

            logging.error(
                f"Failed to finalize images during profile update for user {user_id}: {e}"
            )

    # Execute the update use case with the provided user ID and update data
    updated_user = await update_user_use_case.execute(user_id=user_id, **update_data)

    # Convert the domain model to a response schema
    user_response = UserSchemaMappers.to_user_response(updated_user)

    # Return the response
    return UserProfileResponse(user=user_response)
