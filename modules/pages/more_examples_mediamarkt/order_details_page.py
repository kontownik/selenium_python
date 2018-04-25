from selenium.webdriver.common.by import By
from modules.config import Config
from modules.pages.base_page import BasePage
from modules.forms.message import Message


class OrderDetailsPage(BasePage):
    url = f"{Config.MEDIA_MARKT_BASE_URL}profile/order/"
    page_name = "Order details"

    STATUS_STRONG = (By.XPATH, "//span[text()='Status']/following::span[1]/strong")
    DOWNLOAD_PDF_BTN = (By.XPATH, "//a[contains(.,'pobierz PDF zamówienia')]")

    def go_to_order_details(self, order_id):
        self.driver.get(self.url + str(order_id))
        return self

    def get_order_status(self):
        self.driver.set_current_action(Message.ORDER_STATUS.value)
        return self.driver.wait_and_get_element(self.STATUS_STRONG).text

    def check_if_single_order(self):
        element_array = self.driver.wait_and_get_elements(self.DOWNLOAD_PDF_BTN)
        return len(element_array)

    def get_pdf_link(self):
        self.driver.set_current_action(Message.ORDER_PDF_LINK.value)
        return self.driver.wait_and_get_element(self.DOWNLOAD_PDF_BTN).get_attribute('href')
