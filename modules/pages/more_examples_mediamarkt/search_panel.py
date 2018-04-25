from selenium.webdriver.common.by import By
from modules.pages.more_examples_mediamarkt.product_page import ProductPage
from modules.pages.more_examples_mediamarkt.search_results_page import SearchResultsPage
from modules.pages.base_page import BasePage
from modules.forms.message import Message


class SearchPanel(BasePage):
    SEARCH_INPUT = (By.ID, "query_querystring")
    SUBMIT_BTN = (By.ID, "js-triggerSearch")
    QUERY_STRING = "search?query"

    def search_product_and_follow(self, product_name):
        self.driver.set_current_action(Message.SEARCH_PRODUCT.value.format(product_name))
        self.driver.wait_for_element_and_send_text(self.SEARCH_INPUT, product_name)
        self.driver.wait_for_element_and_click(self.SUBMIT_BTN)
        # are we in search page?
        if self.QUERY_STRING in self.driver.current_url:
            self.driver.set_current_action(Message.SEARCH_PRODUCT_COMPLETE.value.format(product_name))
            search_result_page = SearchResultsPage(self.driver)
            # product found?
            if search_result_page.is_product_found(product_name):
                search_result_page.choose_product(product_name)
                return ProductPage(self.driver)
            else:
                self.driver.set_current_action(Message.SEARCH_PRODUCT_NOT_FOUND.value.format(product_name), "error")
                return None
        # or we are redirected to product (100% name match is skipping search page)
        else:
            self.driver.set_current_action(Message.SEARCH_PRODUCT_REDIRECTED.value.format(product_name))
            return ProductPage(self.driver)
