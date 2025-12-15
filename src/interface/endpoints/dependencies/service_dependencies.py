from typing import Annotated

from dependency_injector.wiring import inject, Provide
from fastapi.params import Depends

from src.application.use_cases.service.create_service_use_case import (
    CreateServiceUseCase,
)
from src.application.use_cases.service.delete_service_use_case import (
    DeleteServiceUseCase,
)
from src.application.use_cases.service.get_service_use_case import GetServiceUseCase
from src.application.use_cases.service.get_services_use_case import GetServicesUseCase
from src.application.use_cases.service.update_service_use_case import (
    UpdateServiceUseCase,
)
from src.containers import AppContainer


@inject
def get_create_service_use_case(
    use_case: Annotated[
        CreateServiceUseCase,
        Depends(Provide[AppContainer.use_cases.create_service_use_case]),
    ],
):
    """Dependency function that provides a CreateServiceUseCase instance."""
    return use_case


@inject
def get_get_service_use_case(
    use_case: Annotated[
        GetServiceUseCase,
        Depends(Provide[AppContainer.use_cases.get_service_use_case]),
    ],
):
    """Dependency function that provides a GetServiceUseCase instance."""
    return use_case


@inject
def get_get_services_use_case(
    use_case: Annotated[
        GetServicesUseCase,
        Depends(Provide[AppContainer.use_cases.get_services_use_case]),
    ],
):
    """Dependency function that provides a GetServicesUseCase instance."""
    return use_case


@inject
def get_update_service_use_case(
    use_case: Annotated[
        UpdateServiceUseCase,
        Depends(Provide[AppContainer.use_cases.update_service_use_case]),
    ],
):
    """Dependency function that provides an UpdateServiceUseCase instance."""
    return use_case


@inject
def get_delete_service_use_case(
    use_case: Annotated[
        DeleteServiceUseCase,
        Depends(Provide[AppContainer.use_cases.delete_service_use_case]),
    ],
):
    """Dependency function that provides a DeleteServiceUseCase instance."""
    return use_case
