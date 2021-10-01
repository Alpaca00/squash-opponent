from behave import given, when, then
from tests.scenarios.data_ import TEST_DATA


@given(
    'launch chrome browser and execute steps from scenario can user login, I get Given and When'
)
def launch_browser(context):
    context.execute_steps(
        """
        Given launch chrome browser
        When open home page at opponent web application of internationalization UA
    """
    )


@when('I enter valid email and invalid password "{invalid_password}"')
def incorrect_password(context, invalid_password):
    user = context.user_login._open_url()
    user._click(context.locator.navbar.btn_login)
    user._input(
        context.locator.login_page.email_field, TEST_DATA["valid"]["EMAIL"]
    )
    user._input(
        context.locator.login_page.password_field, invalid_password
    )
    user._click(context.locator.login_page.submit_login)


@then('I will see flash message about "{message}" at login page')
def flash_message(context, message):
    alert_display = context.user_login._text(context.locator.login_page.flash_message)
    assert alert_display == message
