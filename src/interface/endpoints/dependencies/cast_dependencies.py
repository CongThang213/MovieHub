from typing import Annotated

from dependency_injector.wiring import inject, Provide
from fastapi.params import Depends

from src.application.use_cases.cast.create_cast_use_case import CreateCastUseCase
from src.application.use_cases.cast.delete_cast_use_case import DeleteCastUseCase
from src.application.use_cases.cast.get_cast_use_case import GetCastUseCase
from src.application.use_cases.cast.get_casts_use_case import GetCastsUseCase
from src.application.use_cases.cast.update_cast_use_case import UpdateCastUseCase
from src.containers import AppContainer


@inject
def get_create_cast_use_case(
    use_case: Annotated[
        CreateCastUseCase,
        Depends(Provide[AppContainer.use_cases.create_cast_use_case]),
    ],
):
    """
    Dependency function that provides a CreateCastUseCase instance with injected dependencies.

    Args:
        use_case: The use case instance with injected repository dependencies

    Returns:
        CreateCastUseCase: An instance of the CreateCastUseCase with injected repository dependencies
    """
    return use_case


@inject
def get_get_cast_use_case(
    use_case: Annotated[
        GetCastUseCase,
        Depends(Provide[AppContainer.use_cases.get_cast_use_case]),
    ],
):
    """
    Dependency function that provides a GetCastUseCase instance with injected dependencies.

    Args:
        use_case: The use case instance with injected repository dependencies

    Returns:
        GetCastUseCase: An instance of the GetCastUseCase with injected repository dependencies
    """
    return use_case


@inject
def get_get_casts_use_case(
    use_case: Annotated[
        GetCastsUseCase,
        Depends(Provide[AppContainer.use_cases.get_casts_use_case]),
    ],
):
    """
    Dependency function that provides a GetCastsUseCase instance with injected dependencies.

    Args:
        use_case: The use case instance with injected repository dependencies

    Returns:
        GetCastsUseCase: An instance of the GetCastsUseCase with injected repository dependencies
    """
    return use_case


@inject
def get_update_cast_use_case(
    use_case: Annotated[
        UpdateCastUseCase,
        Depends(Provide[AppContainer.use_cases.update_cast_use_case]),
    ],
):
    """
    Dependency function that provides a UpdateCastUseCase instance with injected dependencies.

    Args:
        use_case: The use case instance with injected repository dependencies

    Returns:
        UpdateCastUseCase: An instance of the UpdateCastUseCase with injected repository dependencies
    """
    return use_case


@inject
def get_delete_cast_use_case(
    use_case: Annotated[
        DeleteCastUseCase,
        Depends(Provide[AppContainer.use_cases.delete_cast_use_case]),
    ],
):
    """
    Dependency function that provides a DeleteCastUseCase instance with injected dependencies.

    Args:
        use_case: The use case instance with injected repository dependencies

    Returns:
        DeleteCastUseCase: An instance of the DeleteCastUseCase with injected repository dependencies
    """
    return use_case
