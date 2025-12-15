from typing import Annotated

from dependency_injector.wiring import inject, Provide
from fastapi.params import Depends

from src.application.use_cases.film_trailer.create_film_trailer_usecase import (
    CreateFilmTrailerUseCase,
)
from src.application.use_cases.film_trailer.delete_film_trailer_usecase import (
    DeleteFilmTrailerUseCase,
)
from src.application.use_cases.film_trailer.get_film_trailer_usecase import (
    GetFilmTrailerUseCase,
)
from src.application.use_cases.film_trailer.update_film_trailer_usecase import (
    UpdateFilmTrailerUseCase,
)
from src.containers import AppContainer


@inject
def get_create_film_trailer_use_case(
    use_case: Annotated[
        CreateFilmTrailerUseCase,
        Depends(Provide[AppContainer.use_cases.create_film_trailer_use_case]),
    ],
) -> CreateFilmTrailerUseCase:
    """
    Dependency provider for CreateFilmTrailerUseCase.

    Returns:
        CreateFilmTrailerUseCase: Use case instance for creating film trailer relationships.
    """
    return use_case


@inject
def get_delete_film_trailer_use_case(
    use_case: Annotated[
        DeleteFilmTrailerUseCase,
        Depends(Provide[AppContainer.use_cases.delete_film_trailer_use_case]),
    ],
) -> DeleteFilmTrailerUseCase:
    """
    Dependency provider for DeleteFilmTrailerUseCase.

    Returns:
        DeleteFilmTrailerUseCase: Use case instance for deleting film trailer relationships.
    """
    return use_case


@inject
def get_get_film_trailer_use_case(
    use_case: Annotated[
        GetFilmTrailerUseCase,
        Depends(Provide[AppContainer.use_cases.get_film_trailer_use_case]),
    ],
) -> GetFilmTrailerUseCase:
    """
    Dependency provider for GetFilmTrailerUseCase.

    Returns:
        GetFilmTrailerUseCase: Use case instance for retrieving film trailer relationships.
    """
    return use_case


@inject
def get_update_film_trailer_use_case(
    use_case: Annotated[
        UpdateFilmTrailerUseCase,
        Depends(Provide[AppContainer.use_cases.update_film_trailer_use_case]),
    ],
) -> UpdateFilmTrailerUseCase:
    """
    Dependency provider for UpdateFilmTrailerUseCase.
    Returns:
        UpdateFilmTrailerUseCase: Use case instance for updating film trailer relationships.
    """
    return use_case
