from typing import Annotated

from dependency_injector.wiring import inject, Provide
from fastapi.params import Depends

from src.application.use_cases.film_cast.create_film_cast_use_case import (
    CreateFilmCastUseCase,
)
from src.application.use_cases.film_cast.delete_film_cast_use_case import (
    DeleteFilmCastUseCase,
)
from src.application.use_cases.film_cast.get_film_cast_use_case import (
    GetFilmCastUseCase,
)
from src.application.use_cases.film_cast.update_film_cast_use_case import (
    UpdateFilmCastUseCase,
)
from src.containers import AppContainer


@inject
def get_create_film_cast_use_case(
    use_case: Annotated[
        CreateFilmCastUseCase,
        Depends(Provide[AppContainer.use_cases.create_film_cast_use_case]),
    ],
) -> CreateFilmCastUseCase:
    """
    Dependency provider for CreateFilmCastUseCase.

    Returns:
        CreateFilmCastUseCase: Use case instance for creating film-cast relationships.
    """
    return use_case


@inject
def get_delete_film_cast_use_case(
    use_case: Annotated[
        DeleteFilmCastUseCase,
        Depends(Provide[AppContainer.use_cases.delete_film_cast_use_case]),
    ],
) -> DeleteFilmCastUseCase:
    """
    Dependency provider for DeleteFilmCastUseCase.

    Returns:
        DeleteFilmCastUseCase: Use case instance for deleting film-cast relationships.
    """
    return use_case


@inject
def get_get_film_cast_use_case(
    use_case: Annotated[
        GetFilmCastUseCase,
        Depends(Provide[AppContainer.use_cases.get_film_cast_use_case]),
    ],
) -> GetFilmCastUseCase:
    """
    Dependency provider for GetFilmCastUseCase.

    Returns:
        GetFilmCastUseCase: Use case instance for retrieving film-cast relationships.
    """
    return use_case


@inject
def get_update_film_cast_use_case(
    use_case: Annotated[
        UpdateFilmCastUseCase,
        Depends(Provide[AppContainer.use_cases.update_film_cast_use_case]),
    ],
) -> UpdateFilmCastUseCase:
    """
    Dependency provider for UpdateFilmCastUseCase.

    Returns:
        UpdateFilmCastUseCase: Use case instance for updating film-cast relationships.
    """
    return use_case
