from src.domain.exceptions.app_exception import AppException


class VoucherNotFoundException(AppException):
    def __init__(self, voucher_id: str):
        """
        Exception raised when a voucher is not found by ID.
        :param voucher_id: The ID of the voucher that was not found.
        """
        super().__init__(
            status_code=404,  # HTTP 404 Not Found
            error_code="VOUCHER_NOT_FOUND",
            message=f"Voucher with id {voucher_id} not found",
            details={"voucher_id": voucher_id},
        )


class VoucherCodeNotFoundException(AppException):
    def __init__(self, code: str):
        """
        Exception raised when a voucher is not found by code.
        :param code: The code of the voucher that was not found.
        """
        super().__init__(
            status_code=404,  # HTTP 404 Not Found
            error_code="VOUCHER_CODE_NOT_FOUND",
            message=f"Voucher with code '{code}' not found",
            details={"code": code},
        )


class VoucherInvalidException(AppException):
    def __init__(self, code: str, reason: str):
        """
        Exception raised when a voucher is invalid.
        :param code: The code of the voucher that is invalid.
        :param reason: The reason why the voucher is invalid.
        """
        super().__init__(
            status_code=400,  # HTTP 400 Bad Request
            error_code="VOUCHER_INVALID",
            message=f"Voucher with code {code} is invalid: {reason}",
            details={"code": code, "reason": reason},
        )
