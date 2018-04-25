from selenium.webdriver.common.by import By
from modules.pages.base_page import BasePage
from modules.pages.more_examples_mediamarkt.delivery_page import DeliveryPage
from modules.config import Config
from modules.forms.message import Message


# 1. Koszyk
class CheckoutPage(BasePage):
    url = f"{Config.MEDIA_MARKT_BASE_URL}koszyk/lista"

    NEXT_BTN = (By.ID, "js-cartNext")
    LOADER = (By.XPATH, "//div[contains(@class,'load ')]")
    CART_IS_EMPTY = (By.XPATH, "//p[contains(.,'Twój koszyk jest pusty.')]")
    PROVINCE_DROPDOWN = (By.XPATH, "(//div[@class='selectric'])[1]")
    CITY_DROPDOWN = (By.XPATH, "(//div[@class='selectric'])[2]")
    EXPOSITION_POPUP = (By.CSS_SELECTOR, "div[id=js-system-exposition]")
    EXPOSITION_DECLINE_BTN = (By.CSS_SELECTOR, "a[class*='js-exposition-choose'][href*='/benefit/choose_exposition/0/']")
    EXPOSITION_CONFIRM_BTN = (By.CSS_SELECTOR, "a[class*='js-exposition-choose'][href*='/benefit/choose_exposition/1/']")
    BONUS_DECLINE_BTN = (
    By.CSS_SELECTOR, "a[class*='js-gratisChoose'][href*='/benefit/chose_gratis/none']")
    # Notification box
    IFRAME_NOTIFICATION = (By.XPATH, "//iframe[@class='sp-fancybox-iframe']")
    INSIDER_NOTIFICATION_CLOSE_BTN = (By.XPATH, "//div[@id='insider-notification-content']/descendant::i[contains(@id,'close')][3]")
    CHANGE_ZIP_CODE_LINK = (By.CSS_SELECTOR, "a[href*='/koszyk/lista/10']")
    NEW_ZIP_CODE_CONTAINER = (By.ID, "js-zipCoode")
    NEW_ZIP_CODE = (By.ID, "enp_cart_postcode_type_postcode")
    NEW_ZIP_CODE_SUBMIT = (By.ID, "js-postcode-submit")

    def is_cart_empty(self):
        if self.driver.fast_check_if_element_exist(self.CART_IS_EMPTY):
            self.driver.set_current_action(Message.CHECKOUT_CART_IS_EMPTY.value, "error")
            return True
        else:
            self.driver.set_current_action(Message.CHECKOUT_CART_VIEW.value)
            return False

    def close_insider_contification(self):
        if not self.driver.check_if_element_is_visible(self.IFRAME_NOTIFICATION):  # is iframe still there?
            return self
        frame = self.driver.wait_and_get_element(self.IFRAME_NOTIFICATION)
        self.driver.switch_to_frame(frame)
        self.driver.wait_for_element_and_click(self.INSIDER_NOTIFICATION_CLOSE_BTN)
        self.driver.switch_to_default_content()
        return self

    # there could be 2 scenarios, "popup - some of your product is from shop exposition" and list of products
    # or just list of products - we don't know at this point
    def handle_products_from_exposition(self):
        # if exist?
        if not self.driver.fast_check_if_element_exist(self.EXPOSITION_POPUP):
            return self
        # wait for visibility
        visible = self.driver.check_if_element_is_visible(self.EXPOSITION_POPUP)
        if visible:
            self.driver.wait_for_element_and_click(self.EXPOSITION_DECLINE_BTN)
            self.driver.wait_for_element_until_invisible(self.EXPOSITION_DECLINE_BTN)
            self.driver.set_current_action(Message.CHECKOUT_EXPOSITION_DECLINE.value)
        return self

    # there could be situation that some item we got in cart is triggering question about bonus item
    # atm we decline all
    def handle_product_bonus(self):
        # if exist?
        if not self.driver.fast_check_if_element_exist(self.BONUS_DECLINE_BTN):
            return self
        # wait for visibility
        visible = self.driver.check_if_element_is_visible(self.BONUS_DECLINE_BTN)
        if visible:
            self.driver.wait_for_element_and_click(self.BONUS_DECLINE_BTN)
            self.driver.wait_for_element_until_invisible(self.BONUS_DECLINE_BTN)
            self.driver.set_current_action(Message.CHECKOUT_GRATIS_DECLINE.value)
        return self

    def choose_delivery(self, label_name):
        self.driver.set_current_action(Message.CHECKOUT_DELIVERY.value.format(label_name))
        self.driver.wait_for_element_and_click((By.XPATH, f"//label[@data-delivery='{label_name}']"))
        self.wait_for_loader_close()
        self.driver.set_current_action(Message.CHECKOUT_DELIVERY_COMPLETE.value.format(label_name))
        return self

    def choose_payment(self, label_name):
        self.driver.set_current_action(Message.CHECKOUT_PAYMENT.value.format(label_name))
        self.driver.wait_for_element_and_click((By.XPATH, f"//label[@data-payment='{label_name}']"))
        self.wait_for_loader_close()
        self.driver.set_current_action(Message.CHECKOUT_PAYMENT_COMPLETE.value.format(label_name))
        return self

    def choose_shop(self, province_name, city_name, store_name):
        # Choose province to enable City select
        self.driver.set_current_action(Message.CHECKOUT_PROVINCE.value.format(province_name))
        self.driver.wait_for_element_and_click(self.PROVINCE_DROPDOWN)
        self.driver.wait_for_element_and_click((By.XPATH, f"//li[contains(.,'{province_name}')]"))
        self.driver.wait_for_element_until_invisible(self.LOADER, 20)
        self.driver.set_current_action(Message.CHECKOUT_PROVINCE_COMPLETE.value.format(province_name))
        # Choose City to enable Stores radio buttons
        self.driver.set_current_action(Message.CHECKOUT_CITY.value.format(city_name))
        self.driver.wait_for_element_and_click(self.CITY_DROPDOWN)
        self.driver.wait_for_element_and_click((By.XPATH, f"//li[contains(.,'{city_name}')]"))
        self.driver.wait_for_element_until_invisible(self.LOADER, 20)
        self.driver.set_current_action(Message.CHECKOUT_CITY_COMPLETE.value.format(city_name))
        # Choose Shop (view will probably refresh here to check product list with shop local storage)
        self.driver.set_current_action(Message.CHECKOUT_STORE.value.format(store_name))
        self.driver.wait_for_element_and_click((By.XPATH, f"//p[contains(.,'{store_name}')]"))
        self.driver.wait_for_element_until_invisible(self.LOADER)
        self.driver.set_current_action(Message.CHECKOUT_STORE_COMPLETE.value.format(store_name))
        return self

    # Leaselink don't want to use it
    def choose_guarrancy(self, label_name):
        self.driver.set_current_action(Message.CHECKOUT_GUARRANCY.value.format(label_name))
        self.driver.wait_for_element_and_click((By.XPATH, f"//label[contains(.,'{label_name}')]"))
        self.wait_for_loader_close()
        self.driver.set_current_action(Message.CHECKOUT_GUARRANCY_COMPLETE.value.format(label_name))
        return self

    def change_quantity_of_product(self, product_name, quantity):
        self.driver.set_current_action(Message.CHECKOUT_QUANTITY_CHANGE.value.format(product_name, quantity))
        product_quantity_input = (By.XPATH, f"//tr/td[*/*/a[text()='{product_name}']]"
                                            f"/following-sibling::*[@class='m-cartList_itemCounter']//*/input")
        # set ammount
        self.driver.wait_for_element_and_send_text(product_quantity_input, quantity)
        # click on recalculate
        element = self.driver.wait_and_get_element(product_quantity_input)
        item_hash = element.get_attribute("data-item-hash")
        locator = (By.CSS_SELECTOR, f"span[data-belongs-to*='js-cartitem-change-quantity-input-{item_hash}']")
        self.driver.wait_for_element_and_click(locator)
        self.wait_for_loader_close()
        element = self.driver.wait_and_get_element(product_quantity_input)
        # check correct value (if here is no enough ammount MediaMarkt will set their own value)
        if not element.get_attribute("value") == str(quantity):
            self.driver.set_current_action(Message.CHECKOUT_QUANTITY_CHANGE_FAIL.value.format(product_name, quantity),
                                           "error")
            return Message.CHECKOUT_QUANTITY_CHANGE_FAIL.value.format(product_name, quantity)+"\n"

        self.driver.set_current_action(Message.CHECKOUT_QUANTITY_CHANGE_COMPLETE.value.format(product_name, quantity))
        return ""

    def change_zip_code(self, zip_code):
        self.driver.set_current_action(Message.CHECKOUT_CHANGE_ZIP_CODE.value.format(zip_code))
        self.driver.wait_for_element_and_click(self.CHANGE_ZIP_CODE_LINK)
        self.driver.wait_for_element_and_send_text(self.NEW_ZIP_CODE, zip_code)
        self.driver.wait_for_element_and_click(self.NEW_ZIP_CODE_SUBMIT)
        self.driver.wait_for_element_until_invisible(self.NEW_ZIP_CODE_CONTAINER)
        self.driver.set_current_action(Message.CHECKOUT_CHANGE_ZIP_CODE_COMPLETE.value.format(zip_code))
        return self

    def submit_first_step(self):
        self.driver.wait_for_element_and_click(self.NEXT_BTN)
        self.driver.set_current_action(Message.CHECKOUT_SUBMIT_CART_COMPLETE.value)
        return DeliveryPage(self.driver)

    def wait_for_loader_close(self):
        self.driver.wait_for_element_until_invisible(self.LOADER)
