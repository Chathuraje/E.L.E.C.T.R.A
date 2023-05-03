
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait


async def setup_selenium_driver(url):
    options = webdriver.ChromeOptions()
    options.add_argument("--log-level=3")
    options.add_argument("user-data-dir=C:\\Users\\Chath\\AppData\\Local\\Google\\Chrome Beta\\User Data\\")
    options.binary_location = "C:\\Program Files\\Google\\Chrome Beta\\Application\\chrome.exe"
    options.headless = True
    options.enable_mobile = False
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 10)
    driver.get(url)

    return driver, wait