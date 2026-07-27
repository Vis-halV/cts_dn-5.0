import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_simple_form_submission(driver, base_url):
    driver.get(base_url + "simple-form-demo")
    message_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "user-message"))
    )
    message_input.clear()
    message_input.send_keys("Hello Selenium")
    driver.find_element(By.ID, "showInput").click()
    result = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "message"))
    )
    assert result is not None


@pytest.mark.parametrize("message", ["Hello", "Selenium Automation"])
def test_simple_form_submission_parameterized(driver, base_url, message):
    driver.get(base_url + "simple-form-demo")
    message_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "user-message"))
    )
    message_input.clear()
    message_input.send_keys(message)
    driver.find_element(By.ID, "showInput").click()
    result = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "message"))
    )
    assert result is not None


def test_checkbox_demo(driver, base_url):
    driver.get(base_url + "checkbox-demo")
    checkbox = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//label[text()='Option 1']/input"))
    )
    assert checkbox.is_selected() is False
    checkbox.click()
    assert checkbox.is_selected() is True
    checkbox.click()
    assert checkbox.is_selected() is False


def test_dropdown_selection(driver, base_url):
    driver.get(base_url + "select-dropdown-demo")
    dropdown = Select(WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "select-demo"))
    ))
    dropdown.select_by_visible_text("Wednesday")
    assert dropdown.first_selected_option.text == "Wednesday"
