"""
Selenium Architecture Notes:
- WebDriver: The core browser automation interface that sends commands to the browser and receives responses.
- Selenium Grid: A server-based solution that allows tests to run in parallel across different machines and browser combinations.
- Selenium IDE: A record-and-playback tool used to generate simple automation scripts and test flows quickly.
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


def main():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Implicit wait is set globally here for simplicity, but it is generally considered a bad practice
    # because it can slow down tests and make timing behavior less explicit than using explicit waits.
    driver.implicitly_wait(10)

    driver.get("https://www.lambdatest.com/selenium-playground/")
    print("Page title:", driver.title)
    driver.quit()


if __name__ == "__main__":
    main()
