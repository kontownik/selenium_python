from selenium.webdriver.common.by import By
from modules.pages.base_page import BasePage
from modules.config import Config
from modules.forms.message import Message


class LoginPage(BasePage):
    url = f"{Config.BASE_URL}"
    page_name = "Login page"

    EMAIL_INPUT = (By.ID, "email")
    PASSWORD_INPUT = (By.ID, "password")
    SUBMIT_BTN = (By.CSS_SELECTOR, "button[type='submit']")

    def login(self, account):
        self.driver.set_current_action(Message.LOGIN.value)
        self.driver.wait_for_element_and_send_text(self.EMAIL_INPUT, account.email)
        self.driver.wait_for_element_and_send_text(self.PASSWORD_INPUT, account.password)
        self.driver.wait_for_element_and_click(self.SUBMIT_BTN)
