from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from Models import Section
from PdfHandler import PdfHandler
from CsvHandler import CsvHandler
from PageHandler import PageHandler
from TextScrapper import TextScrapper
import Arguments
import WebDataStore
import time

def main():
    # Set up Chrome options
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Run in headless mode
    # chrome_options.add_argument("--window-size=1920,1080")  # Set window size
    

    # Initialize the WebDriver
    service = Service(Arguments.PATH_WEB_DRIVER)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        sections = [
            Section(name="medicinine_iranga", url= "https://rekvizitai.vz.lt/imones/medicinine_iranga/"),           
        ]

        savedSectionData = None

        for section in sections:
            # driver.get(section.url)
            # PageHandler.handleCookies(driver)
            # PageHandler.scrollToBottom(driver)
    
            RekvizitaiData = TextScrapper.scrapeCompany(driver, section)
            # CsvHandler.writePricesToCSV(section.name, RekvizitaiData)

    finally:
        # Close the browser
        driver.quit()
    
main()