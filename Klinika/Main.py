from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from Section import Section
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
            Section(name="Doctors", url= "https://lazerineklinika.lt/gydytojai/"),
        ]

        savedSectionData = None

        testIterations = 0
        # Open the target website

        for section in sections:
            driver.get(section.url)
            PageHandler.handleCookies(driver)
            PageHandler.scrollToBottom(driver)
            doctorsData = TextScrapper.scrapeDoctors(driver)
            
            # try:
            #     savedSectionData = WebDataStore.webDataStorage[section.name]
            # except:
            #     savedSectionData = ""

            # if savedSectionData != sectionData:
            #     print("SECTION DATA: changed")
            
            CsvHandler.writeDoctorsToCSV(section.name, doctorsData)
            # PdfHandler.save_webpage_as_pdf(driver, section)
            # WebDataStore.webDataStorage[section.name] = sectionData
            # else:
            #     print("SECTION DATA: did NOT change")


    finally:
        # Close the browser
        driver.quit()
    
main()