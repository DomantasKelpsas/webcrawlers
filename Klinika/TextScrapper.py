from selenium import webdriver
from Models import Doctor
from Models import Service
from Models import Procedure
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
                if(iterations < testIterations):
                    procedure_element.click()
                    time.sleep(1)

                    services: list[Service] = []
                    procedureName = procedure_element.text

                    service_elements = driver.find_elements(By.XPATH, '//div[contains(@class, "kainorastis-block__child") and contains(@class, "active")]//div[contains(@class, "kaina-line")]')
                    serviceTableTitleFields = [element.text.strip() for element in service_elements[0].find_elements(By.XPATH,'.//div[contains(@class, "table-first-line-ins")]')]

                    # try:
                    #     element = service_elements[0].find_element(By.XPATH, './/div[contains(@class, "table-first-line-ins")]')
                    #     text = element.text
                    # except:
                    #     text = ""
                    
                    # try:
                    #     element = service_elements[0].find_element(By.XPATH, './/div[contains(@class, "kaina-price-center")]')
                    #     text = element.text
                    # except:
                    #     text = ""


                    for service_element in service_elements[1:]:
                        serviceName = service_element.find_element(By.XPATH, './/div[contains(@class, "table-first-line-ins")]').text.strip()
                        servicePrice = service_element.find_element(By.XPATH, './/div[contains(@class, "kaina-price-center")]').text.strip()
                        service = Service(serviceName, servicePrice, "")
                        services.append(service)

                    procedure = Procedure(procedureName, serviceTableTitleFields, services)
                    procedures.append(procedure)

                    print("Procedures:", procedures)
                    iterations+=1
                else:
                    return procedures
            return procedures
        except Exception as e:
            print(e)