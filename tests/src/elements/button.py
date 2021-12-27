import functools
from collections.abc import Callable

from tests.src import BasePage


class Button(BasePage):
    def __init__(self, locator: str) -> None:
        super().__init__()
        self.locator = (
            f"//input[contains(@value, '{locator}')] |"
            f"//a[contains(text(), '{locator}')] |"
            f"//a[contains(., '{locator}')] |"
            f"//span[contains(., '{locator}')] |"
            f"//button[contains(text(), '{locator}')] "
        )

    def click(self, index=0) -> None:
        self.element(self.locator, index=index).click()


class ActionButton:
    def __init__(self, button_name: str) -> None:
        self.el = Button(button_name)

    def action(self, index=0) -> None:
        self.el.click(index=index)


def action(button_name, index=0) -> Callable:

    def decorator(func) -> Callable:
        @functools.wraps(func)
        def wrap_arguments(*args, **kwargs) -> ActionButton.action:
            func(*args, **kwargs)
            return ActionButton(button_name).action(index=index)
        return wrap_arguments

    return decorator


def before_action(button_name, index) -> Callable:

    def decorator(func) -> Callable:
        @functools.wraps(func)
        def wrap_arguments(*args, **kwargs) -> ActionButton.action:
            ActionButton(button_name).action(index=index)
            return func(*args, **kwargs)
        return wrap_arguments

    return decorator