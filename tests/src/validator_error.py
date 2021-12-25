import re

from loguru import logger


class ValidatorError:

    def __init__(self, regex):
        self.regex = regex

    def check_value(self, value) -> bool:
        if re.findall(self.regex, value):
            return True
        else:
            logger.info(value)
            raise AssertionError("Invalid phone number.")


class ValidatorPhoneMixin:

    REG_PHONE = r"^(?:\+38)?(?:\([0-9]{3}\D)[ .-]?[0-9]{3}[ .-]?[0-9]{2}[ .-]?[0-9]{2}|[0-9]{3}[ .-]?[0-9]{3}[ .-]?[0-9]{2}[ .-]?[0-9]{2}|[0-9]{3}[0-9]{7}$gm"

    def __init__(self):
        self.validate_phone = ValidatorError(self.REG_PHONE)

    def check_phone(self, value: str) -> str:
        if self.validate_phone.check_value(value):
            return value
