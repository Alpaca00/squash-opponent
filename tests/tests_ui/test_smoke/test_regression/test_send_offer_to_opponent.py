import pytest
from selene import have, be, query
from selenium.webdriver.common.keys import Keys

from tests.locators.navbar_locators import NavBarLocators
from tests.locators.finder_opponent_locators import FinderOpponentLocators


class TestFinderOpponent:
    navbar_locator = NavBarLocators()
    finder_opponent_locator = FinderOpponentLocators()

    @pytest.mark.build_image
    def test_click_on_finder_opponent(self, user):
        user.open("/").element(self.navbar_locator.btn_finder_opponent).hover().should(
            have.exact_text("FINDER-OPPONENT")
        )
        user.open("/").element(self.navbar_locator.btn_finder_opponent).click()
        assert user.driver.title == "Finder-opponent"

    @pytest.mark.build_image
    def test_send_offer_if_opponents_are_waiting_for_confirmation(self, user):
        user.open("/finder").all(self.finder_opponent_locator.btns_offer)[0].click()
        user.element(self.finder_opponent_locator.alert_info_for_opponent).should(be.not_.visible)

        user.element(
                self.finder_opponent_locator.OfferModalWindow.name_field
            ).should(be.blank.and_(have.attribute("name").value("user_name"))).type(
                "Test"
            ).element(
                self.finder_opponent_locator.OfferModalWindow.email_field
            ).should(
                be.blank.and_(have.attribute("name").value("user_email"))
            ).type(
                "test@gemail.com"
            ).element(
                self.finder_opponent_locator.OfferModalWindow.phone_field
            ).should(
                be.blank.and_(have.attribute("name").value("user_phone"))
            ).type(
                "+380677272675"
            ).element(
                self.finder_opponent_locator.OfferModalWindow.location_select
            ).press_enter().type(
                Keys.ARROW_DOWN
            ).type(
                Keys.ARROW_DOWN
            ).press_enter().element(
                self.finder_opponent_locator.OfferModalWindow.category_select
            ).press_enter().type(
                Keys.ARROW_DOWN
            ).type(
                Keys.ARROW_DOWN
            ).press_enter().should(
                have.value("M1")
            ).element(
                self.finder_opponent_locator.OfferModalWindow.message_text
            ).should(
                be.blank.and_(have.attribute(name="placeholder", value="short message"))
            ).type(
                "I'm coming for you"
            ).should(
                have.value("I'm coming for you")
            )
        user.driver.execute_script(
                f'dateField=document.getElementById("party");dateField.value="2021-09-20T18:00"'
            )
        user.element(self.finder_opponent_locator.OfferModalWindow.send_btn).click()

        user.element(self.finder_opponent_locator.alert_info_for_opponent)\
            .should(have.exact_text("You need to wait for the answer of the opponent on the last offer."))
