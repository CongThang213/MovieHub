from typing import Annotated

from dependency_injector.wiring import inject, Provide
from fastapi.params import Depends

from src.application.use_cases.showtime.create_showtime_use_case import (
    CreateShowTimeUseCase,
)
from src.application.use_cases.showtime.delete_showtime_use_case import (
    DeleteShowTimeUseCase,
)
from src.application.use_cases.showtime.get_showtime_use_case import GetShowTimeUseCase
from src.application.use_cases.showtime.get_showtimes_by_cinema_use_case import (
    GetShowTimesByCinemaUseCase,
)
from src.application.use_cases.showtime.get_showtimes_by_film_use_case import (
    GetShowTimesByFilmUseCase,
)
from src.application.use_cases.showtime.get_showtimes_by_hall_use_case import (
    GetShowTimesByHallUseCase,
)
from src.application.use_cases.showtime.get_showtimes_use_case import (
    GetShowTimesUseCase,
)
from src.application.use_cases.showtime.update_showtime_use_case import (
    UpdateShowTimeUseCase,
)
from src.containers import AppContainer


@inject
def get_create_showtime_use_case(
    use_case: Annotated[
        CreateShowTimeUseCase,
        Depends(Provide[AppContainer.use_cases.create_showtime_use_case]),
    ],
):
    """Dependency function that provides a CreateShowTimeUseCase instance."""
    return use_case


@inject
def get_get_showtime_use_case(
    use_case: Annotated[
        GetShowTimeUseCase,
        Depends(Provide[AppContainer.use_cases.get_showtime_use_case]),
    ],
):
    """Dependency function that provides a GetShowTimeUseCase instance."""
    return use_case


@inject
def get_get_showtimes_use_case(
    use_case: Annotated[
        GetShowTimesUseCase,
        Depends(Provide[AppContainer.use_cases.get_showtimes_use_case]),
    ],
):
    """Dependency function that provides a GetShowTimesUseCase instance."""
    return use_case


@inject
def get_get_showtimes_by_film_use_case(
    use_case: Annotated[
        GetShowTimesByFilmUseCase,
        Depends(Provide[AppContainer.use_cases.get_showtimes_by_film_use_case]),
    ],
):
    """Dependency function that provides a GetShowTimesByFilmUseCase instance."""
    return use_case


@inject
def get_get_showtimes_by_hall_use_case(
    use_case: Annotated[
        GetShowTimesByHallUseCase,
        Depends(Provide[AppContainer.use_cases.get_showtimes_by_hall_use_case]),
    ],
):
    """Dependency function that provides a GetShowTimesByHallUseCase instance."""
    return use_case


@inject
def get_get_showtimes_by_cinema_use_case(
    use_case: Annotated[
        GetShowTimesByCinemaUseCase,
        Depends(Provide[AppContainer.use_cases.get_showtimes_by_cinema_use_case]),
    ],
):
    """Dependency function that provides a GetShowTimesByCinemaUseCase instance."""
    return use_case


@inject
def get_update_showtime_use_case(
    use_case: Annotated[
        UpdateShowTimeUseCase,
        Depends(Provide[AppContainer.use_cases.update_showtime_use_case]),
    ],
):
    """Dependency function that provides an UpdateShowTimeUseCase instance."""
    return use_case


@inject
def get_delete_showtime_use_case(
    use_case: Annotated[
        DeleteShowTimeUseCase,
        Depends(Provide[AppContainer.use_cases.delete_showtime_use_case]),
    ],
):
    """Dependency function that provides a DeleteShowTimeUseCase instance."""
    return use_case
