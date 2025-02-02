from selenium import webdriver
from Models import Doctor
from Models import Service
from Models import Procedure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from Utils import Utils

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
            procedure_category_elements = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, '//h3[contains(@class, "ui-accordion-header")]')))
            
            for procedure_category_element in procedure_category_elements:
                driver.execute_script("arguments[0].scrollIntoView(true);", procedure_category_element)  # Scroll to element
                procedure_category_element.click()  # Click on the element

            
            procedures: list[Procedure] = []
            procedures_elements = driver.find_elements(By.XPATH, '//span[contains(@class, "kainos_proceduros_pavadinimas_fsdaysdguas__pavadinimas")]')

            testIterations = 2
            iterations = 0
           
            for procedure_element in procedures_elements:
                procedure_element.click()
                time.sleep(1)

                services: list[Service] = []
                procedureName = procedure_element.text

                service_elements = driver.find_elements(By.XPATH, '//div[contains(@class, "kainorastis-block__child") and contains(@class, "active")]//div[contains(@class, "kaina-line")]')
                serviceTableTitleFields = [element.text.strip() for element in service_elements[0].find_elements(By.XPATH,'.//div[contains(@class, "table-first-line-ins")]')]

                for service_element in service_elements[1:]:
                    serviceName = service_element.find_element(By.XPATH, './/div[contains(@class, "table-first-line-ins")]').text.strip()

                    servicePrice1Fields = service_element.find_element(By.XPATH, './/div[contains(@class, "table-second-line") and not(contains(@class, "second-add"))]//div[contains(@class, "kaina-price-center")]').text.strip().split("\n")
                    servicePrice1 = servicePrice1Fields[0]
                    serviceDiscount1 = Utils.safe_get(servicePrice1Fields,1)
                    if serviceDiscount1:
                        servicePrice1+=f' / {serviceDiscount1}*'

                    try:
                        servicePrice2Fields = service_element.find_element(By.XPATH, './/div[contains(@class, "table-second-line") and contains(@class, "second-add")]//div[contains(@class, "kaina-price-center")]').text.strip().split("\n")
                        servicePrice2 = servicePrice2Fields[0]
                        serviceDiscount2 = Utils.safe_get(servicePrice2Fields,1)
                        if serviceDiscount2:
                            servicePrice2+=f' / {serviceDiscount2}*'
                    except:
                        servicePrice2 = ""

                    service = Service(serviceName, servicePrice1, servicePrice2)
                    services.append(service)

                procedure = Procedure(procedureName, serviceTableTitleFields, services)
                procedures.append(procedure)

                print("Procedures:", procedures)
               
            return procedures
        except Exception as e:
            print(e)