import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


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


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == 'call' and report.failed:
        driver = item.funcargs.get('driver')
        if driver is not None:
            test_name = item.nodeid.replace('::', '_').replace('/', '_')
            screenshot_path = f'{test_name}_failure.png'
            driver.save_screenshot(screenshot_path)
            print(f'Failure screenshot saved: {os.path.abspath(screenshot_path)}')
