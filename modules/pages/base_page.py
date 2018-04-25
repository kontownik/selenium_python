from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By


class BasePage(object):
    url = None
    page_name = "Unknown page"
    LOADER = (By.CSS_SELECTOR, "div[class*='ui-async-content__spinner']")

    def __init__(self, driver):
        self.driver = driver

    def navigate(self):
        self.driver.get(self.url)
        return self

    def click_on(self, locator):
        self.driver.wait_for_element_and_click(locator)

    def type(self, locator, text):
        self.driver.wait_for_element_and_send_text(locator, text)

    def get_text(self, locator):
        return self.driver.wait_for_element_and_get_text(locator)

    def visibility_of_element(self, locator):
        return self.driver.check_if_element_is_visible(locator)

    def compare_url(self):
        if self.driver.current_url == self.url:
            return True
        else:
            return False

    def wait_for_redirect(self, timeout=10):
        WebDriverWait(self.driver, timeout).until(lambda driver: self.driver.current_url == self.url)

    def find_element(self, *locator):
        return self.driver.find_element(*locator)

    def get_element(self, element, timeout=10):
        return self.driver.wait_and_get_element(element, timeout)

    def get_title(self):
        return self.driver.title

    def get_url(self):
        return self.driver.current_url

    def is_loaded(self, element, timeout=2):
        el = self.driver.wait_and_get_element(element, timeout)
        if el is not None:
            return True
        else:
            return False

    def wait_for_loader_to_disappear(self):
        if self.driver.fast_check_if_element_exist(self.LOADER):  # if exist?
            loader_element = self.driver.wait_and_get_element(self.LOADER)
            if loader_element.is_displayed():
                self.driver.wait_for_element_until_invisible(self.LOADER)
