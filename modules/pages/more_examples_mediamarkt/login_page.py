from selenium.webdriver.common.by import By
from modules.pages.base_page import BasePage
from modules.pages.more_examples_mediamarkt.profile_page import ProfilePage
from modules.config import Config
from modules.forms.message import Message


class LoginPage(BasePage):
    url = f"{Config.MEDIA_MARKT_BASE_URL}login"
    page_name = "Login page"

    EMAIL_INPUT = (By.ID, "enp_customer_form_login_username")
    PASSWORD_INPUT = (By.ID, "enp_customer_form_login_password")
    SUBMIT_BTN = (By.CSS_SELECTOR, ".gua-login")

    def login(self, email, password):
        self.driver.set_current_action(Message.LOGIN.value)
        self.driver.wait_for_element_and_send_text(self.EMAIL_INPUT, email)
        self.driver.wait_for_element_and_send_text(self.PASSWORD_INPUT, password)
        self.driver.wait_for_element_and_click(self.SUBMIT_BTN)
        return ProfilePage(self.driver)
