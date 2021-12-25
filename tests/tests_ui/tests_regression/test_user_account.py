import pytest

from tests.src.pages.account_page import AccountPage
from tests.src.steps.common_steps import CommonSteps
from tests.tests_ui.tests_regression.data_tests.data_user_account import UserAccount


@pytest.mark.usefixtures('login')
class TestUserAccount:

    dt = UserAccount()

    def test_finder_opponent_post(self, connect_db):
        user = AccountPage()
        st = CommonSteps()
        db = connect_db
        user.finder_opponent_tab()
        user.autocomplete_opponent_form(
            self.dt.Opponent.phone, self.dt.Opponent.district,
            self.dt.Opponent.category, self.dt.Opponent.datetime_
        )
        user.text_is_displayed(self.dt.Opponent.exp_res)
        st.verify_endpoint(self.dt.Opponent.endpoint)

        db.execute(f"delete from users_opponents where opponent_date='{self.dt.Opponent.datetime_}'; ")