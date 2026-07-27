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
    driver.get('https://www.lambdatest.com/selenium-playground/simple-form-demo')
    wait = WebDriverWait(driver, 20)
    input_el = wait.until(EC.presence_of_element_located((By.ID, 'user-message')))
    print('input_html=', input_el.get_attribute('outerHTML'))
    btn = wait.until(EC.presence_of_element_located((By.ID, 'showInput')))
    print('button_html=', btn.get_attribute('outerHTML'))
    print('button_text=', btn.text)
    print('page_title=', driver.title)
    print('body_snip=', driver.find_element(By.TAG_NAME, 'body').text[:1000])
    print('onclick=', btn.get_attribute('onclick'))
    driver.execute_script("document.getElementById('user-message').value='Hello'; document.getElementById('showInput').click();")
    import time
    time.sleep(3)
    try:
        result = driver.find_element(By.ID, 'message')
        print('result_html=', result.get_attribute('outerHTML'))
        print('result_text=', repr(result.text))
    except Exception as e:
        print('result_error=', type(e).__name__, e)
finally:
    driver.quit()
