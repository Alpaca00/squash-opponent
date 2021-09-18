import os
import pytest
from selene import have, be, query
from selenium.webdriver.common.keys import Keys
from sqlalchemy import desc
from opponent_app import db, UserAccount, create_app
from tests.locators.login_page_locators import LoginLocators
from tests.locators.navbar_locators import NavBarLocators
from tests.locators.registration_page_locators import RegistrationFormLocators
from tests.locators.user_account_locators import UserCardLocators

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


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


def test_if_already_confirmed_user_selenium_example():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--maximized")
    driver = webdriver.Chrome(
        executable_path=ChromeDriverManager().install(), options=options
    )
    driver.get("http://alpaca00.website")
    driver.find_element_by_xpath("//*[@id='btn-login-unique']").click()
    driver.find_element_by_xpath("//input[@placeholder='email']").send_keys(
        "alpaca00tuha@gmail.com"
    )
    driver.find_element_by_xpath("//input[@placeholder='password']").send_keys(
        os.environ["USER_PASSWORD"]
    )
    driver.find_element_by_xpath("//input[@id='submit-user-login']").click()
    try:
        element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#user-card-email h6"))
        )
    except TimeoutException:
        return True
    finally:
        display_email = driver.find_element_by_css_selector(
                "#user-card-email h6"
        ).text
        print(display_email)
        assert display_email == "alpaca00tuha@gmail.com"


class TestUserAction:
    navbar_locator = NavBarLocators()
    login_locator = LoginLocators()
    register_form_locator = RegistrationFormLocators()
    user_card_locator = UserCardLocators()
    test_email = "test@gmail.com"
    test_name = "Test"
    test_password = "qwerty12345"
    actual_user_email = "alpaca00tuha@gmail.com"
    user_password = os.environ["USER_PASSWORD"]
    phone_user = "+380677667776"
    optimal_date = "2021-09-20T18:00"

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

    def user_login(self, user, email, password):
        user.open("/").element(self.navbar_locator.btn_login).click()
        user.element(self.login_locator.email_field).hover().type(email).element(
            self.login_locator.password_field
        ).hover().type(password).element(
            self.login_locator.remember_me_checkbox
        ).hover().click().element(
            self.login_locator.submit_login
        ).click()
        return self

    def query_result_should_have(self, connect_db, rows):
        connect_db.execute(
            f"""select * from users_accounts a1 left join users_opponents o1
                on (a1.id=o1.user_account_id) left join offers_opponents o2
                on (o1.id=o2.user_opponent_id)
                where user_opponent_id is null
                and opponent_date='{self.optimal_date}';"""
        )
        connect_db.fetchall()
        return connect_db.rownumber == rows

    @pytest.mark.build_image
    def test_user_can_register(self, user, connect_db):
        if not user.config.base_url == "http://alpaca00.website/en":
            pytest.skip("Not the English version of the site.", allow_module_level=True)
        else:
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
        if not user.config.base_url == "http://alpaca00.website/en":
            pytest.skip("Not the English version of the site.", allow_module_level=True)
        else:
            self.registration_user(user)
            user.element(self.navbar_locator.btn_logout).click()
            self.user_login(
                user=user, email=self.test_email, password=self.test_password
            )
            connect_db.execute(
                f"delete from users_accounts where email='{self.test_email}';"
            )
            assert user.should(have.url_containing("en/register/unconfirmed"))
            assert user.element(
                self.register_form_locator.ConfirmPageLocators.account_confirm_link
            ).should(have.exact_text("Resend"))

    def test_if_already_confirmed_user(self, user):
        self.user_login(user=user, email=self.actual_user_email, password=self.user_password)
        assert (
            user.all(self.user_card_locator.email_info[1])[0]
            .hover()
            .should(have.exact_text(self.actual_user_email))
        )
        user.element(self.navbar_locator.btn_logout).click()

    def test_can_user_publish_a_post(self, user, connect_db):
        if not user.config.base_url == "http://alpaca00.website/en":
            pytest.skip("Not the English version of the site.", allow_module_level=True)
        else:
            self.user_login(
                user=user, email=self.actual_user_email, password=self.user_password
            )
            before_quantity_post = user.all(
                self.user_card_locator.History.all_delete_post_btn
            ).get(query.size)
            user.all(self.user_card_locator.phone_field)[0].hover().should(
                be.blank
            ).hover().type(self.phone_user).element(
                self.user_card_locator.location_select
            ).press_enter().type(
                Keys.ARROW_DOWN
            ).press_enter().should(
                have.value("Sychivskyi")
            ).element(
                self.user_card_locator.category_select
            ).press_enter().type(
                Keys.ARROW_DOWN
            ).press_enter().should(
                have.value("PRO")
            )
            user.driver.execute_script(f'$("#party").val("{self.optimal_date}")')
            user.element(self.user_card_locator.post_btn).click()
            display = user.element(
                self.user_card_locator.DisplayAlertInfo.alert_info
            ).get(query.text)
            after_quantity_post = user.all(
                self.user_card_locator.History.all_delete_post_btn
            ).get(query.size)

            assert self.query_result_should_have(connect_db, 1)
            assert display == "Successfully. Your post has been added."
            assert before_quantity_post + 1 == after_quantity_post

            user.all(self.user_card_locator.History.all_delete_post_btn)[-1].click()
            new_info_on_display = user.element(
                self.user_card_locator.DisplayAlertInfo.alert_info
            ).get(query.text)

            assert new_info_on_display == "Successfully. Your post has been deleted."
            assert self.query_result_should_have(connect_db, 0)

            user.element(self.navbar_locator.btn_logout).click()
