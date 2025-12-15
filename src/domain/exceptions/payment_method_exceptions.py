from src.domain.exceptions.app_exception import AppException


class PaymentMethodNotFoundException(AppException):
    def __init__(self, payment_method_id: str):
        """
        Exception raised when a payment method is not found by ID.
        :param payment_method_id: The ID of the payment method that was not found.
        """
        super().__init__(
            status_code=404,
            error_code="PAYMENT_METHOD_NOT_FOUND",
            message=f"Payment method with id {payment_method_id} not found",
            details={"payment_method_id": payment_method_id},
        )


class PaymentMethodAlreadyExistsException(AppException):
    def __init__(self, name: str):
        """
        Exception raised when a payment method with the same name already exists.
        :param name: The name of the payment method that already exists.
        """
        super().__init__(
            status_code=409,
            error_code="PAYMENT_METHOD_ALREADY_EXISTS",
            message=f"Payment method with name '{name}' already exists",
            details={"name": name},
        )
