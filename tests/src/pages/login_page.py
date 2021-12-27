from tests.src.elements.button import action
from tests.src.steps.common_steps import CommonSteps


class LoginPage(CommonSteps):
    def __init__(self):
        super().__init__()
        self.anchor_element_loc = "//*[@id='sign-up-unique']"

    @action("Login")
    def login(self, email: str, pw: str):
        self.open_url("/login").is_visible(chain=True)\
            .set_value("email", email).set_value("password", pw)\
            .checkbox(label='Remember Me', enable=False)
        return self

    def page_is_visible(self, text: str):
        self.text_is_displayed(text)

    @action("Sign Up")
    def sign_page(self):
        self.login_url('/register/')
        return self

    @action("Forgot your password?")
    def recovery_password_page(self):
        self.login_url('/recovery-password/')
        return self

    def login_url(self, path: str):
        if not self.browser.driver.current_url.endswith(path):
            self.browser.open(self.url + '/login/')


class SignPage(LoginPage):
    def __init__(self):
        super().__init__()
        self.anchor_element_loc = "//*[@id='name-id']"

    @action("SUBMIT")
    def sign_up(self, email: str, name: str, pw: str) -> None:
        if not self.browser.driver.current_url.endswith('/register/'):
            self.browser.open(self.url + '/register/')
        self.set_value('email', email).set_value('name', name).set_value('password', pw)


class RecoveryPasswordPage(LoginPage):
    def __init__(self):
        super().__init__()
        self.anchor_element_loc = "//*[@id='email-id']"

    @action("SUBMIT")
    def recovery_password(self, email: str) -> None:
        if not self.browser.driver.current_url.endswith('/recovery-password/'):
            self.browser.open(self.url + '/recovery-password/')
        self.set_value('email', email)