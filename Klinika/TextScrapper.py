from selenium import webdriver
from Models import Doctor
from Models import Price
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class TextScrapper:
    def scrapeDoctors(driver: webdriver):
        doctors = []
        doctor_elements = driver.find_elements(By.XPATH, '//div[contains(@class, "col-md-4") and contains(@class, "delay_this_item")]')
        for doctor_element in doctor_elements:
            name = doctor_element.find_element(By.XPATH, './/h3/a').text
            postion = doctor_element.find_element(By.XPATH, './/h4').text
            url = doctor_element.find_element(By.XPATH, './/h3/a').get_attribute('href')
            doctor = Doctor(name, postion, url)
            doctors.append(doctor)
            print("Doctors:", doctors)

        return doctors
    
    def scrapePrices(driver: webdriver):
        try:
            dropdowns = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, '//h3[contains(@class, "ui-accordion-header")]')))
            
            for dropdown in dropdowns:
                driver.execute_script("arguments[0].scrollIntoView(true);", dropdown)  # Scroll to element
                dropdown.click()  # Click on the element

            
            prices = []
            procedures_elements = driver.find_elements(By.XPATH, '//span[contains(@class, "kainos_proceduros_pavadinimas_fsdaysdguas__pavadinimas")]')

            for procedure_element in procedures_elements:
                procedure_element.click()
                time.sleep(2)
                procedureName = procedure_element.text

                service_elements = driver.find_elements(By.XPATH, '//div[contains(@class, "kainorastis-block__child") and contains(@class, "active")]//div[contains(@class, "kaina-line")]')
                for service_element in service_elements:
                    serviceName = service_element.find_element(By.XPATH, './/div[contains(@class, "table-first-line-ins")]').text
                    servicePrice = service_element.find_element(By.XPATH, './/div[contains(@class, "kaina-price-center")]').text
                    price = Price(f'{procedureName} - {serviceName}', servicePrice)
                    prices.append(price)

                print("Prices:", prices)

            return prices
        except Exception as e:
            print(e)