from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
driver = webdriver.Chrome(options=options)
try:
    for message in ['Hello', 'Hello Selenium', 'Selenium Automation', '12345']:
        driver.get('https://www.lambdatest.com/selenium-playground/simple-form-demo')
        elem = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, 'user-message')))
        elem.clear()
        elem.send_keys(message)
        btn = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID, 'showInput')))
        btn.click()
        try:
            result = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'message')))
            print('message=', message, 'text=', repr(result.text), 'outer=', result.get_attribute('outerHTML')[:300])
        except Exception as e:
            print('message=', message, 'ERROR', type(e).__name__, e)
finally:
    driver.quit()
