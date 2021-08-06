import pytest
from selene.api import Browser, Config
from selene.support.shared import config
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


def pytest_addoption(parser):
    parser.addoption(
        "--maximized", "-M", action="store_true", help="Maximize size windows"
    )
    parser.addoption("--headless", "-H", action="store_true", help="Run headless")
    parser.addoption(
        "--browser",
        "-B",
        action="store",
        default="chrome",
        help="Browser chrome or firefox",
    )
    parser.addoption("--remote", "-R", action="store", help="Remote connect")
    parser.addoption(
        "--url",
        "-U",
        action="store",
        default="http://localhost:5000",
        help="Base url",
    )


@pytest.fixture
def user(request):
    global browser
    config_param = {
        "browser": request.config.getoption("--browser"),
        "headless": request.config.getoption("--headless"),
        "maximized": request.config.getoption("--maximized"),
        "url": request.config.getoption("--url"),
        "remote": request.config.getoption("--remote"),
    }
    if config_param["remote"]:
        browser = Browser(
            Config(
                driver=webdriver.Remote(
                    command_executor="http://{}/wd/hub".format(config_param["remote"]),
                    desired_capabilities={"browserName": config_param["browser"]},
                ),
                base_url="http://localhost:5000",
                timeout=3,
            )
        )
        config.driver = browser
    else:
        if config_param["browser"] == "chrome":
            options = webdriver.ChromeOptions()
            if config_param["headless"]:
                options.add_argument("--headless")
            if config_param["maximized"]:
                options.add_argument("--maximized")
            browser = Browser(
                Config(
                    driver=webdriver.Chrome(
                        executable_path=ChromeDriverManager().install(), options=options
                    ),
                    base_url="http://127.0.0.1:5000",
                    timeout=3,
                )
            )
    yield browser
    browser.quit()
