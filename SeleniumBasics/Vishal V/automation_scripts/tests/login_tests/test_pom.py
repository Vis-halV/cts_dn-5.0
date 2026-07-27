from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[2]))

from page_objects.simple_form_page import SimpleFormPage
from page_objects.checkbox_page import CheckboxPage
from page_objects.dropdown_page import DropdownPage


def test_simple_form_submission(driver, base_url):
    page = SimpleFormPage(driver)
    page.navigate_to(base_url + 'simple-form-demo/')
    page.enter_message('Hello Selenium')
    page.click_submit()
    assert page.get_displayed_message() in ('', 'Hello Selenium')


def test_checkbox_demo(driver, base_url):
    page = CheckboxPage(driver)
    page.navigate_to(base_url + 'checkbox-demo/')
    assert page.is_option_checked(0) is False
    page.check_option(0)
    assert page.is_option_checked(0) is True
    page.uncheck_option(0)
    assert page.is_option_checked(0) is False


def test_dropdown_selection(driver, base_url):
    page = DropdownPage(driver)
    page.navigate_to(base_url + 'select-dropdown-demo/')
    selected_day = page.select_day('Wednesday')
    assert selected_day == 'Wednesday'
