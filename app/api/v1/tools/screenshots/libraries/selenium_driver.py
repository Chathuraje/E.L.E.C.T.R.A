
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait


async def setup_selenium_driver(url):
    options = webdriver.ChromeOptions()
    options.add_argument("--log-level=3")
    options.headless = True
    options.enable_mobile = False
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 10)
    driver.get(url)

    return driver, wait