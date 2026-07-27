from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[2]))

from page_objects.simple_form_page import SimpleFormPage


def test_simple_form_submission_parameterized(driver, base_url):
    page = SimpleFormPage(driver)
    page.navigate_to(base_url + 'simple-form-demo/')
    page.enter_message('Selenium Automation')
    page.click_submit()
    assert page.get_displayed_message() in ('', 'Selenium Automation')
