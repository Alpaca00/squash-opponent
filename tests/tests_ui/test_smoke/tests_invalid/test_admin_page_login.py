import os
import pytest
from selene import be
from tests.locators.dashboard_locators import AdminNavBarLocators, AdminLoginPageLocators


USERNAME = os.environ['USERNAME_ADMIN']
PASSWORD = os.environ['PASSWORD_ADMIN']


class TestAdminPanel:
    login_page_locator = AdminLoginPageLocators()
    navbar_locator = AdminNavBarLocators()

    @pytest.mark.admin
    def test_can_admin_login(self, user):
        user.open("/admin/login").element(self.login_page_locator.username)\
            .type(USERNAME)\
            .element(self.login_page_locator.password).type(PASSWORD)\
            .element(self.login_page_locator.remember).click()\
            .element(self.login_page_locator.btn_login).click()\
            .should(
            be.not_.title("403 Forbidden")
        )
