import os
import pytest
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium import webdriver


@pytest.fixture(scope='function')
def driver(request):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')

    chrome_driver_path = r'C:\Users\visha\chromedriver-win64\chromedriver.exe'
    if os.path.exists(chrome_driver_path):
        driver_instance = webdriver.Chrome(service=Service(chrome_driver_path), options=options)
    else:
        driver_instance = webdriver.Chrome(options=options)

    driver_instance.implicitly_wait(5)
    yield driver_instance
    driver_instance.quit()


@pytest.fixture(scope='session')
def base_url():
    return 'https://www.lambdatest.com/selenium-playground/'
