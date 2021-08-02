import pytest
from app import app, db, UserAccount, desc
from doc.locators.login_page_locators import LoginLocators
from doc.locators.navbar_locators import NavBarLocators
from doc.locators.registration_page_locators import RegistrationFormLocators


@pytest.fixture
def clean_user_account_db():
    yield
    with app.app_context():
        message = UserAccount.query.order_by(desc(UserAccount.id)).first()
        db.session.delete(message)
        db.session.commit()


class TestUserAction:
    navbar_locator = NavBarLocators()
    login_locator = LoginLocators()
    register_form_locator = RegistrationFormLocators()
    test_email = "test@gmail.com"
    test_name = "Rino"
    test_password = "qwerty12345"

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
