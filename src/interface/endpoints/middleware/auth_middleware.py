from typing import Callable, Optional

from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.security import HTTPBearer
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from config.logging_config import logger
from src.application.exceptions.auth_exceptions import (
    TokenMissingError,
    InsufficientPermissionsError,
    AuthenticationError,
)
from src.application.services.auth_service import AuthService
from src.domain.enums.account_type import AccountType
from src.interface.endpoints.middleware.rbac_config import (
    has_permission,
    translate_method_to_action,
    get_resource_from_path,
    is_public_route,
)
from src.utilities.common_utilities import to_exception_response


async def _extract_token(request: Request) -> Optional[str]:
    """Extract Bearer token from request headers."""
    authorization = request.headers.get("Authorization")
    if not authorization:
        return None

    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        return None

    return parts[1]


class AuthMiddleware(BaseHTTPMiddleware):
    """
    Middleware that automatically handles authentication and RBAC for protected routes.

    This middleware implements role-based access control (RBAC) to determine if users
    have the required permissions to access specific resources and perform specific actions.

    Uses centralized exception conversion for consistent error responses.
    """

    def __init__(self, app: FastAPI, auth_service: AuthService):
        super().__init__(app)
        self._auth_service = auth_service
        self._security = HTTPBearer(auto_error=False)

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Main middleware logic that runs on every request.
        Implements authentication and RBAC permission checking.
        """
        path = request.url.path
        method = request.method

        # Skip authentication for public routes (centrally defined in RBAC config)
        if is_public_route(path):
            return await call_next(request)

        # Extract and validate token for protected routes
        try:
            token = await _extract_token(request)
            if not token:
                return to_exception_response(
                    TokenMissingError("Authentication token is required")
                )

            # Validate token and get user info
            user_data = await self._validate_token(token)

            # Extract user role and other info
            user_role = user_data.get("account_type", AccountType.CUSTOMER)
            user_id = user_data["user_id"]

            # Add user data to request state for endpoints to access
            request.state.user_id = user_id
            request.state.email = user_data.get("email")
            request.state.account_type = user_role

            # Perform RBAC permission check
            if not self._check_rbac_permission(path, method, user_role):
                logger.warning(
                    f"Access denied for user {user_id} to {method} {path} - insufficient permissions"
                )

                # Extract resource and action for better error context
                resource_name = get_resource_from_path(path)
                required_action = translate_method_to_action(method)

                return to_exception_response(
                    InsufficientPermissionsError(
                        resource=resource_name, action=required_action
                    )
                )

            logger.debug(
                f"Authenticated request for user {user_id} ({user_role.value}) to {method} {path}"
            )

        except AuthenticationError as e:
            logger.warning(
                f"Auth middleware exception: {e.error_code} - {e.message} (Path: {path})"
            )
            return to_exception_response(e)
        except HTTPException as e:
            return JSONResponse(
                status_code=e.status_code,
                content={
                    "error_code": "HTTP_EXCEPTION",
                    "message": str(e.detail),
                    "details": None,
                },
            )
        except Exception as e:
            logger.error(f"Unexpected authentication middleware error: {str(e)}")
            return to_exception_response(AuthenticationError("Authentication failed"))

        # Proceed to the endpoint
        return await call_next(request)

    # noinspection PyMethodMayBeStatic
    def _check_rbac_permission(
        self, path: str, method: str, user_role: AccountType
    ) -> bool:
        """
        Check if the user has permission to access the resource with the given HTTP method.

        Args:
            path: The request URL path
            method: The HTTP method (GET, POST, PUT, DELETE, etc.)
            user_role: The user's account type/role

        Returns:
            bool: True if access is granted, False otherwise
        """
        # Get the resource name from the path
        resource_name = get_resource_from_path(path)
        if not resource_name:
            # If we can't map the path to a resource, allow access
            # (This handles edge cases or unmapped routes)
            logger.debug(f"No resource mapping found for path: {path}, allowing access")
            return True

        # Convert HTTP method to RBAC action
        required_action = translate_method_to_action(method)

        # Check if the user role has permission for this resource and action
        return has_permission(user_role.value, resource_name, required_action)

    async def _validate_token(self, token: str) -> dict:
        """Validate token using the auth service and return user data."""
        try:
            # Use the auth service to validate the token
            decoded_token = await self._auth_service.validate_token(token)

            user_id = decoded_token.get("uid")
            email = decoded_token.get("email")

            if not user_id:
                raise AuthenticationError("User ID not found in token")

            # Extract account type from custom claims
            # (Firebase puts custom claims at root level)
            account_type_str = decoded_token.get("account_type")
            try:
                account_type = (
                    AccountType(account_type_str)
                    if account_type_str
                    else AccountType.CUSTOMER
                )
            except ValueError:
                account_type = AccountType.CUSTOMER

            return {"user_id": user_id, "email": email, "account_type": account_type}

        except AuthenticationError:
            raise
        except Exception as e:
            logger.error(f"Token validation failed: {str(e)}")
            raise AuthenticationError(f"Invalid authentication credentials: {str(e)}")
