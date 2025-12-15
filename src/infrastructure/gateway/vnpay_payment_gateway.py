import hashlib
import hmac
import urllib.parse
from datetime import datetime

from config.app_config import AppSettings
from src.domain.gateway.payment_gateway import PaymentGateway


class VNPayPaymentGateway(PaymentGateway):
    def __init__(self, config: AppSettings):
        self._version = config.vnpay.version
        self._tmnCode = config.vnpay.tmncode
        self._hashSecret = config.vnpay.hash_secret
        self._paymentUrl = config.vnpay.payment_url
        self._returnUrl = config.vnpay.return_url

    def createPayment(self, orderId: str, amount: float, metadata: dict) -> str:
        requestData = {
            "vnp_Version": self._version,
            "vnp_Command": "pay",
            "vnp_TmnCode": self._tmnCode,
            "vnp_Amount": int(amount * 100),
            "vnp_CurrCode": "VND",
            "vnp_TxnRef": orderId,
            "vnp_OrderInfo": metadata.get("orderDes", f"Payment for {orderId}"),
            "vnp_OrderType": "190001",  # Cinema Tickets code
            "vnp_Locale": "vn",
            "vnp_CreateDate": datetime.now().strftime("%Y%m%d%H%M%S"),
            "vnp_IpAddr": metadata.get("ipAddr", "127.0.0.1"),
            "vnp_ReturnUrl": self._returnUrl,
        }

        # Sort by keys and create query string
        sortedData = sorted(requestData.items())
        queryString = ""
        seq = 0
        for key, val in sortedData:
            if seq == 1:
                queryString += "&" + key + "=" + urllib.parse.quote_plus(str(val))
            else:
                seq = 1
                queryString = key + "=" + urllib.parse.quote_plus(str(val))

        hashValue = self.__hmacsha512(self._hashSecret, queryString)
        return self._paymentUrl + "?" + queryString + "&vnp_SecureHash=" + hashValue

    def verifyPayment(self, params: dict) -> bool:
        vnp_SecureHash = params["vnp_SecureHash"]

        # Remove hash params
        if "vnp_SecureHash" in params.keys():
            del params["vnp_SecureHash"]

        if "vnp_SecureHashType" in params.keys():
            del params["vnp_SecureHashType"]

        # Sort by keys and create query string
        sortedParams = sorted(params.items())
        signed_query_string = ""
        seq = 0
        for key, val in sortedParams:
            if str(key).startswith("vnp_"):
                if seq == 1:
                    signed_query_string += (
                        "&" + str(key) + "=" + urllib.parse.quote_plus(str(val))
                    )
                else:
                    seq = 1
                    signed_query_string += (
                        str(key) + "=" + urllib.parse.quote_plus(str(val))
                    )
        hashValue = self.__hmacsha512(self._hashSecret, signed_query_string)

        return vnp_SecureHash == hashValue

    @staticmethod
    def __hmacsha512(key, data):
        byteKey = key.encode("utf-8")
        byteData = data.encode("utf-8")
        return hmac.new(byteKey, byteData, hashlib.sha512).hexdigest()
