from src.domain.exceptions.app_exception import AppException


class ServiceNotFoundException(AppException):
    def __init__(self, service_id: str):
        """
        Exception raised when a service is not found by ID.
        :param service_id: The ID of the service that was not found.
        """
        super().__init__(
            status_code=404,
            error_code="SERVICE_NOT_FOUND",
            message=f"Service with id {service_id} not found",
            details={"service_id": service_id},
        )


class ServiceAlreadyExistsException(AppException):
    def __init__(self, name: str):
        """
        Exception raised when a service with the same name already exists.
        :param name: The name of the service that already exists.
        """
        super().__init__(
            status_code=409,
            error_code="SERVICE_ALREADY_EXISTS",
            message=f"Service with name '{name}' already exists",
            details={"name": name},
        )
