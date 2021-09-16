import pytest
from selene import have
from sqlalchemy import desc
from opponent_app import db, UserAccount, create_app
from tests.locators.login_page_locators import LoginLocators
from tests.locators.navbar_locators import NavBarLocators
from tests.locators.registration_page_locators import RegistrationFormLocators
from tests.locators.user_account_locators import UserCardLocators


@pytest.mark.skip(reason="fixture outside the app")
def app():
    return create_app("test")


@pytest.mark.skip(reason="fixture outside the app")
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
    test_name = "Test"
    test_password = "qwerty12345"

    def registration_user(self, user):
        user.open("/").element(self.navbar_locator.btn_login).click()
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
        return self

    @pytest.mark.build_image
    def test_user_can_register(self, user, connect_db):
        self.registration_user(user)
        connect_db.execute(
            f"""select * from users_accounts a1 full join users_opponents o1 on
            (a1.id=o1.user_account_id) full join offers_opponents o2 on
            (o1.id=o2.user_opponent_id) where email='{self.test_email}';"""
        )
        connect_db.fetchall()
        assert connect_db.rownumber == 1
        connect_db.execute(
            f"delete from users_accounts where email='{self.test_email}';"
        )
        assert user.should(have.url_containing("en/register/unconfirmed"))
        assert user.element(
            self.register_form_locator.ConfirmPageLocators.account_confirm_link
        ).should(have.exact_text("Resend"))

    @pytest.mark.build_image
    def test_can_user_login(self, user, connect_db):
        self.registration_user(user)
        user.element(self.navbar_locator.btn_logout).click()
        user.element(self.navbar_locator.btn_login).click()
        user.element(self.login_locator.email_field).hover().type(
            self.test_email
        ).element(self.login_locator.password_field).hover().type(
            self.test_password
        ).element(
            self.login_locator.remember_me_checkbox
        ).hover().click().element(
            self.login_locator.submit_login
        ).click()
        connect_db.execute(
            f"delete from users_accounts where email='{self.test_email}';"
        )
        assert user.should(have.url_containing("en/register/unconfirmed"))
        assert user.element(
            self.register_form_locator.ConfirmPageLocators.account_confirm_link
        ).should(have.exact_text("Resend"))
