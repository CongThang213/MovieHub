from dependency_injector import containers, providers

from src.infrastructure.gateway.vnpay_payment_gateway import VNPayPaymentGateway


class PaymentGatewayContainer(containers.DeclarativeContainer):
    """Container for payment gateway dependencies."""

    # This container will receive the app_container's config as a dependency
    config = providers.Dependency()

    # Create VNPay payment gateway with config
    vnpay_gateway = providers.Singleton(VNPayPaymentGateway, config=config)
