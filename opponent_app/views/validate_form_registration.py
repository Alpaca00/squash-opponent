import re
from pydantic import BaseModel, validator


class ValidationFormError(Exception):
    """Validation form error."""
    pass


class ValidateForm(BaseModel):
    """Validate form."""
    email: str
    name: str
    password: str

    @validator("email")
    def email_must_contain_the_at_character(cls, value):  # noqa
        """Email must contain the @ character.

        :param value: email

        :return: True if email is valid
        """
        regex_email = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if re.findall(regex_email, value):
            return True
        else:
            raise ValidationFormError("Invalid email.")

    @validator("name")
    def name_must_not_contain_numeric_and_space(cls, value):  # noqa
        """Name must not contain numeric and space.

        :param value: name for user
        """
        if " " * 3 in value or not value.isalnum():
            raise ValidationFormError("The name must contain alphabets-numbers.")
        return True

    @validator("password")
    def password_must_contain_more_than_7_characters(cls, value):  # noqa
        """Password must contain more than 7 characters.

        :param value: password for user
        """
        if len(value) <= 8:
            raise ValidationFormError(
                "The password must contain more than 8 characters."
            )
        return True
