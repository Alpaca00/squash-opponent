import loguru
from selene import be, have, query
from selenium import webdriver
from selenium.webdriver import Chrome

from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
)
from selene.api import Browser, Config
from furl import furl
from webdriver_manager.chrome import ChromeDriverManager


options = webdriver.ChromeOptions()
options.add_argument("--headless")
driver = Browser(
    Config(
        driver=Chrome(
            executable_path=ChromeDriverManager().install(),
            options=options
        ),
        base_url="https://alpaca00.website/en",
        timeout=4,
    )
)


class BasePage:

    anchor_element_loc = None

    def __init__(self, browser=driver):
        self.browser = browser
        self.url = self.browser.config.base_url
        self.timeout = self.browser.config.timeout

    def open_url(self, path="/"):
        self.browser.open(path)
        return self

    def element(self, locator: str, index: int = 0):
        return self.browser.all(locator)[index]

    def set_value(self, name, value):
        loc = f'//input[@name="{name}"]'
        elem = self.browser.element(loc)
        if elem.matching(be.enabled):
            elem.set_value(value)
        return self

    def checkbox(self, label, enable=False):
        loc = f'//input[contains(text(), {label})]'
        elem = self.browser.element(loc)
        if elem.matching(be.visible) and enable:
            elem.click()
        return self

    def is_visible(self, chain=False):
        visible_element = self.element(self.anchor_element_loc).matching(be.visible)
        if not chain:
            assert visible_element
        else:
            if visible_element:
                return self
            else:
                raise

    def text_is_displayed(self, text: str):
        loc = (
            f'//*[contains(text(),"{text}")] |'
            f'//*[contains(.,"{text}")] '
        )
        self.element(loc).should(have.text(text))
        return self

    def extra_wait_for_visible_page(self):
        page_state = self.browser.driver.execute_script("return document.readyState;")
        exp = (NoSuchElementException, StaleElementReferenceException)
        try:
            self.browser.element(self.anchor_element_loc).wait_until(have.size_greater_than_or_equal(1))
            size = self.element(self.anchor_element_loc).get(query.size)
            if page_state == "complete" and size == 0:
                raise exp
        except exp:
            loguru.logger.info(f"Not found {self.anchor_element_loc} locator.")
            return False
        else:
            return self

    def logout(self) -> None:
        url = furl(self.url).add(path="/login/").url
        self.open_url(url)

    def __str__(self) -> str:
        return f"Path: {furl(self.url).path}.\nAnchor element locator: {self.anchor_element_loc}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}"
