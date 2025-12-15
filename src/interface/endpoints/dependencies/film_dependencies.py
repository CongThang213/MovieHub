from typing import Annotated

from dependency_injector.wiring import inject, Provide
from fastapi.params import Depends

from src.application.use_cases.film.create_film_use_case import CreateFilmUseCase
from src.application.use_cases.film.get_film_use_case import GetFilmUseCase
from src.application.use_cases.film.get_films_use_case import GetFilmsUseCase
from src.application.use_cases.film.search_films_use_case import SearchFilmsUseCase
from src.containers import AppContainer


@inject
def get_create_film_use_case(
    use_case: Annotated[
        CreateFilmUseCase,
        Depends(Provide[AppContainer.use_cases.create_film_use_case]),
    ],
) -> CreateFilmUseCase:
    """
    Dependency provider for CreateFilmUseCase.

    Returns:
        CreateFilmUseCase: Use case instance for creating films and orchestrating related entities.
    """
    return use_case


@inject
def get_get_film_use_case(
    use_case: Annotated[
        GetFilmUseCase,
        Depends(Provide[AppContainer.use_cases.get_film_use_case]),
    ],
) -> GetFilmUseCase:
    """
    Dependency provider for GetFilmUseCase.

    Returns:
        GetFilmUseCase: Use case instance for retrieving film details by ID.
    """
    return use_case


@inject
def get_get_films_use_case(
    use_case: Annotated[
        GetFilmsUseCase,
        Depends(Provide[AppContainer.use_cases.get_films_use_case]),
    ],
) -> GetFilmsUseCase:
    """
    Dependency provider for GetFilmsUseCase.

    Returns:
        GetFilmsUseCase: Use case instance for retrieving paginated list of films.
    """
    return use_case


@inject
def get_search_films_use_case(
    use_case: Annotated[
        SearchFilmsUseCase,
        Depends(Provide[AppContainer.use_cases.search_films_use_case]),
    ],
) -> SearchFilmsUseCase:
    """
    Dependency provider for SearchFilmsUseCase.

    Returns:
        SearchFilmsUseCase: Use case instance for searching films with filters.
    """
    return use_case
