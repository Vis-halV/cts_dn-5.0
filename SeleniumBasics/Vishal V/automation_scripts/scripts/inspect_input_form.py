from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
driver = webdriver.Chrome(options=options)
try:
    driver.get('https://www.lambdatest.com/selenium-playground/input-form-demo')
    import time
    time.sleep(3)
    elements = driver.find_elements(By.CSS_SELECTOR, 'input, textarea, button')
    for element in elements:
        if element.get_attribute('id') or element.get_attribute('name') or element.get_attribute('placeholder'):
            print(element.tag_name, 'id=', element.get_attribute('id'), 'name=', element.get_attribute('name'), 'placeholder=', element.get_attribute('placeholder'), 'type=', element.get_attribute('type'))
finally:
    driver.quit()
