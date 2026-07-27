from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import os


def create_driver(headless=True):
    options = Options()
    if headless:
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')

    chrome_driver_path = r'C:\Users\visha\chromedriver-win64\chromedriver.exe'
    if os.path.exists(chrome_driver_path):
        return webdriver.Chrome(service=Service(chrome_driver_path), options=options)
    return webdriver.Chrome(options=options)
