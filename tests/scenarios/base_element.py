from typing import Any
from selenium.common.exceptions import (
    NoSuchElementException,
    ElementNotVisibleException,
    InvalidSelectorException,
)
from selenium.webdriver.remote.webelement import WebElement

x: Any = tuple or list or dict


class BaseElement:
    def __init__(self, driver, base_url):
        self.driver = driver
        self.base_url = base_url

    def _open_url(self):
        self.driver.get(self.base_url)
        return self

    def _get_element(
        self,
        selector: x,
        index_for_tuple: int = 0,
        index_for_list: int = None,
        type_query: str = None,
    ) -> WebElement:
        try:
            if isinstance(selector, tuple):
                return self.driver.find_elements(*selector)[index_for_tuple]
            if isinstance(selector, list):
                if index_for_list is not None:
                    elem = selector[index_for_list]
                    return self.driver.find_elements(*elem)[index_for_tuple]
            if isinstance(selector, dict):
                if type_query is not None:
                    elem = selector[type_query]
                    return self.driver.find_elements(*elem)[index_for_tuple]
        except NoSuchElementException:
            return False

    def _click(self, selector, index_for_tuple: int = 0, index_for_list: int = None):
        self._get_element(selector, index_for_tuple, index_for_list).click()

    def _input(
        self, selector, value, index_for_tuple: int = 0, index_for_list: int = None
    ):
        element = self._get_element(selector, index_for_tuple, index_for_list)
        element.clear()
        element.send_keys(value)

    def _text(
        self, selector, index_for_tuple: int = 0, index_for_list: int = None
    ) -> str:
        return self._get_element(selector, index_for_tuple, index_for_list).text

    def _text_is_displayed(
        self,
        selector,
        index_for_tuple: int = 0,
        index_for_list: int = None,
        text: str = None,
    ):
        element_ = self._get_element(
            selector=selector,
            index_for_tuple=index_for_tuple,
            index_for_list=index_for_list,
        )
        text_on_display = self._text(
            selector=selector,
            index_for_tuple=index_for_tuple,
            index_for_list=index_for_list,
        )
        if text is not None:
            if text_on_display == text and element_.is_displayed():
                return True
            else:
                raise (
                    ElementNotVisibleException(),
                    InvalidSelectorException(),
                )
