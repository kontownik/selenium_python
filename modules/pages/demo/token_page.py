from selenium.webdriver.common.by import By
from modules.pages.base_page import BasePage
from modules.config import Config
from modules.forms.message import Message


class TokensPage(BasePage):
    url = f"{Config.BASE_URL}tokens"
    page_name = "Tokens page"

    TOKEN_NAME_INPUT = (By.ID, "inputToken")
    GENERATE_BUTTON = (By.XPATH, "//button[contains(text(),'Generate')]")
    DELETE_BUTTON = (By.XPATH, "//button[contains(text(),'Delete')]")
    TOKEN_TABLE_ROW = (By.XPATH, "//tbody/tr")

    def add_token(self, value):
        self.type(self.TOKEN_NAME_INPUT, value)
        self.click_on(self.GENERATE_BUTTON)
        return self

    def delete_token_by_index(self, index=0):
        self.click_on((By.XPATH, f"//tbody/tr[{index}]"))
        delete_button = self.driver.wait_and_get_element(self.DELETE_BUTTON)
        delete_button.click()
        return self




