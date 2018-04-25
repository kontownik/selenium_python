from selenium.webdriver.common.by import By
from modules.pages.base_page import BasePage
from modules.config import Config
from modules.forms.message import Message


class PeoplePage(BasePage):
    url = f"{Config.BASE_URL}people"
    page_name = "People page"

