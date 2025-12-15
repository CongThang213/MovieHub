from typing import Annotated

from dependency_injector.wiring import inject, Provide
from fastapi.params import Depends

from src.application.use_cases.voucher.create_voucher_use_case import (
    CreateVoucherUseCase,
)
from src.application.use_cases.voucher.delete_voucher_use_case import (
    DeleteVoucherUseCase,
)
from src.application.use_cases.voucher.get_voucher_by_code_use_case import (
    GetVoucherByCodeUseCase,
)
from src.application.use_cases.voucher.get_voucher_use_case import GetVoucherUseCase
from src.application.use_cases.voucher.get_vouchers_use_case import GetVouchersUseCase
from src.application.use_cases.voucher.update_voucher_use_case import (
    UpdateVoucherUseCase,
)
from src.application.use_cases.voucher.validate_voucher_use_case import (
    ValidateVoucherUseCase,
)
from src.containers import AppContainer


@inject
def get_create_voucher_use_case(
    use_case: Annotated[
        CreateVoucherUseCase,
        Depends(Provide[AppContainer.use_cases.create_voucher_use_case]),
    ],
):
    """
    Dependency function that provides a CreateVoucherUseCase instance with injected dependencies.

    Args:
        use_case: The use case instance with injected repository dependencies
    Returns:
        CreateVoucherUseCase: An instance of the CreateVoucherUseCase with injected repository dependencies
    """
    return use_case


@inject
def get_get_voucher_use_case(
    use_case: Annotated[
        GetVoucherUseCase,
        Depends(Provide[AppContainer.use_cases.get_voucher_use_case]),
    ],
):
    """
    Dependency function that provides a GetVoucherUseCase instance with injected dependencies.

    Args:
        use_case: The use case instance with injected repository dependencies
    Returns:
        GetVoucherUseCase: An instance of the GetVoucherUseCase with injected repository dependencies
    """
    return use_case


@inject
def get_get_voucher_by_code_use_case(
    use_case: Annotated[
        GetVoucherByCodeUseCase,
        Depends(Provide[AppContainer.use_cases.get_voucher_by_code_use_case]),
    ],
):
    """
    Dependency function that provides a GetVoucherByCodeUseCase instance with injected dependencies.

    Args:
        use_case: The use case instance with injected repository dependencies
    Returns:
        GetVoucherByCodeUseCase: An instance of the GetVoucherByCodeUseCase with injected repository dependencies
    """
    return use_case


@inject
def get_get_vouchers_use_case(
    use_case: Annotated[
        GetVouchersUseCase,
        Depends(Provide[AppContainer.use_cases.get_vouchers_use_case]),
    ],
):
    """
    Dependency function that provides a GetVouchersUseCase instance with injected dependencies.

    Args:
        use_case: The use case instance with injected repository dependencies
    Returns:
        GetVouchersUseCase: An instance of the GetVouchersUseCase with injected repository dependencies
    """
    return use_case


@inject
def get_delete_voucher_use_case(
    use_case: Annotated[
        DeleteVoucherUseCase,
        Depends(Provide[AppContainer.use_cases.delete_voucher_use_case]),
    ],
):
    """
    Dependency function that provides a DeleteVoucherUseCase instance with injected dependencies.

    Args:
        use_case: The use case instance with injected repository dependencies
    Returns:
        DeleteVoucherUseCase: An instance of the DeleteVoucherUseCase with injected repository dependencies
    """
    return use_case


@inject
def get_update_voucher_use_case(
    use_case: Annotated[
        UpdateVoucherUseCase,
        Depends(Provide[AppContainer.use_cases.update_voucher_use_case]),
    ],
):
    """
    Dependency function that provides a UpdateVoucherUseCase instance with injected dependencies.

    Args:
        use_case: The use case instance with injected repository dependencies
    Returns:
        UpdateVoucherUseCase: An instance of the UpdateVoucherUseCase with injected repository dependencies
    """
    return use_case


@inject
def get_validate_voucher_use_case(
    use_case: Annotated[
        ValidateVoucherUseCase,
        Depends(Provide[AppContainer.use_cases.validate_voucher_use_case]),
    ],
):
    """
    Dependency function that provides a ValidateVoucherUseCase instance with injected dependencies.

    Args:
        use_case: The use case instance with injected repository dependencies
    Returns:
        ValidateVoucherUseCase: An instance of the ValidateVoucherUseCase with injected repository dependencies
    """
    return use_case
