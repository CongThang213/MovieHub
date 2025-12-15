import re
from typing import Optional

from src.domain.enums.account_type import AccountType

# Define role-based access control (RBAC) structure
# Maps roles to resources and their allowed actions
RESOURCES_FOR_ROLES = {
    AccountType.ADMIN.value: {
        "users": ["read", "write", "update", "delete"],
        "bookings": ["read", "write", "update", "delete"],
        "cinemas": ["read", "write", "update", "delete"],
        "films": ["read", "write", "update", "delete"],
        "casts": ["read", "write", "update", "delete"],
        "showtimes": ["read", "write", "update", "delete"],
        "payments": ["read", "write", "update", "delete"],
        "reviews": ["read", "write", "update", "delete"],
        "admin": ["read", "write", "update", "delete"],
        "genres": ["read", "write", "update", "delete"],
        "film_formats": ["read", "write", "update", "delete"],
        "banners": ["read", "write", "update", "delete"],
    },
    AccountType.CUSTOMER.value: {
        "users": ["read", "update"],
        "bookings": ["read", "write"],
        "cinemas": ["read"],
        "showtimes": ["read"],
        "payments": ["read", "write"],
        "reviews": ["read", "write", "update"],
        "films": ["read"],
        "casts": ["read"],
        "banners": ["read"],
    },
}

# Define path-to-resource mapping
# Maps URL path patterns to resource names
PATH_TO_RESOURCE_MAPPING = {
    r"^/users/.*": "users",
    r"^/bookings/.*": "bookings",
    r"^/cinemas/.*": "cinemas",
    r"^/films/.*": "films",
    r"^/showtimes/.*": "showtimes",
    r"^/payments/.*": "payments",
    r"^/reviews/.*": "reviews",
    r"^/admin/.*": "admin",
    r"^/genres/.*": "genres",
    r"^/film-formats/.*": "film_formats",
    r"^/banners/.*": "banners",
}

# Define routes that DON'T require authentication
# This is the single source of truth for public routes
PUBLIC_ROUTES = [
    r"^/$",
    r"^/docs.*",
    r"^/redoc.*",
    r"^/openapi\.json$",
    r"^/health.*",
    r"^/auth/sign-up$",
    r"^/auth/forgot-password$",
    r"^/payment/vnpay/return.*",  # VNPay user return callback (public)
    r"^/payment/IPN.*",            # VNPay IPN webhook (public, server-to-server, uppercase)
]

# Define routes that are public ONLY for GET requests (read-only access)
# Other methods (POST, PUT, DELETE) require authentication
PUBLIC_GET_ONLY_ROUTES = [
    r"^/films/?$",  # List all films
    r"^/films/search.*",  # Search films
    r"^/films/[^/]+$",  # View specific film details
    r"^/genres/?$",  # List all genres
    r"^/genres/[^/]+$",  # View specific genre details
    r"^/casts/?$",  # List all cast members
    r"^/casts/[^/]+$",  # View specific cast details
    r"^/film-formats/?$",  # List all film formats
    r"^/film-formats/[^/]+$",  # View specific film format details
    r"^/showtimes/?$",  # List all showtimes
    r"^/showtimes/[^/]+$",  # View specific showtime details
    r"^/showtimes/film/[^/]+$",  # Get showtimes by film
    r"^/showtimes/hall/[^/]+$",  # Get showtimes by hall
    r"^/showtimes/cinema/[^/]+$",  # Get showtimes by cinema
    r"^/showtimes/search/date-range.*",  # Search showtimes by date range
    r"^/film-reviews/?$",  # List all film reviews
    r"^/film-reviews/film/[^/]+$",  # Get reviews for a specific film
    r"^/film-reviews/[^/]+$",  # View specific review details
    r"^/banners/?$",  # List all active banners (for hero section)
    r"^/banners/[^/]+$",  # View specific banner details
    # Public endpoint for activating payment methods (read-only)
    r"^/payment-methods/active.*",
]


def translate_method_to_action(method: str) -> str:
    """
    Map HTTP request methods to RBAC actions.

    Args:
        method: HTTP method (GET, POST, PUT, DELETE, etc.)

    Returns:
        str: The corresponding RBAC action
    """
    method_permission_mapping = {
        "GET": "read",
        "POST": "write",
        "PUT": "update",
        "PATCH": "update",
        "DELETE": "delete",
    }
    return method_permission_mapping.get(method.upper(), "read")


def get_resource_from_path(path: str) -> Optional[str]:
    """
    Extract resource name from URL path using the mapping.

    Args:
        path: The request URL path

    Returns:
        Optional[str]: The resource name if found, None otherwise
    """
    for pattern, resource in PATH_TO_RESOURCE_MAPPING.items():
        if re.match(pattern, path):
            return resource
    return None


def has_permission(
    user_role: str, resource_name: str, required_permission: str
) -> bool:
    """
    Check if a user role has the required permission for a resource.

    Args:
        user_role: The user's role (e.g., 'admin', 'customer')
        resource_name: The name of the resource being accessed
        required_permission: The permission required (e.g., 'read', 'write')

    Returns:
        bool: True if permission is granted, False otherwise
    """
    if (
        user_role in RESOURCES_FOR_ROLES
        and resource_name in RESOURCES_FOR_ROLES[user_role]
    ):
        return required_permission in RESOURCES_FOR_ROLES[user_role][resource_name]
    return False


def is_public_route(path: str, method: str = "GET") -> bool:
    """
    Check if a route is public (doesn't require authentication).

    This is the centralized function to determine if a path should bypass authentication.
    Some routes are always public (any method), while others are public only for GET requests.

    Args:
        path: The request URL path
        method: The HTTP method (defaults to GET)

    Returns:
        bool: True if the route is public, False otherwise
    """
    # Check if route is always public (any method)
    if any(re.match(pattern, path) for pattern in PUBLIC_ROUTES):
        return True

    # Check if route is public only for GET requests
    if method.upper() == "GET":
        return any(re.match(pattern, path) for pattern in PUBLIC_GET_ONLY_ROUTES)

    return False
