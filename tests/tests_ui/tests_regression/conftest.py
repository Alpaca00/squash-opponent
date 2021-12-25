import pytest

from tests.src.pages.login_page import LoginPage
from tests.tests_ui.tests_regression.data_tests.data_login import DataLogin


@pytest.fixture(scope='class')
def login():
    user = LoginPage()
    dt = DataLogin()
    user.login(dt.CorrectLogin.email, dt.CorrectLogin.pw)
    yield user
    user.quit()