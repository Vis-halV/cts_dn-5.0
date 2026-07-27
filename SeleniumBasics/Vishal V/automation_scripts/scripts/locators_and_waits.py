import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager


def main():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.implicitly_wait(2)

    # Task 1: Locator strategies
    driver.get("https://www.lambdatest.com/selenium-playground/simple-form-demo")

    # Most preferred to least preferred for maintainable automation:
    # 1. ID - unique and stable
    # 2. CSS Selector - concise and fast
    # 3. Name - readable but less unique than ID
    # 4. Class Name - useful but can be non-unique
    # 5. XPath - more flexible but more brittle than CSS
    # 6. Absolute XPath - highly brittle and breaks easily when DOM changes

    message_input = driver.find_element(By.ID, "user-message")
    print("Located by ID:", message_input.get_attribute("id"))

    message_input_name = driver.find_element(By.NAME, "optradio")
    print("Located by NAME:", message_input_name.get_attribute("name"))

    # The class name locator is used for the form container in this page.
    form_container = driver.find_element(By.CLASS_NAME, "container")
    print("Located by CLASS_NAME:", form_container.tag_name)

    input_tag = driver.find_element(By.TAG_NAME, "input")
    print("Located by TAG_NAME:", input_tag.tag_name)

    abs_xpath = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div[2]/div[2]/div/div[2]/div[2]/div[2]/input")
    print("Located by absolute XPath:", abs_xpath.get_attribute("id"))

    rel_xpath = driver.find_element(By.XPATH, "//input[@id='user-message']")
    print("Located by relative XPath:", rel_xpath.get_attribute("id"))

    css_id = driver.find_element(By.CSS_SELECTOR, "#user-message")
    css_attr = driver.find_element(By.CSS_SELECTOR, "[name='optradio']")
    css_child = driver.find_element(By.CSS_SELECTOR, "div > input")
    print("CSS selectors found:", css_id.get_attribute("id"), css_attr.get_attribute("name"), css_child.get_attribute("id"))

    # Task 2: Checkbox demo using XPath text and contains
    driver.get("https://www.lambdatest.com/selenium-playground/checkbox-demo")
    first_label = driver.find_element(By.XPATH, "//label[text()='Option 1']")
    print("Checkbox label found:", first_label.text)

    option_labels = driver.find_elements(By.XPATH, "//label[contains(text(),'Option')]")
    print("Option labels found:", [label.text for label in option_labels])

    # Task 3: Bootstrap alerts with explicit waits
    driver.get("https://www.lambdatest.com/selenium-playground/bootstrap-alerts-demo")

    start = time.time()
    driver.find_element(By.CSS_SELECTOR, "#autoclosable-btn-success").click()
    time.sleep(3)
    end = time.time()
    print("time.sleep version took:", round(end - start, 2), "seconds")

    driver.get("https://www.lambdatest.com/selenium-playground/bootstrap-alerts-demo")
    start = time.time()
    wait = WebDriverWait(driver, 10)
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#autoclosable-btn-success"))).click()
    alert = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert-success")))
    end = time.time()
    print("Explicit wait version took:", round(end - start, 2), "seconds")
    print("Alert text:", alert.text)

    # visibility_of_element_located checks whether the element is visible in the DOM.
    # element_to_be_clickable checks that it is visible, enabled, and not obscured.

    # Task 4: FluentWait for a dynamically loaded element
    driver.get("https://www.lambdatest.com/selenium-playground/jquery-download-progress-bar-demo")
    start_button = driver.find_element(By.ID, "downloadButton")
    start_button.click()

    from selenium.webdriver.support.ui import WebDriverWait as FluentWait
    fluent_wait = FluentWait(driver, 10, poll_frequency=0.5)
    fluent_wait.ignoring(NoSuchElementException)
    progress_bar = fluent_wait.until(lambda d: d.find_element(By.CSS_SELECTOR, ".progress-label"))
    print("Fluent wait found:", progress_bar.text)

    driver.quit()


if __name__ == "__main__":
    main()
