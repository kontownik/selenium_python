from selenium.webdriver.common.by import By
from modules.pages.base_page import BasePage
from modules.forms.message import Message


class SearchResultsPage(BasePage):
    SUBMIT_BTN = (By.NAME, "_submit")
    SEARCH_EMPTY = (By.CSS_SELECTOR, "div[class='s-search_empty']")

    def get_product_path(self, product_name):
        return (By.XPATH, f"//*[@class='m-offerBox_headline']/a[@data-offer-name='{product_name}']")

    def is_product_found(self, product_name):
        return not self.driver.check_if_element_is_visible(self.SEARCH_EMPTY)

    def choose_product(self, product_name):
        self.driver.set_current_action(Message.SEARCH_PRODUCT_PICK.value.format(product_name))
        product_path = self.get_product_path(product_name)
        self.driver.wait_for_element_and_click(product_path)
        self.driver.set_current_action(Message.SEARCH_PRODUCT_PICK_COMPLETE.value.format(product_name))
