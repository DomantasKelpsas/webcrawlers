from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from Competitor import Competitor
from PdfHandler import PdfHandler
from GeminiModel import GeminiModel
from CsvHandler import CsvHandler
from PageHandler import PageHandler
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
        competitors = [
            Competitor(name="Teltonika", url= "https://teltonika-iot-group.com"),
            Competitor(name="Revolut", url= "https://www.revolut.com/en-LT/news/"),
            Competitor(name="Vinted", url= "https://company.vinted.com/lt/newsroom"),
            Competitor(name="KiloHealth", url= "https://kilo.health/about/"),
            Competitor(name="Bankera", url= "https://blog.bankera.com/")
        ]

        geminiModel = GeminiModel.initGeminiModel(apiKey = Arguments.GEMINI_API_KEY)

        savedCompetitorData = None

        testIterations = 0
        # Open the target website
        while testIterations < 3:
            for competitor in competitors:
                driver.get(competitor.url)
                PageHandler.handleCookies(driver)
                PageHandler.scrollToBottom(driver)
                competitorData = scrapeText(driver)
                
                try:
                    savedCompetitorData = WebDataStore.webDataStorage[competitor.name]
                except:
                    savedCompetitorData = ""

                if savedCompetitorData != competitorData:
                    print("COMPETITOR DATA: changed")
                    foramttedCompetitorData = GeminiModel.getGeminiQuery(model = geminiModel, competitorData = competitorData)
                    CsvHandler.writeToCSV(competitor.name, foramttedCompetitorData)
                    PdfHandler.save_webpage_as_pdf(driver, competitor)
                    WebDataStore.webDataStorage[competitor.name] = competitorData
                else:
                    print("COMPETITOR DATA: did NOT change")

            print("Scrapper timeout until next iteration")
            testIterations += 1
            time.sleep(30)
    finally:
        # Close the browser
        driver.quit()

def scrapeText(driver: webdriver):
    pageText = driver.find_element("tag name", "body").text.replace('\n', ' ').replace('\r', ' ')
    return pageText
    
main()