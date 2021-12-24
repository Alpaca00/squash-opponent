import re
from dataclasses import dataclass
from behave import given, when, then
from tests.locators.login_page_locators import LoginLocators
from tests.locators.navbar_locators import NavBarLocators
from tests.locators.user_account_locators import UserCardLocators
from tests.scenarios import BaseElement
from tests.scenarios.data_ import TEST_DATA


@dataclass
class Locator:
    navbar: object = NavBarLocators()
    login_page: object = LoginLocators()
    user_account: object = UserCardLocators()


@given("Launch chrome browser")
def launch_browser(context):
    context.locator = Locator()
    context.user_login = BaseElement(driver=context.browser, base_url=None)


@when("Open home page at opponent web application of internationalization UA")
def open_url(context):
    url = "https://alpaca00.website/uk"
    context.user_login.base_url = url


@then("I will see the account details")
def account_details(context):
    user = context.user_login._open_url()
    lang_v = context.user_login.driver.current_url
    res = [x for x in lang_v.split("/") if re.search(x, 'uk')]
    if 'uk' not in res:
        context.scenario.skip(reason="Not the Ukrainian version of the site.")
    else:
        user._click(context.locator.navbar.btn_login)
        user._input(context.locator.login_page.email_field, TEST_DATA["valid"]["EMAIL"])
        user._input(
            context.locator.login_page.password_field, TEST_DATA["valid"]["USER_PASSWORD"]
        )
        user._click(context.locator.login_page.submit_login)
        user_will_see_the_text = user._text_is_displayed(
            selector=context.locator.user_account.email_info,
            index_for_list=0,
            text=TEST_DATA["valid"]["EMAIL"],
        )
        assert user_will_see_the_text


@then("Close browser")
def close_browser(context):
    context.user_login.driver.quit()
