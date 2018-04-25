from selenium.webdriver.common.by import By
from modules.pages.base_page import BasePage
from modules.config import Config
from modules.forms.message import Message
from selenium.webdriver.support.ui import Select


class ProfilePage(BasePage):
    url = f"{Config.BASE_URL}profile"
    page_name = "Profile page"

    INPUTS_ARRAY = {"firstName", "lastName", "birthdate", "gender", "city", "zipcode", "country"}
    ZIP_CODE_INPUT = (By.NAME, "zipcode")
    ZIP_CODE_VALIDATION_FAIL = (By.XPATH, "//input[@name='zipcode']/following-sibling::div[@class='invalid-feedback' and contains(text(),'Invalid')]")
    ICON_CALENDAR = (By.CSS_SELECTOR, "span[class='icon-calendar']")
    CALENDAR_DAY_BUTTON = (By.CSS_SELECTOR, "td[aria-selected='false'] button[class='pika-button pika-day']")
    BIRTHDATE_INPUT = (By.NAME, "birthdate")
    UPDATE_PROFILE = (By.XPATH, "//button[contains(text(),'Update profile')]")
    # profile - email
    INACTIVE_EMAIL_TAB = (By.CSS_SELECTOR, "a[href='/profile/email'][class='mx-2 nav-link']")
    SAVE_BUTTON = (By.XPATH, "//button[contains(text(),'Save')]")
    EMAIL_INPUT = (By.NAME, "email")
    CURRENT_EMAIL = (By.XPATH, "//p[contains(text(),'Update profile')]")
    # profile - password
    INACTIVE_PASSWORD_TAB = (By.CSS_SELECTOR, "a[href='/profile/change-password'][class='mx-2 nav-link']")
    OLD_PASSWORD_INPUT = (By.NAME, "oldPassword")
    NEW_PASSWORD_INPUT = (By.NAME, "password")
    CONFIRM_PASSWORD_INPUT = (By.NAME, "confirmPassword")
    VALIDATOR_ERROR = (By.CSS_SELECTOR, "div[class='invalid-feedback']:not(:empty)")

    def input_field_validation_error(self):
        if self.driver.fast_check_if_element_exist(self.VALIDATOR_ERROR):
            return self.get_element(self.VALIDATOR_ERROR).text

    def set_input_by_name(self, element_name, value):
        if not element_name in self.INPUTS_ARRAY:
            self.driver.set_current_action(Message.FORM_INPUT_FIELD_MISSING.value.format(element_name))
            return self
        self.type((By.NAME, element_name), value)
        self.click_on(self.UPDATE_PROFILE)
        validation_message = self.input_field_validation_error()
        # pre-POST
        assert validation_message is None, validation_message
        self.wait_for_loader_to_disappear()
        validation_message = self.input_field_validation_error()
        # after-POST
        assert validation_message is None, validation_message
        return self

    def set_country(self, value):
        country_select = Select(self.driver.find_element_by_name('country'))
        country_select.select_by_value(value)
        self.click_on(self.UPDATE_PROFILE)
        self.wait_for_loader_to_disappear()
        return self

    def get_datetime_placeholder(self):
        birthdate_input = self.driver.find_element_by_name('birthdate')
        return birthdate_input.get_attribute('placeholder')

    def get_datetime_value(self):
        birthdate_input = self.driver.find_element_by_name('birthdate')
        return birthdate_input.get_attribute('value')

    def select_random_day(self):
        self.wait_for_loader_to_disappear()
        self.click_on(self.ICON_CALENDAR)
        self.click_on(self.CALENDAR_DAY_BUTTON)
        self.click_on(self.ICON_CALENDAR)
        self.click_on(self.UPDATE_PROFILE)
        self.wait_for_loader_to_disappear()
        return self

    def validate_zip_code_for_country(self, country):
        if country == "US":
            # wrong validation
            self.set_input_by_name("zipcode", "654321")
            # check if validator shows up
            if not self.driver.fast_check_if_element_exist(self.ZIP_CODE_VALIDATION_FAIL):
                return False
            # set 5 digits zipcode
            self.set_input_by_name("zipcode", "12345")
            zipcode_value = self.driver.find_element_by_name("zipcode").get_attribute("value")
            if zipcode_value == "12345":
                return True
            else:
                return False
        elif country == "CA":
            return

    def change_email(self, value):
        if self.driver.fast_check_if_element_exist(self.INACTIVE_EMAIL_TAB):
            self.click_on(self.INACTIVE_EMAIL_TAB)
        self.type(self.EMAIL_INPUT, value)
        self.click_on(self.SAVE_BUTTON)
        self.wait_for_loader_to_disappear()
        return self

    def check_current_email_visible(self, email):
        return self.driver.fast_check_if_element_exist((By.XPATH, f"//p[contains(text(),'{email}')]"))

    def change_password(self, old_password, new_password):
        if self.driver.fast_check_if_element_exist(self.INACTIVE_PASSWORD_TAB):
            self.click_on(self.INACTIVE_PASSWORD_TAB)
        self.type(self.OLD_PASSWORD_INPUT, old_password)
        self.type(self.NEW_PASSWORD_INPUT, new_password)
        self.type(self.CONFIRM_PASSWORD_INPUT, new_password)
        self.click_on(self.SAVE_BUTTON)
        self.wait_for_loader_to_disappear()
        return self
