from typing import Annotated

from dependency_injector.wiring import inject, Provide
from fastapi.params import Depends

from src.application.use_cases.payment_method.create_payment_method_use_case import (
    CreatePaymentMethodUseCase,
)
from src.application.use_cases.payment_method.delete_payment_method_use_case import (
    DeletePaymentMethodUseCase,
)
from src.application.use_cases.payment_method.get_active_payment_methods_use_case import (
    GetActivePaymentMethodsUseCase,
)
from src.application.use_cases.payment_method.get_payment_method_use_case import (
    GetPaymentMethodUseCase,
)
from src.application.use_cases.payment_method.get_payment_methods_use_case import (
    GetPaymentMethodsUseCase,
)
from src.application.use_cases.payment_method.update_payment_method_use_case import (
    UpdatePaymentMethodUseCase,
)
from src.containers import AppContainer


@inject
def get_create_payment_method_use_case(
    use_case: Annotated[
        CreatePaymentMethodUseCase,
        Depends(Provide[AppContainer.use_cases.create_payment_method_use_case]),
    ],
):
    """Dependency function that provides a CreatePaymentMethodUseCase instance."""
    return use_case


@inject
def get_payment_method_use_case(
    use_case: Annotated[
        GetPaymentMethodUseCase,
        Depends(Provide[AppContainer.use_cases.get_payment_method_use_case]),
    ],
):
    """Dependency function that provides a GetPaymentMethodUseCase instance."""
    return use_case


@inject
def get_payment_methods_use_case(
    use_case: Annotated[
        GetPaymentMethodsUseCase,
        Depends(Provide[AppContainer.use_cases.get_payment_methods_use_case]),
    ],
):
    """Dependency function that provides a GetPaymentMethodsUseCase instance."""
    return use_case


@inject
def get_active_payment_methods_use_case(
    use_case: Annotated[
        GetActivePaymentMethodsUseCase,
        Depends(Provide[AppContainer.use_cases.get_active_payment_methods_use_case]),
    ],
):
    """Dependency function that provides a GetActivePaymentMethodsUseCase instance."""
    return use_case


@inject
def get_update_payment_method_use_case(
    use_case: Annotated[
        UpdatePaymentMethodUseCase,
        Depends(Provide[AppContainer.use_cases.update_payment_method_use_case]),
    ],
):
    """Dependency function that provides an UpdatePaymentMethodUseCase instance."""
    return use_case


@inject
def get_delete_payment_method_use_case(
    use_case: Annotated[
        DeletePaymentMethodUseCase,
        Depends(Provide[AppContainer.use_cases.delete_payment_method_use_case]),
    ],
):
    """Dependency function that provides a DeletePaymentMethodUseCase instance."""
    return use_case
