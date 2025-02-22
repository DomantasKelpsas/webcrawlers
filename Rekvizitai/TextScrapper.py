from selenium import webdriver
from Models import Section
from Models import Company
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from Utils import Utils
from PageHandler import PageHandler
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import Arguments
import Network
import requests
from PIL import Image
import pytesseract
from io import BytesIO
import cv2
import re
import numpy as np
import random
from GeminiModel import GeminiModel
import google.generativeai as genai

class TextScrapper:
    def imageScrapper(imageUrl):
        pytesseract.pytesseract.tesseract_cmd = Arguments.PATH_TESSERACT_OCR
        extracted_text = ""
       
        try:
            response = requests.get(imageUrl)
            if response.status_code == 200:
                gif = Image.open(BytesIO(response.content))
                gif.seek(0)
                image = cv2.cvtColor(np.array(gif.convert('RGB')), cv2.COLOR_RGB2BGR)
                
                padding = 20
                image_padded = cv2.copyMakeBorder(image, padding, padding, padding, padding,
                                  cv2.BORDER_CONSTANT, value=[255, 255, 255])

                # Convert image to grayscale for better OCR accuracy
                gray = cv2.cvtColor(image_padded, cv2.COLOR_BGR2GRAY)

                img_resized = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
                custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789+'  # OCR Engine Mode 3, Page Segmentation Mode 6
                extracted_text = pytesseract.image_to_string(img_resized, config=custom_config)

        except Exception as e:
            print(f"Error: {e}")
        finally:
            return extracted_text.strip()
        
    def getMaxPage(driver: webdriver.Chrome) -> int:
        maxPage = 1
        pagingItems = Utils.safeGetElements(driver,'.//ul[@class="pagination"]/li[@class="page-item numbers"]')
        try:
            maxPage = Utils.getIntFromText(pagingItems[-1].text)
        finally:
            return maxPage
        
    def scrapeCompanyAboutPage(driver: webdriver.Chrome, url:str):
        driver.get(url)
        time.sleep(2)
        
    def parseCompanyDetails(geminiModel: genai.GenerativeModel, companyDetails: str):
        GeminiModel.getGeminiQuery(geminiModel, companyDetails)

    def scrapeCompany(mainDriver: webdriver.Chrome, section: Section) -> list[Company]:
        geminiModel = GeminiModel.initGeminiModel(apiKey = Arguments.GEMINI_API_KEY)
        service = Service(Arguments.PATH_WEB_DRIVER)
        itemDriver = None
        itemAboutPageDriver = Network.getDefaultWebDriver()
        rekvizitaiData:list[Company] = []

        try:
            mainDriver.get(section.url)
            PageHandler.handleCookies(mainDriver)
            maxPage = TextScrapper.getMaxPage(mainDriver)
            
            for pageNumber in range(maxPage):   
                mainDriver.get(section.url + str(pageNumber + 1))
                PageHandler.scrollToBottom(mainDriver)
                
                if pageNumber % 5 == 0:
                    if itemDriver:
                        itemDriver.close()
                    itemDriver = Network.getRandomWebDriver(service)
             
                companies = mainDriver.find_elements(By.XPATH, '//div[contains(@class, "company")]//div[contains(concat(" ", normalize-space(@class), " "), " company-info ")]')
                for company in companies:
                    try:
                        titleElement = company.find_element(By.XPATH, './/a[contains(@class, "company-title")]')
                        companyName = titleElement.text
                        companyUrl = titleElement.get_attribute("href")
                        time.sleep(random.uniform(1, 5))
                        itemDriver.get(companyUrl)
                        
                        directorElement = Utils.safeGetElement(itemDriver,'//tr[td[@class="name" and contains(text(), "Vadovas")]]/td[contains(@class,"value")]')
                        if(directorElement):
                            directorStringWords = Utils.getWordsFromText(directorElement.text)
                            if len(directorStringWords) >= 2:
                                director = f'{directorStringWords[0]} {directorStringWords[1]}'
                            else:
                                director = ""
                        else:
                            director = ""
                            
                        addressElement = Utils.safeGetElement(itemDriver,'//tr[td[@class="name" and contains(text(), "Adresas")]]/td[contains(@class,"value")]')
                        if(addressElement):
                            address = addressElement.text
                        else:
                            address = ""
                            
                        companyPageElement = Utils.safeGetElement(itemDriver,'//tr[td[@class="name" and contains(text(), "Tinklalapis")]]/td[contains(@class,"value")]/a')
                        if(companyPageElement):
                            companyPage = companyPageElement.text
                        else:
                            companyPage = ""
                        
                        phoneNumberElement = Utils.safeGetElement(itemDriver,'//tr[td[@class="name" and contains(text(), "Mobilus telefonas")]]/td[contains(@class,"value")]/img')
                        if(phoneNumberElement):
                            phoneNumber1 = TextScrapper.imageScrapper(phoneNumberElement.get_attribute("src"))
                        else:
                            phoneNumber1 = ""
                            
                        phoneNumberElement = Utils.safeGetElement(itemDriver,'//tr[td[@class="name" and contains(text(), "Telefonas")]]/td[contains(@class,"value")]/img')
                        if(phoneNumberElement):
                            phoneNumber2 = TextScrapper.imageScrapper(phoneNumberElement.get_attribute("src"))
                        else:
                            phoneNumber2 = ""
                            
                        phoneNumberElement = Utils.safeGetElement(itemDriver,'//tr[td[@class="name" and contains(text(), "Buhalterijos telefonas")]]/td[contains(@class,"value")]/img')
                        if(phoneNumberElement):
                            phoneNumber3 = TextScrapper.imageScrapper(phoneNumberElement.get_attribute("src"))
                        else:
                            phoneNumber3 = ""

                        employeeCountElement = Utils.safeGetElement(itemDriver,'//tr[td[@class="name" and contains(text(), "Darbuotojai")]]/td[contains(@class,"value")]')
                        if(employeeCountElement):
                            employeeCount = Utils.getIntFromText(employeeCountElement.text)
                        else:
                            employeeCount = 0
                        
                        revenueElement = Utils.safeGetElement(itemDriver,'//tr[td[@class="name" and contains(text(), "Pardavimo pajamos")]]/td[contains(@class,"value")]')
                        if(revenueElement):
                            revenue = Utils.getFloatFromText(revenueElement.text)
                        else:
                            revenue = float(0)
                            
                        profitElement = Utils.safeGetElement(itemDriver,'//tr[td[@class="name" and contains(text(), "Grynasis pelnas")]]/td[contains(@class,"value")]')
                        if(profitElement):
                            profit = Utils.getFloatFromText(profitElement.text)
                        else:
                            profit = float(0)
                            
                        companyAgeElement = Utils.safeGetElement(itemDriver,'//tr[td[@class="name" and contains(text(), "Įmonės amžius")]]/td[contains(@class,"value")]')
                        if(companyAgeElement):
                            companyAge = companyAgeElement.text
                        else:
                            companyAge = ""
                            
                        companyDescriptionElement = Utils.safeGetElement(itemDriver,'//div[@class="block companyDescription"]/div[@class="description"]')
                        if(companyDescriptionElement):
                            companyDescription = companyDescriptionElement.text
                        else:
                            companyDescription = ""
                            
                        # if companyPage: 
                        #     TextScrapper.scrapeCompanyAboutPage(itemAboutPageDriver, companyPage)
                        
                        companyDescription = TextScrapper.parseCompanyDetails(geminiModel, companyDescription)

                        companyData = Company(companyName, address, phoneNumber1, phoneNumber2, phoneNumber3, employeeCount, revenue, profit, director, companyPage, companyAge, companyDescription)
                        rekvizitaiData.append(companyData)
                    except Exception as e:
                        print(e)
        except Exception as e:
            print(e)
        finally:
            itemDriver.quit()
            return rekvizitaiData