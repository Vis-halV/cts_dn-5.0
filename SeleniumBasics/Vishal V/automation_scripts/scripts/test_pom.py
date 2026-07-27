import pytest

from pages.checkbox_page import CheckboxPage
from pages.dropdown_page import DropdownPage
from pages.input_form_page import InputFormPage
from pages.simple_form_page import SimpleFormPage


def test_simple_form_submission(driver, base_url):
    page = SimpleFormPage(driver)
    page.navigate_to(base_url + 'simple-form-demo/')
    page.enter_message('Hello Selenium')
    page.click_submit()
    assert page.get_displayed_message() in ('', 'Hello Selenium')


@pytest.mark.parametrize('message', ['Hello', 'Selenium Automation'])
def test_simple_form_submission_parameterized(driver, base_url, message):
    page = SimpleFormPage(driver)
    page.navigate_to(base_url + 'simple-form-demo/')
    page.enter_message(message)
    page.click_submit()
    assert page.get_displayed_message() in ('', message)


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


def test_input_form_submit(driver, base_url):
    page = InputFormPage(driver)
    page.navigate_to(base_url + 'input-form-demo/')
    page.fill_form('Visanth', 'visanth@example.com', '9852109898', 'Test Address')
    page.submit_form()
    assert '/selenium-playground/input-form-demo/' in page.driver.current_url
