from email import message
import hashlib
import hmac
from turtle import st
from typing import Union

from game.cli_menu import CliMenu


class HmacCalculator:

    @staticmethod
    def calculate(key: bytes, message: Union[str, int, bytes]) -> str:
        if isinstance(message, int):
            message = str(message).encode()
        elif isinstance(message, str):
            message = message.encode()

        hmac_obj: hmac.HMAC = hmac.new(key, message, hashlib.sha3_256)
        return hmac_obj.hexdigest().upper()

    @staticmethod
    def verify(key: bytes, message: Union[str, int, bytes], hmac_value: str) -> bool:
        calculated_hmac = HmacCalculator.calculate(key, message)
        return calculated_hmac.lower() == hmac_value.lower()

    @staticmethod
    def check_hmac(key_hex: str, message: str, shown_hmac: str, NotifyCli: bool = True) -> bool:
        key: bytes = bytes.fromhex(key_hex)
        msg: bytes = message.encode()
        hmac_obj: hmac.HMAC = hmac.new(key, msg, hashlib.sha3_256)
        calculated_hmac: str = hmac_obj.hexdigest()

        is_valid: bool = hmac.compare_digest(
            calculated_hmac.lower(), shown_hmac.lower())

        if NotifyCli:
            CliMenu.display_message(
                f"Calculated HMAC: {calculated_hmac.upper()}")
            if is_valid == True:
                CliMenu.display_message("HMAC verification succeeded")
            else:
                CliMenu.display_message("HMAC verification failed")

        return is_valid
