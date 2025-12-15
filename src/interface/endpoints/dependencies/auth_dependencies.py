from typing import Optional

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, Request
from fastapi.security import HTTPBearer
from pydantic import BaseModel

from src.application.exceptions.auth_exceptions import (
    TokenMissingError,
)
from src.application.use_cases.authentication.forgot_password_use_case import (
    ForgotPasswordUseCase,
)
from src.application.use_cases.authentication.sign_up_use_case import SignUpUseCase
from src.containers import AppContainer
from src.domain.enums.account_type import AccountType

# Security scheme for OpenAPI documentation
security = HTTPBearer()


class TokenData(BaseModel):
    """Data extracted from a validated authentication token"""

    user_id: str
    email: Optional[str] = None
    account_type: Optional[AccountType] = None


@inject
def get_sign_up_use_case(
    use_case: SignUpUseCase = Depends(Provide[AppContainer.use_cases.sign_up_use_case]),
) -> SignUpUseCase:
    """Dependency function to provide SignUpUseCase instance"""
    return use_case


@inject
def get_forgot_password_use_case(
    use_case: ForgotPasswordUseCase = Depends(
        Provide[AppContainer.use_cases.forgot_password_use_case]
    ),
) -> ForgotPasswordUseCase:
    """Dependency function to provide ForgotPasswordUseCase instance"""
    return use_case


def get_current_user(request: Request) -> TokenData:
    """
    Extract user data that was set by the authentication middleware.

    This function serves two purposes:
        1. Extract user data from request.state (set by middleware)
        2. Tell FastAPI that this endpoint requires authentication (for docs)

    The actual authentication is handled by AuthenticationMiddleware,
    but this dependency makes the docs show the authentication requirement.

    Args:
        request: The FastAPI request object

    Returns:
        TokenData: The user information extracted from the validated token

    Note:
        The token parameter is only used for OpenAPI documentation.
        The actual authentication and token validation is done by the middleware.
    """
    # Check if middleware has set the user data
    if not hasattr(request.state, "user_id"):
        raise TokenMissingError(
            "Authentication required - user data not found in request state"
        )

    return TokenData(
        user_id=request.state.user_id,
        email=getattr(request.state, "email", None),
        account_type=getattr(request.state, "account_type", AccountType.CUSTOMER),
    )
