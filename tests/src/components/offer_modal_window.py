from tests.src import BasePage
from tests.src.elements.select import SelectList
from tests.src.validator_error import ValidatorPhoneMixin


class NewOfferModalWindow(BasePage):
    def __init__(
            self, name: str, email: str, phone: str, district: str,
            category: str, message: str, datetime_: str
    ):
        super().__init__()
        self.name = name
        self.email = email
        self.phone = phone
        self.district = district
        self.category = category
        self.message = message
        self.datetime_ = datetime_
        self.select = SelectList

    def fill_form(self) -> None:
        if ValidatorPhoneMixin().check_phone(self.phone):
            self.set_value('user_name', self.name)
            self.set_value('user_email', self.email)
            self.set_value('user_phone', self.phone)
            self.set_value('user_message_text', self.message)
            self.select(name='user_district').select_by_text(self.district)
            self.select(name='user_category').select_by_text(self.category)
            self.set_datetime(self.datetime_)