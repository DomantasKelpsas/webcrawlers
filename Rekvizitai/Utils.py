import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

class Utils:
    def safe_get(lst, index):
        try:
            return lst[index]
        except IndexError:
            return ""

    def getIntFromText(floatString: str):
        numeric_value = 0
        try:
            clean_value = floatString.split('€')[0]
            clean_value = re.sub(r'[^\d,]', '', clean_value)  # Keep only digits and commas
            numeric_value = int(clean_value)
        finally:
             return numeric_value
       
    def getFloatFromText(floatString: str):
        numeric_value = float(0)
        try:
            clean_value = floatString.split('€')[0]
            clean_value = re.sub(r'[^\d,]', '', clean_value)  # Keep only digits and commas
            clean_value = clean_value.replace(',', '.')  # Replace comma with a dot (if needed)
            numeric_value = float(clean_value)
        finally:
             return numeric_value
    
    def safeGetElement(driver: webdriver.Chrome, query: str) -> WebElement:
        try:
            return driver.find_element(By.XPATH, query)
        except Exception:
            return None
        
    def getWordsFromText(text: str) -> list[str]:
        words = [""]
        try:
            words = re.split(r'[ ,!\n]+', text)
        finally:
            return words
