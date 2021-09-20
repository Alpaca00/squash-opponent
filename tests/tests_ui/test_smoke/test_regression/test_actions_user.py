import os
import pytest
from selene import have, be, query
from selene.support.conditions import not_
from selenium.webdriver.common.keys import Keys
from sqlalchemy import desc
from opponent_app import db, UserAccount, create_app
from tests.locators.login_page_locators import LoginLocators
from tests.locators.navbar_locators import NavBarLocators
from tests.locators.registration_page_locators import RegistrationFormLocators
from tests.locators.user_account_locators import UserCardLocators
from tests.tests_ui.test_smoke.test_regression.data_generation import Cache


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
    cache_email = Cache(email=True)
    cache_password = Cache()
    navbar_locator = NavBarLocators()
    login_locator = LoginLocators()
    register_form_locator = RegistrationFormLocators()
    user_card_locator = UserCardLocators()
    test_email = "test@gmail.com"
    test_name = "Test"
    test_password = "qwerty12345"
    actual_user_email = "alpaca00tuha@gmail.com"
    USER_PASSWORD = os.environ["USER_PASSWORD"]
    phone_user = "+380677667776"
    optimal_date = "2021-09-20T18:00"
    new_phone_user_for_update = "+380630123456"
    new_district_for_update = "Zaliznychnyi"
    new_optimal_date_for_update = "2021-10-25T18:00"

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
                and opponent_date='{self.optimal_date}'
                and opponent_phone='{self.phone_user}';"""
        )
        connect_db.fetchall()
        return connect_db.rownumber == rows

    def user_publication_post(self, user):
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
        return self


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


    @pytest.mark.parametrize(
        "email, password, expected_result",
        [
            ("alpaca00tuhagmail.com", f"{USER_PASSWORD}", "Invalid email."),
            ("1234567890", f"{USER_PASSWORD}", "Invalid email."),
            ("q", f"{USER_PASSWORD}", "Invalid email."),
            ("", f"{USER_PASSWORD}", "Invalid email."),
            ("alpaca00tuha@gmailcom", f"{USER_PASSWORD}", "Invalid email."),
            ("alpaca00tuha$gmail.com", f"{USER_PASSWORD}", "Invalid email."),
            (f"{actual_user_email}", "12345", "Invalid password."),
            (f"{actual_user_email}", "qwerty", "Invalid password."),
            (f"{actual_user_email}", "~!@#$%^&*()_+|\?/.,", "Invalid password."),
            (f"{actual_user_email}", "", "Invalid password."),
            (f"{cache_email.get_more_than_255_characters}", f"{USER_PASSWORD}", "Invalid email."),
            (f"{actual_user_email}", f"{cache_password.get_more_than_255_characters}", "Invalid password."),
            ("фйцукенгшщзхїфівапроол@gmail.com", f"{cache_password.get_more_than_255_characters}", "Invalid email."),
            (f"{actual_user_email}", "йцукенгшщзхххччорс", "Invalid password."),
        ],
    )
    def test_incorrect_login(self, user, email, password, expected_result):
        if not user.config.base_url == "http://alpaca00.website/en":
            pytest.skip("Not the English version of the site.", allow_module_level=True)
        else:
            self.user_login(user, email, password)
            assert user.element(self.login_locator.flash_message).should(
                have.exact_text(expected_result)
            )

    def test_if_already_confirmed_user(self, user):
        self.user_login(
            user=user, email=self.actual_user_email, password=self.USER_PASSWORD
        )
        assert (
            user.all(self.user_card_locator.email_info[1])[0]
            .hover()
            .should(have.exact_text(self.actual_user_email))
        )
        user.element(self.navbar_locator.btn_logout).click()

    @pytest.mark.build_image
    def test_can_user_publish_a_post(self, user, connect_db):
        if not user.config.base_url == "http://alpaca00.website/en":
            pytest.skip("Not the English version of the site.", allow_module_level=True)
        else:
            self.user_login(
                user=user, email=self.actual_user_email, password=self.USER_PASSWORD
            )
            before_quantity_post = user.all(
                self.user_card_locator.History.all_delete_post_btn
            ).get(query.size)
            self.user_publication_post(user)
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

    @pytest.mark.build_image
    def test_can_user_update_a_post(self, user, connect_db):
        if not user.config.base_url == "http://alpaca00.website/en":
            pytest.skip("Not the English version of the site.", allow_module_level=True)
        else:
            self.user_login(
                user=user, email=self.actual_user_email, password=self.USER_PASSWORD
            )
            self.user_publication_post(user)
            connect_db.execute(
                f"""select o1."id" from users_accounts a1 full join users_opponents o1
                    on (a1.id=o1.user_account_id) full join offers_opponents o2
                    on (o1.id=o2.user_opponent_id)
                    where user_opponent_id is null
                    and opponent_date='{self.optimal_date}'
                    and opponent_phone='{self.phone_user}';"""
            )
            post_id = connect_db.fetchall()
            user.all(self.user_card_locator.History.all_change_post_btn)[-1].click()

            assert user.should(
                have.url_containing(f"/en/account/update/{post_id[0][0]}")
            )
            assert user.element(self.user_card_locator.phone_field).should(
                have.value(self.phone_user)
            )
            assert user.element(self.user_card_locator.location_select).should(
                have.value("Sychivskyi")
            )
            assert user.element(self.user_card_locator.category_select).should(
                have.value("PRO")
            )
            assert user.element(self.user_card_locator.date_field).should(
                have.value(self.optimal_date)
            )

            user.element(self.navbar_locator.btn_logout).click()

            connect_db.execute(
                f"delete from users_opponents where id={int(post_id[0][0])};"
            )

    @pytest.mark.build_image
    def test_user_update_a_post(self, user, connect_db):
        if not user.config.base_url == "http://alpaca00.website/en":
            pytest.skip("Not the English version of the site.", allow_module_level=True)
        else:
            self.user_login(
                user=user, email=self.actual_user_email, password=self.USER_PASSWORD
            )
            self.user_publication_post(user)
            connect_db.execute(
                f"""select o1."id" from users_accounts a1 full join users_opponents o1
                    on (a1.id=o1.user_account_id) full join offers_opponents o2
                    on (o1.id=o2.user_opponent_id)
                    where user_opponent_id is null
                    and opponent_date='{self.optimal_date}'
                    and opponent_phone='{self.phone_user}';"""
            )
            post_id = connect_db.fetchall()
            user.all(self.user_card_locator.History.all_change_post_btn)[-1].click()
            user.all(self.user_card_locator.phone_field)[0].hover().should(
                not_.blank
            ).hover().clear().type(self.new_phone_user_for_update).element(
                self.user_card_locator.location_select
            ).press_enter().type(
                Keys.ARROW_DOWN
            ).type(
                Keys.ARROW_DOWN
            ).press_enter().should(
                have.value(self.new_district_for_update)
            ).element(
                self.user_card_locator.category_select
            ).press_enter().type(
                Keys.ARROW_DOWN
            ).type(
                Keys.ARROW_DOWN
            ).press_enter().should(
                have.value("M1")
            )
            user.driver.execute_script(
                f'dateField=document.getElementById("party");dateField.value="{self.new_optimal_date_for_update}"'
            )

            assert user.element(self.user_card_locator.date_field).should(
                have.value(self.new_optimal_date_for_update)
            )

            user.element(self.user_card_locator.post_btn).click()
            connect_db.execute(
                f"""select o1."id" from users_accounts a1 full join users_opponents o1
                    on (a1.id=o1.user_account_id) full join offers_opponents o2
                    on (o1.id=o2.user_opponent_id)
                    where user_opponent_id is null
                    and opponent_date='{self.new_optimal_date_for_update}'
                    and opponent_phone='{self.new_phone_user_for_update}';"""
            )
            update_post_id = connect_db.fetchall()

            assert post_id[0][0] == update_post_id[0][0]

            district_update_info = user.all(
                self.user_card_locator.History.all_rows_opponent_post_information_district_text_at_card
            )[-1].get(query.text)
            phone_update_info = user.all(
                self.user_card_locator.History.all_rows_opponent_post_information_phone_text_at_card
            )[-1].get(query.text)
            category_update_info = user.all(
                self.user_card_locator.History.all_rows_opponent_post_information_category_text_at_card
            )[-1].get(query.text)

            assert district_update_info.split(":")[1] == self.new_district_for_update
            assert phone_update_info.split(":")[1] == self.new_phone_user_for_update
            assert category_update_info.split(":")[1] == "M1"

            user.element(self.navbar_locator.btn_logout).click()
            connect_db.execute(
                f"delete from users_opponents where id={int(update_post_id[0][0])};"
            )
