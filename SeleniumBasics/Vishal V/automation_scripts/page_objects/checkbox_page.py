from selenium.webdriver.common.by import By

from .base_page import BasePage


class CheckboxPage(BasePage):
    OPTION_1 = (By.XPATH, "//label[text()='Option 1']/input")

    def check_option(self, index):
        option = self.driver.find_elements(*self.OPTION_1)[index]
        if not option.is_selected():
            option.click()
        return option

    def uncheck_option(self, index):
        option = self.driver.find_elements(*self.OPTION_1)[index]
        if option.is_selected():
            option.click()
        return option

    def is_option_checked(self, index):
        option = self.driver.find_elements(*self.OPTION_1)[index]
        return option.is_selected()
