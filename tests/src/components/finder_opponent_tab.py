from tests.src import BasePage
from tests.src.elements.select import SelectList
from tests.src.validator_error import ValidatorPhoneMixin


class FinderOpponentTab(BasePage):
    def __init__(self, phone: str, district: str, category: str, datetime_: str,):
        super().__init__()
        self.phone = phone
        self.district = district
        self.category = category
        self.datetime_ = datetime_
        self.select = SelectList

    def fill_form(self) -> None:
        if ValidatorPhoneMixin().check_phone(self.phone):
            self.set_value('phone', self.phone)
            self.select(name='district').select_by_text(self.district)
            self.select(name='category').select_by_text(self.category)
            self.set_datetime(self.datetime_)


