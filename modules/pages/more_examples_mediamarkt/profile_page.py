from modules.pages.base_page import BasePage
from modules.config import Config


class ProfilePage(BasePage):
    url = f"{Config.MEDIA_MARKT_BASE_URL}profile"

    # no need for methods here
