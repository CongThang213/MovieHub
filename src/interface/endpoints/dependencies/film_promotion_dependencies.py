from typing import Annotated

from dependency_injector.wiring import inject, Provide
from fastapi.params import Depends

from src.application.use_cases.film_promotion.create_film_promotion_usecase import (
    CreateFilmPromotionUseCase,
)
from src.application.use_cases.film_promotion.delete_film_promotion_usecase import (
    DeleteFilmPromotionUseCase,
)
from src.application.use_cases.film_promotion.get_film_promotion_usecase import (
    GetFilmPromotionUseCase,
)
from src.application.use_cases.film_promotion.update_film_promotion_usecase import (
    UpdateFilmPromotionUseCase,
)
from src.application.use_cases.film_promotion.get_film_promotions_by_film_id_usecase import (
    GetFilmPromotionsByFilmIdUseCase,
)
from src.containers import AppContainer


@inject
def get_create_film_promotion_use_case(
    use_case: Annotated[
        CreateFilmPromotionUseCase,
        Depends(Provide[AppContainer.use_cases.create_film_promotion_use_case]),
    ],
) -> CreateFilmPromotionUseCase:
    """
    Dependency provider for CreateFilmPromotionUseCase.

    Returns:
        CreateFilmPromotionUseCase: Use case instance for creating film promotion relationships.
    """
    return use_case


@inject
def get_delete_film_promotion_use_case(
    use_case: Annotated[
        DeleteFilmPromotionUseCase,
        Depends(Provide[AppContainer.use_cases.delete_film_promotion_use_case]),
    ],
) -> DeleteFilmPromotionUseCase:
    """
    Dependency provider for DeleteFilmPromotionUseCase.

    Returns:
        DeleteFilmPromotionUseCase: Use case instance for deleting film promotion relationships.
    """
    return use_case


@inject
def get_get_film_promotion_use_case(
    use_case: Annotated[
        GetFilmPromotionUseCase,
        Depends(Provide[AppContainer.use_cases.get_film_promotion_use_case]),
    ],
) -> GetFilmPromotionUseCase:
    """
    Dependency provider for GetFilmPromotionUseCase.

    Returns:
        GetFilmPromotionUseCase: Use case instance for retrieving film promotion relationships.
    """
    return use_case


@inject
def get_update_film_promotion_use_case(
    use_case: Annotated[
        UpdateFilmPromotionUseCase,
        Depends(Provide[AppContainer.use_cases.update_film_promotion_use_case]),
    ],
) -> UpdateFilmPromotionUseCase:
    """
    Dependency provider for UpdateFilmPromotionUseCase.

    Returns:
        UpdateFilmPromotionUseCase: Use case instance for updating film promotion relationships.
    """
    return use_case


@inject
def get_get_film_promotions_by_film_id_use_case(
    use_case: Annotated[
        GetFilmPromotionsByFilmIdUseCase,
        Depends(Provide[AppContainer.use_cases.get_film_promotion_by_film_in_use_case]),
    ],
) -> GetFilmPromotionsByFilmIdUseCase:
    """
    Dependency provider for GetFilmPromotionsByFilmIdUseCase.

    Returns:
        GetFilmPromotionsByFilmIdUseCase: Use case instance for retrieving all promotions for a film.
    """
    return use_case
