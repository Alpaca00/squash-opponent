from datetime import datetime
import re
from typing import final

from opponent_app.public_api.helpers.error_codes import ErrorCode


class Validator:
    """Class for validation."""

    phone_pattern: final = "^(?=.{13,13}$)[\+]380\d{9}"
    date_pattern: final = r"^(?:(?:31(\/|-|\.)(?:0?[13578]|1[02]))\1|(?:(?:29|30)(\/|-|\.)(?:0?[13-9]|1[0-2])\2))(?:(?:1[6-9]|[2-9]\d)?\d{2})$|^(?:29(\/|-|\.)0?2\3(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579][26])|(?:(?:16|[2468][048]|[3579][26])00))))$|^(?:0?[1-9]|1\d|2[0-8])(\/|-|\.)(?:(?:0?[1-9])|(?:1[0-2]))\4(?:(?:1[6-9]|[2-9]\d)?\d{2})$"
    email_pattern: final = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    time_pattern: final = "/^(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$/"

    @classmethod
    def validate_phone_value(cls, value: str) -> bool:
        """Method for validating phone number."""
        return bool(re.match(cls.phone_pattern, f'+{value}'))

    @classmethod
    def validate_date_value(cls, value: str):
        """Method for validating date."""
        if bool(re.match(cls.date_pattern, value)) and len(value) == 10:
            parse_date = datetime.strptime(value, '%d-%m-%Y').strftime(
                '%Y-%m-%d'
            )
            return parse_date
        else:
            return

    @staticmethod
    def response_error(data):
        """Method for creating a dictionary with an error code."""
        return ErrorCode.parameter_wrong_format(data)

    @classmethod
    def validate_create_data_publication(cls, data) -> bool:
        """Method for validating data for creating a publication."""
        if not bool(re.match(cls.email_pattern, data.email)):
            cls.response_error(data.email)
        if not data.name.isalpha():
            cls.response_error(data.email)
        if not len(data.password) > 7:
            cls.response_error(data.password)
        if not bool(re.match(cls.phone_pattern, f'+{data.phone}')):
            cls.response_error(data.phone)
        if not data.city.isalpha():
            cls.response_error(data.city)
        if not data.district.isalpha():
            cls.response_error(data.district)
        if not bool(re.match(cls.date_pattern, data.date))\
                and len(data.date) == 10:
            cls.response_error(data.date)
        if not bool(re.match(cls.time_pattern, data.time_)):
            cls.response_error(data.time_)
        return True



