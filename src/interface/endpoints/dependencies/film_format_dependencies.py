from typing import Annotated

from dependency_injector.wiring import inject, Provide
from fastapi.params import Depends

from src.application.use_cases.film_format.create_film_format_use_case import (
    CreateFilmFormatUseCase,
)
from src.application.use_cases.film_format.delete_film_format_use_case import (
    DeleteFilmFormatUseCase,
)
from src.application.use_cases.film_format.get_film_format_use_case import (
    GetFilmFormatUseCase,
)
from src.application.use_cases.film_format.get_film_formats_use_case import (
    GetFilmFormatsUseCase,
)
from src.application.use_cases.film_format.update_film_format_use_case import (
    UpdateFilmFormatUseCase,
)
from src.containers import AppContainer


@inject
def get_create_film_format_use_case(
    use_case: Annotated[
        CreateFilmFormatUseCase,
        Depends(Provide[AppContainer.use_cases.create_film_format_use_case]),
    ],
):
    """
    Dependency function that provides a CreateFilmFormatUseCase instance with injected dependencies.

    Args:
        use_case: The use case instance with injected repository dependencies

    Returns:
        CreateFilmFormatUseCase: An instance of the CreateFilmFormatUseCase with injected repository dependencies
    """
    return use_case


@inject
def get_get_film_format_use_case(
    use_case: Annotated[
        GetFilmFormatUseCase,
        Depends(Provide[AppContainer.use_cases.get_film_format_use_case]),
    ],
):
    """
    Dependency function that provides a GetFilmFormatUseCase instance with injected dependencies.

    Args:
        use_case: The use case instance with injected repository dependencies

    Returns:
        GetFilmFormatUseCase: An instance of the GetFilmFormatUseCase with injected repository dependencies
    """
    return use_case


@inject
def get_get_film_formats_use_case(
    use_case: Annotated[
        GetFilmFormatsUseCase,
        Depends(Provide[AppContainer.use_cases.get_film_formats_use_case]),
    ],
):
    """
    Dependency function that provides a GetFilmFormatsUseCase instance with injected dependencies.

    Args:
        use_case: The use case instance with injected repository dependencies

    Returns:
        GetFilmFormatsUseCase: An instance of the GetFilmFormatsUseCase with injected repository dependencies
    """
    return use_case


@inject
def get_update_film_format_use_case(
    use_case: Annotated[
        UpdateFilmFormatUseCase,
        Depends(Provide[AppContainer.use_cases.update_film_format_use_case]),
    ],
):
    """
    Dependency function that provides a UpdateFilmFormatUseCase instance with injected dependencies.

    Args:
        use_case: The use case instance with injected repository dependencies

    Returns:
        UpdateFilmFormatUseCase: An instance of the UpdateFilmFormatUseCase with injected repository dependencies
    """
    return use_case


@inject
def get_delete_film_format_use_case(
    use_case: Annotated[
        DeleteFilmFormatUseCase,
        Depends(Provide[AppContainer.use_cases.delete_film_format_use_case]),
    ],
):
    """
    Dependency function that provides a DeleteFilmFormatUseCase instance with injected dependencies.

    Args:
        use_case: The use case instance with injected repository dependencies

    Returns:
        DeleteFilmFormatUseCase: An instance of the DeleteFilmFormatUseCase with injected repository dependencies
    """
    return use_case
