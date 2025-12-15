from typing import Annotated

from dependency_injector.wiring import inject, Provide
from fastapi.params import Depends

from src.application.use_cases.cinema.create_cinema_use_case import (
    CreateCinemaUseCase,
)
from src.application.use_cases.cinema.delete_cinema_use_case import (
    DeleteCinemaUseCase,
)
from src.application.use_cases.cinema.get_cinema_use_case import GetCinemaUseCase
from src.application.use_cases.cinema.get_cinemas_by_city_use_case import (
    GetCinemasByCityUseCase,
)
from src.application.use_cases.cinema.get_cinemas_use_case import GetCinemasUseCase
from src.application.use_cases.cinema.update_cinema_use_case import (
    UpdateCinemaUseCase,
)
from src.containers import AppContainer


@inject
def get_create_cinema_use_case(
    use_case: Annotated[
        CreateCinemaUseCase,
        Depends(Provide[AppContainer.use_cases.create_cinema_use_case]),
    ],
):
    """
    Dependency function that provides a CreateCinemaUseCase instance with injected dependencies.

    Args:
        use_case: The use case instance with injected repository dependencies
    Returns:
        CreateCinemaUseCase: An instance of the CreateCinemaUseCase with injected repository dependencies
    """
    return use_case


@inject
def get_get_cinema_use_case(
    use_case: Annotated[
        GetCinemaUseCase,
        Depends(Provide[AppContainer.use_cases.get_cinema_use_case]),
    ],
):
    """
    Dependency function that provides a GetCinemaUseCase instance with injected dependencies.

    Args:
        use_case: The use case instance with injected repository dependencies
    Returns:
        GetCinemaUseCase: An instance of the GetCinemaUseCase with injected repository dependencies
    """
    return use_case


@inject
def get_get_cinemas_use_case(
    use_case: Annotated[
        GetCinemasUseCase,
        Depends(Provide[AppContainer.use_cases.get_cinemas_use_case]),
    ],
):
    """
    Dependency function that provides a GetCinemasUseCase instance with injected dependencies.

    Args:
        use_case: The use case instance with injected repository dependencies
    Returns:
        GetCinemasUseCase: An instance of the GetCinemasUseCase with injected repository dependencies
    """
    return use_case


@inject
def get_get_cinemas_by_city_use_case(
    use_case: Annotated[
        GetCinemasByCityUseCase,
        Depends(Provide[AppContainer.use_cases.get_cinemas_by_city_use_case]),
    ],
):
    """
    Dependency function that provides a GetCinemasByCityUseCase instance with injected dependencies.

    Args:
        use_case: The use case instance with injected repository dependencies
    Returns:
        GetCinemasByCityUseCase: An instance of the GetCinemasByCityUseCase with injected repository dependencies
    """
    return use_case


@inject
def get_delete_cinema_use_case(
    use_case: Annotated[
        DeleteCinemaUseCase,
        Depends(Provide[AppContainer.use_cases.delete_cinema_use_case]),
    ],
):
    """
    Dependency function that provides a DeleteCinemaUseCase instance with injected dependencies.

    Args:
        use_case: The use case instance with injected repository dependencies
    Returns:
        DeleteCinemaUseCase: An instance of the DeleteCinemaUseCase with injected repository dependencies
    """
    return use_case


@inject
def get_update_cinema_use_case(
    use_case: Annotated[
        UpdateCinemaUseCase,
        Depends(Provide[AppContainer.use_cases.update_cinema_use_case]),
    ],
):
    """
    Dependency function that provides a UpdateCinemaUseCase instance with injected dependencies.

    Args:
        use_case: The use case instance with injected repository dependencies
    Returns:
        UpdateCinemaUseCase: An instance of the UpdateCinemaUseCase with injected repository dependencies
    """
    return use_case
