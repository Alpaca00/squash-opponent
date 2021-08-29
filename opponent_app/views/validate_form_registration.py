import re
from pydantic import BaseModel, validator


class ValidationFormError(Exception):
    pass


class ValidateForm(BaseModel):
    email: str
    name: str
    password: str

    @validator("email")
    def email_must_contain_the_At_character(cls, value):
        REGEX_EMAIL = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if re.findall(REGEX_EMAIL, value):
            return True
        else:
            raise ValidationFormError("Invalid email.")

    @validator("name")
    def name_must_not_contain_numeric_and_space(cls, value):
        if " " * 3 in value or not value.isalnum():
            raise ValidationFormError("The name must contain alphabets-numbers.")
        return True

    @validator("password")
    def password_must_contain_more_than_7_characters(cls, value):
        if len(value) <= 8:
            raise ValidationFormError(
                "The password must contain more than 8 characters."
            )
        return True
