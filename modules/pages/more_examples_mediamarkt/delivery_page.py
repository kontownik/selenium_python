from selenium.webdriver.common.by import By
from modules.pages.base_page import BasePage
from modules.pages.more_examples_mediamarkt.summary_page import SummaryPage
from modules.config import Config
from modules.forms.message import Message


# 2. Dostawa i faktura
class DeliveryPage(BasePage):
    url = f"{Config.MEDIA_MARKT_BASE_URL}koszyk/adres"

    ADDRESS_NEXT_BTN = (By.ID, "js-validBtn")
    ACCEPT_RULES_CHECKBOX = (By.XPATH, "//strong[contains(.,'Zapoznałem się i akceptuję')]")
    ACCEPT_ALL_CHECKBOX = (By.XPATH, "//strong[contains(.,'Zaznacz wszystkie')]")
    ACCEPT_AND_PAY_BTN = (By.ID, "js-summation_submit")
    ORDER_COMMENTS = (By.ID, "cart_flow_address_step_customerComment")
    LOADER = (By.XPATH, "//div[contains(@class,'load ')]")
    ORDERING_AS_COMPANY = (By.XPATH, "//label[contains(.,'Firma')]")
    INVOICE_CONTAINER = (By.ID, "js-invoice-container")
    INVOICE_CHECKBOX = (By.XPATH, "//label[contains(.,'Chcę otrzymać fakturę VAT')]")
    # Zamawiam jako 'Firma'
    COMPANY_NAME = (By.ID, "cart_flow_address_step_accountAddress_company")
    COMPANY_NIP = (By.ID, "cart_flow_address_step_accountAddress_nip")
    COMPANY_EMAIL = (By.ID, "cart_flow_address_step_accountAddress_email")
    COMPANY_PHONE = (By.ID, "cart_flow_address_step_accountAddress_phone")
    COMPANY_STREET = (By.ID, "cart_flow_address_step_accountAddress_street")
    COMPANY_HOUSE_NUMBER = (By.ID, "cart_flow_address_step_accountAddress_houseNumber")
    COMPANY_APARTMENT = (By.ID, "cart_flow_address_step_accountAddress_apartmentNumber")
    # Client data
    DELIVERY_OTHER_ADDRESS = (By.XPATH, "//p[contains(.,'Inny adres dostawy')]/following-sibling::div/label[contains(.,'Tak')]")
    DELIVERY_SAME_ADDRESS = (By.XPATH, "//p[contains(.,'Inny adres dostawy')]/following-sibling::div/label[contains(.,'Nie')]")
    DELIVERY_COMPANY_NAME = (By.ID, "cart_flow_address_step_transportAddress_company")
    DELIVERY_FIRST_NAME = (By.ID, "cart_flow_address_step_transportAddress_firstName")
    DELIVERY_LAST_NAME = (By.ID, "cart_flow_address_step_transportAddress_lastName")
    DELIVERY_PHONE = (By.ID, "cart_flow_address_step_transportAddress_phone")
    DELIVERY_STREET = (By.ID, "cart_flow_address_step_transportAddress_street")
    DELIVERY_HOUSE_NUMBER = (By.ID, "cart_flow_address_step_transportAddress_houseNumber")
    DELIVERY_APARTMENT = (By.ID, "cart_flow_address_step_transportAddress_apartmentNumber")
    DELIVERY_ZIP_CODE = (By.ID, "cart_flow_address_step_transportAddress_postcode")
    DELIVERY_CITY = (By.ID, "cart_flow_address_step_transportAddress_city")

    # Zamawiam jako 'Firma'
    def order_as_company(self, data_dict):
        self.driver.wait_for_element_and_click(self.ORDERING_AS_COMPANY)
        self.driver.wait_for_element_and_send_text(self.COMPANY_NAME, data_dict["company_name"])
        self.driver.wait_for_element_and_send_text(self.COMPANY_NIP, data_dict["nip"])
        self.driver.wait_for_element_and_send_text(self.COMPANY_EMAIL, data_dict["email"])
        # final client phone goes here
        self.driver.wait_for_element_and_send_text(self.COMPANY_PHONE, data_dict["client_phone_number"])
        self.driver.wait_for_element_and_send_text(self.COMPANY_STREET, data_dict["street"])
        self.driver.wait_for_element_and_send_text(self.COMPANY_HOUSE_NUMBER, data_dict["street_number"])
        self.driver.wait_for_element_and_send_text(self.COMPANY_APARTMENT, data_dict["local_number"])
        # we always take 'invoice/faktura'
        if data_dict["vat_invoice"]:
            invoice_style = self.driver.wait_and_get_element(self.INVOICE_CONTAINER).get_attribute('style')
            if "display: block;" not in invoice_style:
                self.driver.wait_for_element_and_click(self.INVOICE_CHECKBOX)
        return self

    def set_client_delivery(self, data_dict):
        self.driver.set_current_action(Message.DELIVERY_CLIENT_DATA.value)
        self.wait_for_loader_close()
        if data_dict['other_delivery_address']:
            self.driver.wait_for_element_and_click(self.DELIVERY_OTHER_ADDRESS)
        else:
            self.driver.wait_for_element_and_click(self.DELIVERY_SAME_ADDRESS)
        self.driver.wait_for_element_and_send_text(self.DELIVERY_COMPANY_NAME, data_dict["company_name"])
        self.driver.wait_for_element_and_send_text(self.DELIVERY_FIRST_NAME, data_dict["name"])
        self.driver.wait_for_element_and_send_text(self.DELIVERY_LAST_NAME, data_dict["surname"])
        self.driver.wait_for_element_and_send_text(self.DELIVERY_PHONE, data_dict["phone_number"])
        self.driver.wait_for_element_and_send_text(self.DELIVERY_STREET, data_dict["street"])
        self.driver.wait_for_element_and_send_text(self.DELIVERY_HOUSE_NUMBER, data_dict["street_number"])
        self.driver.wait_for_element_and_send_text(self.DELIVERY_APARTMENT, data_dict["local_number"])
        zip_code_input = self.driver.wait_and_get_element(self.DELIVERY_ZIP_CODE)
        # sometimes zip code is readonly field
        if not zip_code_input.get_attribute('readonly') == 'true':
            self.driver.wait_for_element_and_send_text(self.DELIVERY_ZIP_CODE, data_dict["delivery_zip_code"])
        self.driver.wait_for_element_and_send_text(self.DELIVERY_CITY, data_dict["city"])
        return self

    def accept_rules(self):
        self.driver.wait_for_element_and_click(self.ACCEPT_ALL_CHECKBOX)
        self.driver.set_current_action(Message.DELIVERY_ALL_ACCEPTED.value)
        return self

    def order_comment(self, comment):
        self.driver.set_current_action(Message.DELIVERY_COMMENT.value.format(comment))
        self.driver.wait_for_element_and_send_text(self.ORDER_COMMENTS, comment)
        return self

    def wait_for_loader_close(self):
        self.driver.wait_for_element_until_invisible(self.LOADER)

    def submit_second_step(self):
        self.driver.set_current_action(Message.DELIVERY_SUBMIT.value)
        self.driver.wait_for_element_and_click(self.ADDRESS_NEXT_BTN)
        self.driver.set_current_action(Message.DELIVERY_SUBMIT_COMPLETE.value)
        return SummaryPage(self.driver)
