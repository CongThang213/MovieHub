from abc import abstractmethod, ABC


class PaymentGateway(ABC):
    @abstractmethod
    def createPayment(self, orderId: str, amount: float, metadata: dict) -> str:
        """
        Creates a payment for the specified order.

        Args:
            orderId (str): The unique identifier of the order.
            amount (float): The amount to be paid.
            metadata (dict): Additional information required for processing the payment.

        Returns:
            str: The redirect URL for payment.
        """
        pass

    @abstractmethod
    def verifyPayment(self, params: dict) -> bool:
        """
        Verifies the status or result of a payment.

        Args:
            params (dict): Parameters required to verify the payment, such as payment ID and status.

        Returns:
            bool: True if the payment is verified successfully, False otherwise.
        """
        pass
