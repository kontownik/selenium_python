import pytest

from data.credentials import user, admin, user_change_email
from modules.helpers.webdriver_extension import WebDriver
from modules.pages.demo.navigation_top_bar import NavigationTopBar
from modules.pages.demo.profile_page import ProfilePage


@pytest.mark.parametrize('login', [user], indirect=True, scope='function')
def test_001_user_update_country_and_date(driver: WebDriver, login):
    profile_page = ProfilePage(driver)
    profile_page.wait_for_redirect()
    profile_page.wait_for_loader_to_disappear()

    # user pick some random country
    profile_page.set_country("AL")

    # user pick USA, USA zip code and date format validation
    profile_page.set_country("US")
    profile_page.select_random_day()
    assert profile_page.get_datetime_placeholder() == "MM-DD-YYYY", "Birthdate should be formatted like 'MM-DD-YYYY'"
    assert "-" in profile_page.get_datetime_value(), f"{profile_page.get_datetime_value()} should be formatted like 'MM-DD-YYYY'"
    assert profile_page.validate_zip_code_for_country("US"), "Valid zip-code for US is not updated"

    # user pick Canada, zip code and date format validation
    profile_page.set_country("CA")
    profile_page.select_random_day()
    assert profile_page.get_datetime_placeholder() == "DD/MM/YYYY", "Birthdate should be formatted like 'DD/MM/YYYY'"
    assert "/" in profile_page.get_datetime_value(), f"{profile_page.get_datetime_value()} should be formatted like 'DD/MM/YYYY'"


@pytest.mark.parametrize('login', [user_change_email], indirect=True, scope='function')
def test_002_user_change_email(driver: WebDriver, login):
    some_email = "a098@a098.com"

    profile_page = ProfilePage(driver)
    profile_page.wait_for_redirect()
    profile_page.wait_for_loader_to_disappear()
    profile_page.change_email(some_email)
    assert profile_page.check_current_email_visible(some_email), "Current email don't match"
    profile_page.change_email(user_change_email.email)
    assert profile_page.check_current_email_visible(user_change_email.email), "Current email don't match"


@pytest.mark.parametrize('login', [user], indirect=True, scope='function')
def test_003_user_change_password(driver: WebDriver, login):
    some_new_pass = "Tester1234"
    some_new_pass2 = "Tester12345"

    profile_page = ProfilePage(driver)
    profile_page.wait_for_redirect()
    profile_page.wait_for_loader_to_disappear()
    profile_page.change_password(user.password, some_new_pass)
    profile_page.change_password(some_new_pass, some_new_pass2)
    profile_page.change_password(some_new_pass2, user.password)


@pytest.mark.parametrize('login', [user_change_email], indirect=True, scope='function')
def test_004_user_update_names(driver: WebDriver, login):
    profile_page = ProfilePage(driver)
    profile_page.wait_for_redirect()
    profile_page.wait_for_loader_to_disappear()
    profile_page.set_input_by_name("lastName", "StaffUser")


# (navigation bar)
@pytest.mark.parametrize('login', [admin], indirect=True, scope='function')
def test_005_admin_navigate_by_topbar(driver: WebDriver, login):
    nav = NavigationTopBar(driver, user)
    nav.go_dashboard()
    nav.go_locations()
    nav.go_people()
    nav.go_tokens()
    nav.go_profile()
    nav.change_organizations("Colorado INC_2")
    nav.change_organizations("Organization_3")
    nav.go_logout()
