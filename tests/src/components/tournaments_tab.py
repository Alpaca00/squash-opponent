from tests.src import BasePage
from tests.src.elements.select import SelectList
from tests.src.validator_error import ValidatorPhoneMixin


class TournamentsTab(BasePage):
    def __init__(
            self, title: str, phone: str, district: str,
            quantity_member: str, category: str, datetime_: str
    ):
        super().__init__()
        self.title = title
        self.phone = phone
        self.district = district
        self.quantity_member = quantity_member
        self.category = category
        self.datetime_ = datetime_
        self.select = SelectList

    def fill_form(self) -> None:
        if ValidatorPhoneMixin().check_phone(self.phone):
            self.set_value('title', self.title)
            self.set_value('phone', self.phone)
            self.select(name='district').select_by_text(self.district)
            self.set_value('quantity', self.quantity_member)
            self.select(name='category').select_by_text(self.category)
            self.set_datetime(self.datetime_)
