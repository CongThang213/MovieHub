from typing import Annotated

from dependency_injector.wiring import inject, Provide
from fastapi.params import Depends

from src.application.use_cases.film_review.create_film_review_use_case import (
    CreateFilmReviewUseCase,
)
from src.application.use_cases.film_review.delete_film_review_use_case import (
    DeleteFilmReviewUseCase,
)
from src.application.use_cases.film_review.get_film_review_use_case import (
    GetFilmReviewUseCase,
)
from src.application.use_cases.film_review.get_film_reviews_by_film_id_use_case import (
    GetFilmReviewsByFilmIdUseCase,
)
from src.application.use_cases.film_review.get_film_reviews_use_case import (
    GetFilmReviewsUseCase,
)
from src.application.use_cases.film_review.update_film_review_use_case import (
    UpdateFilmReviewUseCase,
)
from src.containers import AppContainer


@inject
def get_create_film_review_use_case(
    use_case: Annotated[
        CreateFilmReviewUseCase,
        Depends(Provide[AppContainer.use_cases.create_film_review_use_case]),
    ],
):
    """Dependency function that provides a CreateFilmReviewUseCase instance."""
    return use_case


@inject
def get_get_film_review_use_case(
    use_case: Annotated[
        GetFilmReviewUseCase,
        Depends(Provide[AppContainer.use_cases.get_film_review_use_case]),
    ],
):
    """Dependency function that provides a GetFilmReviewUseCase instance."""
    return use_case


@inject
def get_get_film_reviews_use_case(
    use_case: Annotated[
        GetFilmReviewsUseCase,
        Depends(Provide[AppContainer.use_cases.get_film_reviews_use_case]),
    ],
):
    """Dependency function that provides a GetFilmReviewsUseCase instance."""
    return use_case


@inject
def get_get_film_reviews_by_film_id_use_case(
    use_case: Annotated[
        GetFilmReviewsByFilmIdUseCase,
        Depends(Provide[AppContainer.use_cases.get_film_reviews_by_film_id_use_case]),
    ],
):
    """Dependency function that provides a GetFilmReviewsByFilmIdUseCase instance."""
    return use_case


@inject
def get_update_film_review_use_case(
    use_case: Annotated[
        UpdateFilmReviewUseCase,
        Depends(Provide[AppContainer.use_cases.update_film_review_use_case]),
    ],
):
    """Dependency function that provides a UpdateFilmReviewUseCase instance."""
    return use_case


@inject
def get_delete_film_review_use_case(
    use_case: Annotated[
        DeleteFilmReviewUseCase,
        Depends(Provide[AppContainer.use_cases.delete_film_review_use_case]),
    ],
):
    """Dependency function that provides a DeleteFilmReviewUseCase instance."""
    return use_case
