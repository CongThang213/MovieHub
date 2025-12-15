from typing import Annotated

from dependency_injector.wiring import inject, Provide
from fastapi.params import Depends

from src.application.use_cases.seat_category.create_seat_category_use_case import (
    CreateSeatCategoryUseCase,
)
from src.application.use_cases.seat_category.delete_seat_category_use_case import (
    DeleteSeatCategoryUseCase,
)
from src.application.use_cases.seat_category.get_seat_category_use_case import (
    GetSeatCategoryUseCase,
)
from src.application.use_cases.seat_category.get_seat_categories_use_case import (
    GetSeatCategoriesUseCase,
)
from src.application.use_cases.seat_category.update_seat_category_use_case import (
    UpdateSeatCategoryUseCase,
)
from src.containers import AppContainer


@inject
def get_create_seat_category_use_case(
    use_case: Annotated[
        CreateSeatCategoryUseCase,
        Depends(Provide[AppContainer.use_cases.create_seat_category_use_case]),
    ],
):
    """
    Dependency function that provides a CreateSeatCategoryUseCase instance with injected dependencies.

    Args:
        use_case: The use case instance with injected repository dependencies
    Returns:
        CreateSeatCategoryUseCase: An instance of the CreateSeatCategoryUseCase with injected repository dependencies
    """
    return use_case


@inject
def get_get_seat_category_use_case(
    use_case: Annotated[
        GetSeatCategoryUseCase,
        Depends(Provide[AppContainer.use_cases.get_seat_category_use_case]),
    ],
):
    """
    Dependency function that provides a GetSeatCategoryUseCase instance with injected dependencies.

    Args:
        use_case: The use case instance with injected repository dependencies
    Returns:
        GetSeatCategoryUseCase: An instance of the GetSeatCategoryUseCase with injected repository dependencies
    """
    return use_case


@inject
def get_get_seat_categories_use_case(
    use_case: Annotated[
        GetSeatCategoriesUseCase,
        Depends(Provide[AppContainer.use_cases.get_seat_categories_use_case]),
    ],
):
    """
    Dependency function that provides a GetSeatCategoriesUseCase instance with injected dependencies.

    Args:
        use_case: The use case instance with injected repository dependencies
    Returns:
        GetSeatCategoriesUseCase: An instance of the GetSeatCategoriesUseCase with injected repository dependencies
    """
    return use_case


@inject
def get_update_seat_category_use_case(
    use_case: Annotated[
        UpdateSeatCategoryUseCase,
        Depends(Provide[AppContainer.use_cases.update_seat_category_use_case]),
    ],
):
    """
    Dependency function that provides an UpdateSeatCategoryUseCase instance with injected dependencies.

    Args:
        use_case: The use case instance with injected repository dependencies
    Returns:
        UpdateSeatCategoryUseCase: An instance of the UpdateSeatCategoryUseCase with injected repository dependencies
    """
    return use_case


@inject
def get_delete_seat_category_use_case(
    use_case: Annotated[
        DeleteSeatCategoryUseCase,
        Depends(Provide[AppContainer.use_cases.delete_seat_category_use_case]),
    ],
):
    """
    Dependency function that provides a DeleteSeatCategoryUseCase instance with injected dependencies.

    Args:
        use_case: The use case instance with injected repository dependencies
    Returns:
        DeleteSeatCategoryUseCase: An instance of the DeleteSeatCategoryUseCase with injected repository dependencies
    """
    return use_case
