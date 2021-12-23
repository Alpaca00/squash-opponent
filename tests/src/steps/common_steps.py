from tests.src import BasePage


class CommonSteps(BasePage):

    def verify_endpoint(self, path):
        assert self.browser.driver.current_url.endswith(path)