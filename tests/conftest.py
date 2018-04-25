import pytest

from modules.helpers.webdriver_extension import WebDriver
from modules.pages.demo.login_page import LoginPage
from selenium.webdriver.common.by import By
from modules.config import Config

def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome-window-mode", help="Type in browser type")
    parser.addoption("--base_url", action="store", default=Config.BASE_URL,
                     help="Type in browser type")


@pytest.mark.hookwrapper
def pytest_runtest_makereport(item, call):
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])
    try:
        driver = item.funcargs['driver']
        if report.when == 'call':
            screenshot = driver.get_screenshot_as_base64()
            extra.append(pytest_html.extras.image(screenshot, ''))
            xfail = hasattr(report, 'wasxfail')
            if (report.skipped and xfail) or (report.failed and not xfail):
                extra.append(pytest_html.extras.html('<div>Additional HTML</div>'))
            report.extra = extra
    except:
        pass


@pytest.fixture(scope='class')
def driver(request):
    Config.BASE_URL = request.config.getoption("--base_url")
    driver = WebDriver(request.config.getoption("--browser"))
    driver.maximize_window()

    def fin():
        driver.quit()

    request.addfinalizer(fin)
    return driver


@pytest.fixture(scope='function')
def login(driver: WebDriver, request):
    login_page = LoginPage(driver)
    login_page.navigate()
    LoginPage(driver).navigate().login(request.param)
    nav_element = (By.CSS_SELECTOR, "nav[class*='dashboard-navbar']")
    login_page.visibility_of_element(nav_element)
    return request.param
