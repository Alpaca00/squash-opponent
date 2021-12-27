from tests.src import BasePage
from tests.src.components.offer_modal_window import NewOfferModalWindow
from tests.src.elements.button import action, before_action


class FinderPage(BasePage):
    def __init__(self):
        super().__init__()
        self.anchor_element_loc = "//div[@id='clock']"

    @action('Finder opponent')
    def finder_opponent_tab(self):
        self.finder_url()

    @action('SEND')
    @before_action('Offer', -1)
    def autocomplete_offer_form(
            self, name, email, phone, district, category, message, datetime_
    ):
        NewOfferModalWindow(name, email, phone, district, category, message, datetime_).fill_form()
        return self

    def finder_url(self):
        if not self.browser.driver.current_url.endswith('/finder/'):
            return self.browser.open(self.url + '/finder/')
