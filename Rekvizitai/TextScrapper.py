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

class TextScrapper:  
    def scrapeCompany(mainDriver: webdriver.Chrome, section: Section):
        chrome_options = Options()
        service = Service(Arguments.PATH_WEB_DRIVER)
        itemDriver = webdriver.Chrome(service=service, options=chrome_options)

        rekvizitaiData:list[Company] = []

        try:
            for pageNumber in range(5):
                mainDriver.get(section.url + str(pageNumber + 1))
                if pageNumber == 0:
                    PageHandler.handleCookies(mainDriver)

                companies = mainDriver.find_elements(By.XPATH, '//div[contains(@class, "company")]//div[contains(concat(" ", normalize-space(@class), " "), " company-info ")]')
                for company in companies:
                    try:
                        titleElement = company.find_element(By.XPATH, './/a[contains(@class, "company-title")]')
                        title = titleElement.text
                        companyUrl = titleElement.get_attribute("href")
                        itemDriver.get(companyUrl)

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

                        companyData = Company(title, "0", employeeCount, revenue)
                        rekvizitaiData.append(companyData)
                    except Exception as e:
                        print(e)
        except Exception as e:
            print(e)
        finally:
            return rekvizitaiData