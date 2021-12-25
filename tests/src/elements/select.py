from selene import have

from tests.src import BasePage


class SelectList(BasePage):
    def __init__(self, name=None):
        super().__init__()
        loc = f'//select[@name="{name}"]'
        self._element = self.element(loc)

    def open(self):
        self._element.click()
        return self

    def _options(self):
        return self._element.all('option')

    def select_by_value(self, value):
        self._options().element_by(have.value(value)).click()
        return self

    def select_by_text(self, text):
        self._options().element_by(have.text(text)).click()
        return self

    def select_by_exact_text(self, text):
        self._options().element_by(have.exact_text(text)).click()
        return self

    def set(self, value):
        self.open()
        self.select_by_value(value)
        return self