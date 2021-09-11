import pytest
from selene import have, be
from tests.locators.navbar_locators import NavBarLocators
from tests.locators.finder_opponent_locators import FinderOpponentLocators


class TestFinderOpponent:
    navbar_locator = NavBarLocators()
    finder_opponent_locator = FinderOpponentLocators()

    def test_click_on_finder_opponent(self, user):
        user.open("/").element(self.navbar_locator.btn_finder_opponent).hover().should(
            have.exact_text("FINDER-OPPONENT")
        )
        user.open("/").element(self.navbar_locator.btn_finder_opponent).click()
        assert user.driver.title == "Finder-opponent"

    @pytest.mark.create_image
    def test_make_an_offer_if_already_made(self, user):
        user.open("/en/finder").all(self.finder_opponent_locator.btns_offer)[0].click()
        alert = user.config.driver.switch_to.alert
        assert alert.text == "You need to wait for the answer of the opponent on the last offer."
        alert.accept()
        assert user.all(self.finder_opponent_locator.btns_offer)[0].should(be.visible)
