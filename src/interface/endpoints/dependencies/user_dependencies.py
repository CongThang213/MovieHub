from typing import Annotated

from dependency_injector.wiring import inject, Provide
from fastapi import Depends

from src.application.use_cases.user.get_user_use_case import GetUserUseCase
from src.application.use_cases.user.update_user_use_case import UpdateUserUseCase
from src.containers import AppContainer


@inject
def get_update_user_use_case(
    use_case: Annotated[
        UpdateUserUseCase,
        Depends(Provide[AppContainer.use_cases.update_user_use_case]),
    ],
) -> UpdateUserUseCase:
    """
    Dependency function that provides an UpdateUserUseCase instance with injected dependencies.

    Args:
        use_case: The use case instance with injected repository dependencies

    Returns:
        UpdateUserUseCase: An instance of the UpdateUserUseCase with injected repository dependencies
    """
    return use_case


@inject
def get_get_user_use_case(
    use_case: Annotated[
        GetUserUseCase,
        Depends(Provide[AppContainer.use_cases.get_user_use_case]),
    ],
) -> GetUserUseCase:
    """
    Dependency function that provides a GetUserUseCase instance with injected dependencies.

    Args:
        use_case: The use case instance with injected repository dependencies

    Returns:
        GetUserUseCase: An instance of the GetUserUseCase with injected repository dependencies
    """
    return use_case
