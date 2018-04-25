from selenium.webdriver.common.by import By
from modules.pages.base_page import BasePage
from modules.config import Config
from modules.forms.message import Message


# 3. Podsumowanie
class SummaryPage(BasePage):
    url = f"{Config.MEDIA_MARKT_BASE_URL}koszyk/podsumowanie"

    ACCEPT_AND_PAY_BTN = (By.ID, "js-summation_submit")
    LOADER = (By.XPATH, "//div[contains(@class,'load ')]")
    ORDER_DESCRIPTION = (By.CSS_SELECTOR, "p[class='title seller-orderdescription'")

    def accept_and_pay_btn(self):
        self.driver.wait_for_element_and_click(self.ACCEPT_AND_PAY_BTN)
        self.driver.set_current_action(Message.SUMMARY_GET_ORDER_ID.value)
        # wait until all redirections
        order = self.driver.wait_and_get_element(self.ORDER_DESCRIPTION, 90)
        self.driver.set_current_action(Message.SUMMARY_REDIRECTED.value)
        order_text = order.text
        self.driver.set_current_action(Message.SUMMARY_GET_ORDER_ID_COMPLETE.value.format(order_text))
        order_text_array = order.text.split(" ")
        return [order.text, order_text_array[-1]]

    def wait_for_loader_close(self):
        self.driver.wait_for_element_until_invisible(self.LOADER)
