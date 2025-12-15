from typing import Annotated

from dependency_injector.wiring import inject, Provide
from fastapi.params import Depends

from src.application.use_cases.genre.create_genre_use_case import CreateGenreUseCase
from src.application.use_cases.genre.delete_genre_use_case import DeleteGenreUseCase
from src.application.use_cases.genre.get_genre_use_case import GetGenreUseCase
from src.application.use_cases.genre.get_genres_use_case import GetGenresUseCase
from src.application.use_cases.genre.get_random_genres_use_case import (
    GetRandomGenresUseCase,
)
from src.application.use_cases.genre.update_genre_use_case import UpdateGenreUseCase
from src.containers import AppContainer


@inject
def get_create_genre_use_case(
    use_case: Annotated[
        CreateGenreUseCase,
        Depends(Provide[AppContainer.use_cases.create_genre_use_case]),
    ],
):
    """
    Dependency function that provides a CreateGenreUseCase instance with injected dependencies.

    Args:
        use_case: The use case instance with injected repository dependencies
    Returns:
        CreateGenreUseCase: An instance of the CreateGenreUseCase with injected repository dependencies
    """
    return use_case


@inject
def get_get_genre_use_case(
    use_case: Annotated[
        GetGenreUseCase,
        Depends(Provide[AppContainer.use_cases.get_genre_use_case]),
    ],
):
    """
    Dependency function that provides a GetGenreUseCase instance with injected dependencies.

    Args:
        use_case: The use case instance with injected repository dependencies
    Returns:
        GetGenreUseCase: An instance of the GetGenreUseCase with injected repository dependencies
    """
    return use_case


@inject
def get_get_genres_use_case(
    use_case: Annotated[
        GetGenresUseCase,
        Depends(Provide[AppContainer.use_cases.get_genres_use_case]),
    ],
):
    """
    Dependency function that provides a GetGenresUseCase instance with injected dependencies.

    Args:
        use_case: The use case instance with injected repository dependencies
    Returns:
        GetGenresUseCase: An instance of the GetGenresUseCase with injected repository dependencies
    """
    return use_case


@inject
def get_delete_genre_use_case(
    use_case: Annotated[
        DeleteGenreUseCase,
        Depends(Provide[AppContainer.use_cases.delete_genre_use_case]),
    ],
):
    """
    Dependency function that provides a DeleteGenreUseCase instance with injected dependencies.

    Args:
        use_case: The use case instance with injected repository dependencies
    Returns:
        DeleteGenreUseCase: An instance of the DeleteGenreUseCase with injected repository dependencies
    """
    return use_case


@inject
def get_update_genre_use_case(
    use_case: Annotated[
        UpdateGenreUseCase,
        Depends(Provide[AppContainer.use_cases.update_genre_use_case]),
    ],
):
    """
    Dependency function that provides a UpdateGenreUseCase instance with injected dependencies.

    Args:
        use_case: The use case instance with injected repository dependencies
    Returns:
        UpdateGenreUseCase: An instance of the UpdateGenreUseCase with injected repository dependencies
    """
    return use_case


@inject
def get_get_random_genres_use_case(
    use_case: Annotated[
        GetRandomGenresUseCase,
        Depends(Provide[AppContainer.use_cases.get_random_genres_use_case]),
    ],
):
    """
    Dependency function that provides a GetRandomGenresUseCase instance with injected dependencies.

    Args:
        use_case: The use case instance with injected repository dependencies
    Returns:
        GetRandomGenresUseCase: An instance of the GetRandomGenresUseCase with injected repository dependencies
    """
    return use_case
