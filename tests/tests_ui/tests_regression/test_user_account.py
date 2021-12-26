import pytest

from tests.src.pages.account_page import AccountPage
from tests.src.steps.common_steps import CommonSteps
from tests.tests_ui.tests_regression.data_tests.data_user_account import UserAccount


@pytest.fixture
def create_opponent_post(connect_db):
    dt = UserAccount()
    user = AccountPage()
    user.finder_opponent_tab()
    user.autocomplete_opponent_form(
        dt.Opponent.phone, dt.Opponent.district,
        dt.Opponent.category, dt.Opponent.datetime_
    )
    yield user
    connect_db.execute(
        f"""delete from users_opponents where 
                opponent_date='{dt.Opponent.datetime_}';"""
    )


@pytest.fixture
def create_tournament_post(connect_db):
    dt = UserAccount()
    user = AccountPage()
    user.tournaments_tab()
    user.autocomplete_tournaments_form(
        dt.Tournament.title, dt.Tournament.phone,
        dt.Tournament.district, dt.Tournament.quantity_member,
        dt.Tournament.category, dt.Tournament.datetime_
    )
    yield user
    connect_db.execute(
        f'''delete from members where user_member_id in 
               (select "id" from users_members 
               where users_members.member_date='{dt.Tournament.datetime_}');'''
    )


@pytest.mark.usefixtures('login')
class TestUserAccount:

    dt = UserAccount()
    st = CommonSteps()

    def test_finder_opponent_post(self, create_opponent_post):
        create_opponent_post.text_is_displayed(self.dt.Opponent.exp_res)
        self.st.verify_endpoint(self.dt.Opponent.endpoint)

    def test_tournaments_post(self, create_tournament_post):
        create_tournament_post.text_is_displayed(self.dt.Tournament.exp_res)
        self.st.verify_endpoint(self.dt.Tournament.endpoint)




