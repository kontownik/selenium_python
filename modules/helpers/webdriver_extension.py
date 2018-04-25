import os
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from modules.config import Config
from modules.forms.message import Message


class WebDriver(webdriver.Chrome):
    timeout = Config.DEFAULT_TIMEOUT

    def __init__(self, browser):
        self.screenshot_full_path = "/tmp/temp.png"
        self.current_action = Message.REQUEST_STARTING.value
        chrome_options = webdriver.ChromeOptions()
        if browser == 'chrome-window-mode':
            webdriver.Chrome.__init__(self, ChromeDriverManager().install(), chrome_options=chrome_options)
        elif browser == 'chrome-headless':
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument(f"--window-size={os.environ.get('CHROME_WINDOW_SIZE')}")
            webdriver.Chrome.__init__(self, ChromeDriverManager().install(), chrome_options=chrome_options)

    def wait_for_element_and_click(self, element, time=timeout):
        WebDriverWait(self, time).until(
            EC.presence_of_element_located(element), "Element is not present"
        )
        WebDriverWait(self, time).until(
            EC.element_to_be_clickable(element), "Element is not clickable"
        )
        self.find_element(*element).click()

    def wait_for_element_and_send_text(self, element, text, time=timeout):
        WebDriverWait(self, time).until(
            EC.presence_of_element_located(element), "Element is not present"
        )
        self.find_element(*element).clear()
        self.find_element(*element).send_keys(text)

    def check_if_element_is_invisible(self, element, time=timeout):
        try:
            WebDriverWait(self, time).until(
                EC.invisibility_of_element_located(element), "Element is not invisible"
            )
            return True
        except TimeoutException:
            return False

    def wait_for_element_and_get_text(self, element, time=timeout):
        WebDriverWait(self, time).until(
            EC.presence_of_element_located(element), "Element is not present"
        )
        return self.find_element(*element).text

    def wait_for_element_and_get_text_from_input(self, element, time=timeout):
        WebDriverWait(self, time).until(
            EC.presence_of_element_located(element), "Element is not present"
        )
        return self.find_element(*element).get_attribute("value")

    def wait_and_get_element(self, element, time=timeout):
        WebDriverWait(self, time).until(
            EC.presence_of_element_located(element), "Element is not present"
        )
        return self.find_element(*element)

    def wait_and_get_elements(self, element, time=timeout):
        WebDriverWait(self, time).until(
            EC.presence_of_element_located(element), "Element is not present"
        )
        return self.find_elements(*element)

    def wait_for_element(self, element, time=timeout):
        try:
            WebDriverWait(self, time).until(
                EC.presence_of_element_located(element), "Element is not present"
            )
        except:
            pass

    def wait_for_element_until_invisible(self, element, time=timeout):
        WebDriverWait(self, time).until(
            EC.invisibility_of_element_located(element), "Element is not invisible"
        )

    def wait_for_element_until_visible(self, element, time=timeout):
        WebDriverWait(self, time).until(
            EC.visibility_of_element_located(element), "Element is not visible"
        )

    def check_if_element_is_visible(self, element, time=timeout):
        self.wait_for_element(element, time)
        elements = self.find_elements(*element)
        if len(elements) > 0:
            return True
        else:
            return False

    def fast_check_if_element_exist(self, element):
        elements = self.find_elements(*element)
        if len(elements) > 0:
            return True
        else:
            return False

    def check_visible_of_elements(self, elements, time=timeout):
        for element in elements:
            self.wait_for_element(time)
            searched_elements = self.find_elements(*element)
            if len(searched_elements) < 1:
                return False
        return True

    def set_current_action(self, action="No message", message_type="info", exception_message=""):
        self.current_action = action
        print(f"[{message_type}] {action} {exception_message}")
