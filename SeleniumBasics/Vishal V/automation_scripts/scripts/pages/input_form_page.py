from selenium.webdriver.common.by import By

from .base_page import BasePage


class InputFormPage(BasePage):
    NAME_INPUT = (By.NAME, 'first_name')
    EMAIL_INPUT = (By.NAME, 'email')
    PHONE_INPUT = (By.NAME, 'mobile_no')
    ADDRESS_INPUT = (By.NAME, 'message')
    SUBMIT_BUTTON = (By.ID, 'contbtn')
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, '.success-message')

    def fill_form(self, name, email, phone, address):
        self.driver.execute_script("document.querySelector('input[name=\"first_name\"]').value = arguments[0];", name)
        self.driver.execute_script("document.querySelector('input[name=\"email\"]').value = arguments[0];", email)
        self.driver.execute_script("document.querySelector('input[name=\"mobile_no\"]').value = arguments[0];", phone)
        self.driver.execute_script("document.querySelector('textarea[name=\"message\"]').value = arguments[0];", address)

    def submit_form(self):
        button = self.wait_for_element(self.SUBMIT_BUTTON)
        self.driver.execute_script("arguments[0].click();", button)

    def get_success_message(self):
        return self.wait_for_element(self.SUCCESS_MESSAGE).text
