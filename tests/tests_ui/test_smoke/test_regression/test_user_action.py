import pytest
from selene import query
from sqlalchemy import desc
from opponent_app import db, UserAccount, create_app
from tests.locators.login_page_locators import LoginLocators
from tests.locators.navbar_locators import NavBarLocators
from tests.locators.registration_page_locators import RegistrationFormLocators
from tests.locators.user_account_locators import UserCardLocators


@pytest.fixture
def app():
    return create_app('test')


@pytest.fixture
def clean_user_account_db(app):
    yield
    with app.app_context():
        message = UserAccount.query.order_by(desc(UserAccount.id)).first()
        db.session.delete(message)
        db.session.commit()


class TestUserAction:
    navbar_locator = NavBarLocators()
    login_locator = LoginLocators()
    register_form_locator = RegistrationFormLocators()
    user_card_locator = UserCardLocators()
    test_email = "test@gmail.com"
    test_name = "Rino"
    test_password = "qwerty12345"

    @pytest.mark.create_image
    def test_user_can_register(self, user):
        user.open("/").element(self.navbar_locator.Action.btn_action).click().element(
            self.navbar_locator.Action.btn_login
        ).click()
        user.element(self.login_locator.sign_up).click()
        user.element(self.register_form_locator.email_field).hover().type(
            self.test_email
        ).element(self.register_form_locator.name_field).hover().type(
            self.test_name
        ).element(
            self.register_form_locator.password_field
        ).hover().type(
            self.test_password
        ).element(
            self.register_form_locator.submit_btn
        ).click()

    @pytest.mark.create_image
    def test_can_user_login(self, user):
        user.open("/").element(self.navbar_locator.Action.btn_action).click().element(
            self.navbar_locator.Action.btn_login
        ).click()
        user.element(self.login_locator.email_field).hover().type(
            self.test_email
        ).element(self.login_locator.password_field).hover().type(
            self.test_password
        ).element(
            self.login_locator.remember_me_checkbox
        ).hover().click().element(
            self.login_locator.submit_login
        ).click()
        user_email_on_card = user.element(self.user_card_locator.email_info).get(
            query.text
        )
        assert user_email_on_card == self.test_email
