from selenium.webdriver.common.by import By
from modules.pages.base_page import BasePage
from modules.forms.message import Message


class ProductPage(BasePage):
    BUY_NOW_BTN = (By.XPATH, "//div[contains(@class,'m-productAction_btn')]/a[./i]")
    SUCCESS_MESSAGE = (By.XPATH, "//p[contains(.,'Dodałeś pomyślnie produkt do koszyka')]")
    NO_PRODUCT_MESSAGE = (By.XPATH, "//p[contains(.,'Produkt chwilowo niedostępny!')]")
    PRE_CART_WINDOW_CLOSE_BTN = (By.CSS_SELECTOR, "div[id='js-preCart'] button[class*='mfp-close']")
    PRODUCT_AVAILABLE_STATUS = (By.CSS_SELECTOR, "a[href='/dostawa']")
    PRODUCT_AVAILABLE = (By.XPATH, "//a[contains(.,'Dostępny')]")
    PRODUCT_PRICE_BOX_LIST = (By.CSS_SELECTOR, "span[class*='is-price is-']")

    def is_product_available(self, product_name):
        self.driver.set_current_action(Message.CART_ADD.value.format(product_name))
        available_status = self.driver.wait_and_get_element(self.BUY_NOW_BTN).get_attribute('data-offer-ava')
        if available_status == "Dostępny!" or available_status == "":
            self.driver.set_current_action(Message.PRODUCT_AVAILABLE.value.format(product_name))
            return True
        else:
            self.driver.set_current_action(Message.PRODUCT_AVAILABLE_FAILED.value.format(available_status), "error")
            return False

    def add_product_to_cart(self, product_name):
        self.driver.set_current_action(Message.CART_ADD.value.format(product_name))
        self.driver.wait_for_element_and_click(self.BUY_NOW_BTN)

        # This product was add to cart ?
        try:
            self.driver.wait_and_get_element(self.SUCCESS_MESSAGE)
            self.driver.set_current_action(Message.CART_ADD_COMPLETE.value.format(product_name))
            self.driver.wait_for_element_and_click(self.PRE_CART_WINDOW_CLOSE_BTN)
            return True
        except Exception:
            self.driver.set_current_action(Message.CART_ADD_FAILED.value.format(product_name), "error")
            pass

        # No products online ?
        try:
            self.driver.wait_and_get_element(self.NO_PRODUCT_MESSAGE)
            self.driver.set_current_action(Message.CART_ADD_NO_PRODUCTS.value.format(product_name), "error")
            self.driver.wait_for_element_and_click(self.PRE_CART_WINDOW_CLOSE_BTN)
            return True
        except Exception:
            # some other error that we don't care at this point
            self.driver.set_current_action(Message.CART_ADD_FAILED.value.format(product_name), "error")
            pass

        return False

    def get_price(self):
        price_box = self.driver.wait_and_get_elements(self.PRODUCT_PRICE_BOX_LIST)
        price_string = []
        dot_limit = -1
        for element in price_box:
            if dot_limit == 0:
                break
            dot_limit -= 1
            element_class = element.get_attribute('class')
            number = element_class.split('-')[-1]
            if not number.isdigit():
                if number == "dot":
                    number = "."
                    dot_limit = 2
                else:
                    break
            price_string.append(number)
        return "".join(price_string)

    def compare_prices(self, expected_price):
        price_on_site = self.get_price()
        if float(price_on_site) <= float(expected_price):
            self.driver.set_current_action(Message.PRODUCT_PRICE.value.format(price_on_site, expected_price))
            return True
        else:
            self.driver.set_current_action(Message.PRODUCT_PRICE_FAIL.value.format(price_on_site, expected_price), "error")
            return False
