from datetime import datetime
import re
from typing import final


class Validator:

    phone_pattern: final = "^(?=.{13,13}$)[\+]380\d{9}"
    date_pattern: final = r"^(?:(?:31(\/|-|\.)(?:0?[13578]|1[02]))\1|(?:(?:29|30)(\/|-|\.)(?:0?[13-9]|1[0-2])\2))(?:(?:1[6-9]|[2-9]\d)?\d{2})$|^(?:29(\/|-|\.)0?2\3(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579][26])|(?:(?:16|[2468][048]|[3579][26])00))))$|^(?:0?[1-9]|1\d|2[0-8])(\/|-|\.)(?:(?:0?[1-9])|(?:1[0-2]))\4(?:(?:1[6-9]|[2-9]\d)?\d{2})$"

    @classmethod
    def validate_phone_value(cls, value: str) -> bool:
        return bool(re.match(cls.phone_pattern, f'+{value}'))

    @classmethod
    def validate_date_value(cls, value: str):
        if bool(re.match(cls.date_pattern, value)) and len(value) == 10:
            parse_date = datetime.strptime(value, '%d-%m-%Y').strftime(
                '%Y-%m-%d'
            )
            return parse_date
        else:
            return