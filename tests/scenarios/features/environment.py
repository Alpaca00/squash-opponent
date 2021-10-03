from behave import fixture, use_fixture
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


@fixture
def browser_chrome(context):
    options = webdriver.ChromeOptions()
    mode = context.config.userdata.get("hidden", "headless")
    if mode is not None:
        options.add_argument("--headless")
    options.add_argument("--maximized")
    context.browser = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    yield context.browser
    context.browser.quit()


def before_tag(context, tag):
    if tag == "fixture.browser.chrome":
        use_fixture(browser_chrome, context)


