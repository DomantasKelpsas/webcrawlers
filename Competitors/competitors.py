from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from dataclasses import dataclass
import datetime
import time
import csv
import google.generativeai as genai
import base64
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Competitor import Competitor
from PdfHandler import PdfHandler
from GeminiModel import GeminiModel
from CsvHandler import CsvHandler

def main():
    # Set up Chrome options
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Run in headless mode
    # chrome_options.add_argument("--window-size=1920,1080")  # Set window size

    # Specify the path to the ChromeDriver
    driver_path = "E:\\Users\\Echo\\Documents\\Python\\chromedriver.exe"

    # Initialize the WebDriver
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        competitors = [
            Competitor(name="teltonika", url= "https://teltonika-iot-group.com"),
            # Competitor(name="revolut", url= "https://www.revolut.com/en-LT/news/")
        ]

        geminiModel = GeminiModel.initGeminiModel()
        
        # Open the target website
        for competitor in competitors:
            driver.get(competitor.url)

            PdfHandler.save_webpage_as_pdf(driver, competitor)
            # competitorData = scrapeText(driver)
            # foramttedompetitorData = getGeminiQuery(model = geminiModel, competitorData = competitorData)
            # writeToCSV(competitor.name, foramttedompetitorData)


    finally:
        # Close the browser
        driver.quit()

def scrapeText(driver: webdriver):
    pageText = driver.find_element("tag name", "body").text.replace('\n', ' ').replace('\r', ' ')
    print(pageText)

    return pageText
    
main()

