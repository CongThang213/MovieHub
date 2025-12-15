from typing import Annotated

from dependency_injector.wiring import inject, Provide
from fastapi.params import Depends

from src.application.use_cases.hall.create_hall_use_case import CreateHallUseCase
from src.application.use_cases.hall.delete_hall_use_case import DeleteHallUseCase
from src.application.use_cases.hall.get_hall_use_case import GetHallUseCase
from src.application.use_cases.hall.get_halls_by_cinema_use_case import (
    GetHallsByCinemaUseCase,
)
from src.application.use_cases.hall.get_halls_use_case import GetHallsUseCase
from src.application.use_cases.hall.update_hall_use_case import UpdateHallUseCase
from src.application.use_cases.hall_layout.create_hall_layout_use_case import (
    CreateHallLayoutUseCase,
)
from src.application.use_cases.hall_layout.get_hall_layout_use_case import (
    GetHallLayoutUseCase,
)
from src.application.use_cases.hall_layout.update_hall_layout_use_case import (
    UpdateHallLayoutUseCase,
)
from src.containers import AppContainer


@inject
def get_create_hall_use_case(
    use_case: Annotated[
        CreateHallUseCase,
        Depends(Provide[AppContainer.use_cases.create_hall_use_case]),
    ],
):
    """
    Dependency function that provides a CreateHallUseCase instance with injected dependencies.

    Args:
        use_case: The use case instance with injected repository dependencies
    Returns:
        CreateHallUseCase: An instance of the CreateHallUseCase with injected repository dependencies
    """
    return use_case


@inject
def get_get_hall_use_case(
    use_case: Annotated[
        GetHallUseCase,
        Depends(Provide[AppContainer.use_cases.get_hall_use_case]),
    ],
):
    """
    Dependency function that provides a GetHallUseCase instance with injected dependencies.

    Args:
        use_case: The use case instance with injected repository dependencies
    Returns:
        GetHallUseCase: An instance of the GetHallUseCase with injected repository dependencies
    """
    return use_case


@inject
def get_get_halls_use_case(
    use_case: Annotated[
        GetHallsUseCase,
        Depends(Provide[AppContainer.use_cases.get_halls_use_case]),
    ],
):
    """
    Dependency function that provides a GetHallsUseCase instance with injected dependencies.

    Args:
        use_case: The use case instance with injected repository dependencies
    Returns:
        GetHallsUseCase: An instance of the GetHallsUseCase with injected repository dependencies
    """
    return use_case


@inject
def get_get_halls_by_cinema_use_case(
    use_case: Annotated[
        GetHallsByCinemaUseCase,
        Depends(Provide[AppContainer.use_cases.get_halls_by_cinema_use_case]),
    ],
):
    """
    Dependency function that provides a GetHallsByCinemaUseCase instance with injected dependencies.

    Args:
        use_case: The use case instance with injected repository dependencies
    Returns:
        GetHallsByCinemaUseCase: An instance of the GetHallsByCinemaUseCase with injected repository dependencies
    """
    return use_case


@inject
def get_delete_hall_use_case(
    use_case: Annotated[
        DeleteHallUseCase,
        Depends(Provide[AppContainer.use_cases.delete_hall_use_case]),
    ],
):
    """
    Dependency function that provides a DeleteHallUseCase instance with injected dependencies.

    Args:
        use_case: The use case instance with injected repository dependencies
    Returns:
        DeleteHallUseCase: An instance of the DeleteHallUseCase with injected repository dependencies
    """
    return use_case


@inject
def get_update_hall_use_case(
    use_case: Annotated[
        UpdateHallUseCase,
        Depends(Provide[AppContainer.use_cases.update_hall_use_case]),
    ],
):
    """
    Dependency function that provides a UpdateHallUseCase instance with injected dependencies.

    Args:
        use_case: The use case instance with injected repository dependencies
    Returns:
        UpdateHallUseCase: An instance of the UpdateHallUseCase with injected repository dependencies
    """
    return use_case


@inject
def get_create_hall_layout_use_case(
    use_case: Annotated[
        CreateHallLayoutUseCase,
        Depends(Provide[AppContainer.use_cases.create_hall_layout_use_case]),
    ],
):
    """
    Dependency function that provides a CreateHallLayoutUseCase instance with injected dependencies.

    Args:
        use_case: The use case instance with injected repository dependencies
    Returns:
        CreateHallLayoutUseCase: An instance of the CreateHallLayoutUseCase with injected repository dependencies
    """
    return use_case


@inject
def get_update_hall_layout_use_case(
    use_case: Annotated[
        UpdateHallLayoutUseCase,
        Depends(Provide[AppContainer.use_cases.update_hall_layout_use_case]),
    ],
):
    """
    Dependency function that provides a UpdateHallLayoutUseCase instance with injected dependencies.

    Args:
        use_case: The use case instance with injected repository dependencies
    Returns:
        UpdateHallLayoutUseCase: An instance of the UpdateHallLayoutUseCase with injected repository dependencies
    """
    return use_case


@inject
def get_get_hall_layout_use_case(
    use_case: Annotated[
        GetHallLayoutUseCase,
        Depends(Provide[AppContainer.use_cases.get_hall_layout_use_case]),
    ],
):
    """
    Dependency function that provides a GetHallLayoutUseCase instance with injected dependencies.

    Args:
        use_case: The use case instance with injected repository dependencies
    Returns:
        GetHallLayoutUseCase: An instance of the GetHallLayoutUseCase with injected repository dependencies
    """
    return use_case
