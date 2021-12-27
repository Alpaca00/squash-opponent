from tests.src import BasePage
from tests.src.db import DB


class CommonSteps(BasePage):

    connect_db = DB()

    def verify_endpoint(self, path):
        assert self.browser.driver.current_url.endswith(path)

    def current_number_of_opponent_widgets(self, email: str) -> int:
        count = self.connect_db.execute_query(
            query=f"""select count(*) from users_accounts ua right join users_opponents uo
             on (ua.id=uo.user_account_id) where ua.email='{email}';"""
        )
        return count

    def current_number_of_sent_offer_to_opponent(self, email_opponent, email_offer):
        count = self.connect_db.execute_query(
            query=f"""
            select count(*) from offers_opponents where
            offers_opponents.offer_email='{email_offer}' and
             offers_opponents.user_opponent_id in
             (select id from users_opponents where users_opponents.user_account_id in
              (select id from users_accounts where email='{email_opponent}'));
            """
        )
        return count
