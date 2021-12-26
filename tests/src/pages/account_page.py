from tests.src import BasePage
from tests.src.components.finder_opponent_tab import FinderOpponentTab
from tests.src.components.tournaments_tab import TournamentsTab
from tests.src.elements.button import action


class AccountPage(BasePage):
    def __init__(self):
        super().__init__()
        self.anchor_element_loc = "//div[@id='page-content']"

    @action('Tournaments')
    def tournaments_tab(self):
        if not self.browser.driver.current_url.endswith('/account/'):
            self.browser.open(self.url + '/account/')
        return self

    @action('Finder opponent')
    def finder_opponent_tab(self):
        if not self.browser.driver.current_url.endswith('/account/'):
            self.browser.open(self.url + '/account/')
        return self

    @action('POST')
    def autocomplete_opponent_form(self, phone, district, category, datetime_):
        FinderOpponentTab(phone, district, category, datetime_).fill_form()
        return self

    @action('POST')
    def autocomplete_tournaments_form(self, title, phone, district, quantity_member, category, datetime_):
        TournamentsTab(title, phone, district, quantity_member, category, datetime_).fill_form()
        return self
