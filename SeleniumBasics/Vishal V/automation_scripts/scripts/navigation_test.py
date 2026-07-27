import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


def main():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.implicitly_wait(10)

    driver.get("https://www.lambdatest.com/selenium-playground/")
    driver.find_element(By.LINK_TEXT, "Simple Form Demo").click()

    assert "simple-form-demo" in driver.current_url
    print("Navigation successful. Current URL:", driver.current_url)

    driver.back()

    driver.execute_script('window.open("https://www.google.com");')
    print("Open tabs:", driver.window_handles)
    driver.switch_to.window(driver.window_handles[1])
    print("Google tab title:", driver.title)

    driver.switch_to.window(driver.window_handles[0])
    size = driver.get_window_size()
    print("Current window size:", size)
    driver.set_window_size(1280, 800)

    # A consistent browser window size matters because responsive UI tests can behave differently
    # when the viewport changes between environments or machines.
    screenshot_path = "playground_screenshot.png"
    driver.save_screenshot(screenshot_path)
    print("Screenshot created:", os.path.exists(screenshot_path))

    driver.quit()


if __name__ == "__main__":
    main()
