from selenium import webdriver
from Doctor import Doctor
from selenium.webdriver.common.by import By

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