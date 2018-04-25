from selenium.webdriver.support.events import AbstractEventListener


class WebDriverListener(AbstractEventListener):
    def on_exception(self, exception, driver):
        driver.get_screenshot_as_file(driver.screenshot_full_path)  # path + filename + .png
        driver.set_current_action(f"{driver.current_action} - FAILED", "error", "Selenium WebDriver Exception")
        driver.quit()
