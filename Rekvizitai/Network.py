from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
from selenium.webdriver.chrome.service import Service
import Arguments

def getRandomWebDriver(service: Service):
    ua = UserAgent()
    random_user_agent = ua.random

    # Configure Chrome options
    chrome_options = Options()
    chrome_options.add_argument(f"user-agent={random_user_agent}")

    # Initialize the driver
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def getDefaultWebDriver():
    chrome_options = Options()
    service = Service(Arguments.PATH_WEB_DRIVER)
    return webdriver.Chrome(service=service, options=chrome_options)
