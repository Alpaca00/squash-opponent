import functools
from collections.abc import Callable

from tests.src import BasePage


class Button(BasePage):
    def __init__(self, locator: str) -> None:
        super().__init__()
        self.locator = (
            f"//input[contains(@value, '{locator}')] |"
            f"//a[contains(text(), '{locator}')] |"
            f"//button[contains(text(), '{locator}')] "
        )

    def click(self) -> None:
        self.element(self.locator).click()


class ActionButton:
    def __init__(self, button_name: str) -> None:
        self.el = Button(button_name)

    @property
    def action(self) -> None:
        self.el.click()


def action(button_name) -> Callable:

    def decorator(func) -> Callable:
        @functools.wraps(func)
        def wrap_arguments(*args, **kwargs) -> ActionButton.action:
            func(*args, **kwargs)
            return ActionButton(button_name).action
        return wrap_arguments

    return decorator


def before_action(button_name) -> Callable:

    def decorator(func) -> Callable:
        @functools.wraps(func)
        def wrap_arguments(*args, **kwargs) -> Callable:
            def local_wrap() -> ActionButton.action:
                return ActionButton(button_name).action
            func(*args, **kwargs)
            return local_wrap
        return wrap_arguments

    return decorator