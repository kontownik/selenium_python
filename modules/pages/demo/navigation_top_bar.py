from selenium.webdriver.common.by import By
from modules.pages.base_page import BasePage
from modules.forms.message import Message
from modules.pages.demo.profile_page import ProfilePage
from modules.pages.demo.token_page import TokensPage


class NavigationTopBar(BasePage):

    TOGGLE_ICON = (By.CSS_SELECTOR, "button[class='navbar-toggler']")

    DASHOBOARD_ITEM = (By.CSS_SELECTOR, "a[href='/']")
    LOCATIONS_ITEM = (By.CSS_SELECTOR, "a[href='/locations']")
    PEOPLE_ITEM = (By.CSS_SELECTOR, "a[href='/people']")
    REPORTS_ITEM = (By.CSS_SELECTOR, "a[href='/reports']")
    PROFILE_ITEM = (By.CSS_SELECTOR, "a[href='/profile']")
    TOKENS_ITEM = (By.CSS_SELECTOR, "a[href='/tokens']")
    LOGOUT_ITEM = (By.CSS_SELECTOR, "a[href='/logout']")
    ORGANIZATION_DIV = (By.CSS_SELECTOR, "div[class*='navbar-organization-picker']")

    def __init__(self, driver, user):
        self.user_type = user.user_type
        self.active = True
        super().__init__(driver)

    def handle_menu_toggle(self):
        if self.driver.fast_check_if_element_exist(self.TOGGLE_ICON):  # if exist?
            toggle_icon = self.driver.wait_and_get_element(self.TOGGLE_ICON)
            if toggle_icon.is_enabled() and toggle_icon.is_displayed():
                toggle_icon.click()

    def go_dashboard(self):
        self.handle_menu_toggle()
        self.click_on(self.DASHOBOARD_ITEM)
        return self

    def go_locations(self):
        self.handle_menu_toggle()
        self.click_on(self.LOCATIONS_ITEM)
        return self

    def go_people(self):
        self.handle_menu_toggle()
        self.click_on(self.PEOPLE_ITEM)
        return self

    def go_reports(self):
        self.handle_menu_toggle()
        self.click_on(self.REPORTS_ITEM)
        return self

    def go_profile(self):
        self.handle_menu_toggle()
        self.click_on(self.PROFILE_ITEM)
        return ProfilePage(self.driver)

    def go_tokens(self):
        self.handle_menu_toggle()
        self.click_on(self.TOKENS_ITEM)
        return TokensPage(self.driver)

    def go_logout(self):
        self.handle_menu_toggle()
        self.click_on(self.LOGOUT_ITEM)

    def change_organizations(self, name):
        self.click_on(self.ORGANIZATION_DIV)
        dropdown_item = self.driver.wait_and_get_element((By.XPATH, f"//button[contains(text(),'{name}')]"))
        dropdown_item.click()
        return self
