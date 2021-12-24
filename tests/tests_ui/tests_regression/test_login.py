import pytest
from tests.src.pages.login_page import LoginPage, SignPage, RecoveryPasswordPage
from tests.tests_ui.tests_regression.data_tests.data_login import DataLogin


class TestLogin:

    dt = DataLogin()

    @pytest.mark.regression
    def test_correct_login(self):
        user = LoginPage()
        user.login(self.dt.CorrectLogin.email, self.dt.CorrectLogin.pw)
        user.page_is_visible(self.dt.CorrectLogin.exp_result)
        user.verify_endpoint(self.dt.CorrectLogin.endpoint)

    @pytest.mark.regression
    @pytest.mark.dependency()
    def test_sign_up(self):
        user = SignPage()
        user.sign_page()
        user.sign_up(self.dt.SignUp.email, self.dt.SignUp.name, self.dt.SignUp.pw)
        user.page_is_visible(self.dt.SignUp.exp_result)
        user.verify_endpoint(self.dt.SignUp.endpoint)

    @pytest.mark.regression
    @pytest.mark.dependency(depends=["TestLogin::test_sign_up"])
    def test_recovery_password(self, connect_db):
        db = connect_db
        user = RecoveryPasswordPage()
        user.recovery_password_page()
        user.recovery_password(self.dt.RecoveryPassword.email)
        user.page_is_visible(self.dt.RecoveryPassword.exp_result)
        user.verify_endpoint(self.dt.RecoveryPassword.endpoint)

        db.execute(f"delete from users_accounts where email='{self.dt.SignUp.email}';")
        user.quit()


