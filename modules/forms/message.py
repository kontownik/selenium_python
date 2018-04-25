from enum import Enum


class Message(Enum):

    LOGIN = "Trying to login by login form"
    GO_DASHBOARD = "Trying to get to 'Dashboard' by topbar menu"
    GO_LOCATIONS = "Trying to get to 'Locations' by topbar menu"
    GO_PEOPLE = "Trying to get to 'People' by topbar menu"
    GO_REPORTS = "Trying to get to 'Reports' by topbar menu"
    GO_PROFILE = "Trying to get to 'Profile' by topbar menu"
    GO_TOKENS = "Trying to get to 'Tokens' by topbar menu"
    GO_LOGOUT = "Trying to 'Logout' by topbar menu"
    FORM_INPUT_FIELD_MISSING = "'{}' field not exist in this form"

    REQUEST_STARTING = "Starting request"
    WEBDRIVER_ERROR = "WebDriver init error, please contact administrator"
    ORDER_CHECK_SPLIT = "Warning! Order '{}' is splitted to more than one order.\n"
    PAGE_LOADED = "{} page loaded successful"
    SEARCH_PRODUCT = "Trying to search for '{}'"
    SEARCH_PRODUCT_COMPLETE = "Search results for '{}' loaded"
    SEARCH_PRODUCT_PICK = "Trying to pick '{}' from list"
    SEARCH_PRODUCT_PICK_COMPLETE = "Picked '{}' from list"
    SEARCH_PRODUCT_NOT_FOUND = "Product '{}' not found in search results"  # ERROR
    SEARCH_PRODUCT_REDIRECTED = "You are redirected to '{}' product page"
    CART_ADD = "Trying to add '{}' to cart"
    CART_ADD_COMPLETE = "Product '{}' added to cart"
    CART_ADD_NO_PRODUCTS = "Online store don't get any '{}' in storage, please try later"   # ERROR
    CART_ADD_FAILED = "Product '{}' IS NOT added to cart"   # ERROR
    CART_PRE_CART_WINDOW_CLOSE = "Trying to close pre-cart window"
    PRODUCT_PAGE_LOADED = "Product '{}' page is loaded"
    PRODUCT_AVAILABLE = "Product '{}' is available"
    PRODUCT_AVAILABLE_FAILED = "Product IS NOT available, message: '{}'"  # ERROR
    PRODUCT_PRICE = "Product price on site '{}' is OK with expected '{}'"
    PRODUCT_PRICE_FAIL = "Product price '{}' is bigger than expected '{}'"  # ERROR
    PRODUCT_NOT_ADDED_TO_CART = "Product '{}' was skipped in this order request, check logs for more informations.\n"
    CHECKOUT_EXPOSITION_DECLINE = "Question about 'exposition' is closed"
    CHECKOUT_GRATIS_DECLINE = "Question about 'gratis' is closed"
    CHECKOUT_CART_IS_EMPTY = "Cart is empty"   # ERROR
    CHECKOUT_CART_VIEW = "Cart is open and isn't empty"
    CHECKOUT_GREEN_BOX = "Notification (green box) popup"
    CHECKOUT_GREEN_BOX_COMPLETE = "Notification (green box) closed"
    CHECKOUT_DELIVERY = "Trying to set delivery type to '{}'"
    CHECKOUT_DELIVERY_COMPLETE = "Delivery type set to '{}'"
    CHECKOUT_PAYMENT = "Trying to set payment method to '{}'"
    CHECKOUT_PAYMENT_COMPLETE = "Payment method set to '{}'"
    CHECKOUT_PROVINCE = "Trying to set '{}' province"
    CHECKOUT_PROVINCE_COMPLETE = "Province '{}' picked"
    CHECKOUT_CITY = "Trying to set '{}' city"
    CHECKOUT_CITY_COMPLETE = "City '{}' picked"
    CHECKOUT_STORE = "Trying to pick '{}' store"
    CHECKOUT_STORE_COMPLETE = "Store '{}' picked"
    CHECKOUT_GUARRANCY = "Trying to set guarrancy service to '{}'"
    CHECKOUT_GUARRANCY_COMPLETE = "Guarrancy service set to '{}'"
    CHECKOUT_QUANTITY_CHANGE = "Trying to change quantity of '{}' to {}"
    CHECKOUT_QUANTITY_CHANGE_COMPLETE = "Quantity of '{}' is set to {}"
    CHECKOUT_QUANTITY_CHANGE_FAIL = "Set quantity of '{}' to '{}' failed, product is not available in this amount"
    CHECKOUT_CHANGE_ZIP_CODE = "Trying to change client zip-code to '{}'"
    CHECKOUT_CHANGE_ZIP_CODE_COMPLETE = "Zip-code changed to '{}'"
    CHECKOUT_SUBMIT_CART_COMPLETE = "Cart (Step 1) submitted redirected to Delivery (Step 2) "
    CHECKOUT_CLOSING_INSIDER_WINDOW = "Start closing insider window "
    CHECKOUT_CLOSING_INSIDER_WINDOW_SUCCESS = "Insider window has been successfully closed"
    CHECKOUT_CLOSING_INSIDER_WINDOW_FAILED = "Insider window is not visible or it has been automatically closed"
    DELIVERY_ORDER_AS = "Order as '{}'"
    DELIVERY_CLIENT_DATA = "Trying to set client delivery data"
    DELIVERY_ALL_ACCEPTED = "All 'Zgody formalne' accepted"
    DELIVERY_COMMENT = "Comment added '{}'"
    DELIVERY_SUBMIT = "Trying to submit Delivery form"
    DELIVERY_SUBMIT_COMPLETE = "Delivery submit, redirect to Summary page"
    SUMMARY_REDIRECTED = "Redirected to payment website"
    SUMMARY_GET_ORDER_ID = "Waiting for order number (description)"
    SUMMARY_GET_ORDER_ID_FAILED = "Failed to get order ID"  # ERROR
    SUMMARY_GET_ORDER_ID_COMPLETE = "Got order number (description) '{}'"
    ORDER_STATUS = "Trying to get 'Order status'"
    ORDER_STATUS_COMPLETE = "Order status is '{}'"
    ORDER_PDF_LINK = "Trying to get 'PDF Link'"
    ORDER_PDF_LINK_COMPLETE = "Got PDF Link '{}'"