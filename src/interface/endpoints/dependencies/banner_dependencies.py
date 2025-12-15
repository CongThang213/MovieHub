from typing import Annotated

from dependency_injector.wiring import inject, Provide
from fastapi.params import Depends

from src.application.use_cases.banner.create_banner_use_case import (
    CreateBannerUseCase,
)
from src.application.use_cases.banner.get_active_banners_use_case import (
    GetActiveBannersUseCase,
)
from src.application.use_cases.banner.get_banner_use_case import GetBannerUseCase
from src.application.use_cases.banner.update_banner_use_case import (
    UpdateBannerUseCase,
)
from src.application.use_cases.banner.delete_banner_use_case import (
    DeleteBannerUseCase,
)
from src.containers import AppContainer


@inject
def get_active_banners_use_case(
    use_case: Annotated[
        GetActiveBannersUseCase,
        Depends(Provide[AppContainer.use_cases.get_active_banners_use_case]),
    ],
) -> GetActiveBannersUseCase:
    """
    Dependency provider for GetActiveBannersUseCase.

    Returns:
        GetActiveBannersUseCase: Use case instance for retrieving active banners.
    """
    return use_case


@inject
def get_create_banner_use_case(
    use_case: Annotated[
        CreateBannerUseCase,
        Depends(Provide[AppContainer.use_cases.create_banner_use_case]),
    ],
) -> CreateBannerUseCase:
    """
    Dependency provider for CreateBannerUseCase.

    Returns:
        CreateBannerUseCase: Use case instance for creating banners.
    """
    return use_case


@inject
def get_banner_use_case(
    use_case: Annotated[
        GetBannerUseCase,
        Depends(Provide[AppContainer.use_cases.get_banner_use_case]),
    ],
) -> GetBannerUseCase:
    """
    Dependency provider for GetBannerUseCase.

    Returns:
        GetBannerUseCase: Use case instance for retrieving a banner by ID.
    """
    return use_case


@inject
def get_update_banner_use_case(
    use_case: Annotated[
        UpdateBannerUseCase,
        Depends(Provide[AppContainer.use_cases.update_banner_use_case]),
    ],
) -> UpdateBannerUseCase:
    """
    Dependency provider for UpdateBannerUseCase.

    Returns:
        UpdateBannerUseCase: Use case instance for updating banners.
    """
    return use_case


@inject
def get_delete_banner_use_case(
    use_case: Annotated[
        DeleteBannerUseCase,
        Depends(Provide[AppContainer.use_cases.delete_banner_use_case]),
    ],
) -> DeleteBannerUseCase:
    """
    Dependency provider for DeleteBannerUseCase.

    Returns:
        DeleteBannerUseCase: Use case instance for deleting banners.
    """
    return use_case
