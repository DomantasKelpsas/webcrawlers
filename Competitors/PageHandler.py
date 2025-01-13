from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class PageHandler:
    def handleCookies(driver: webdriver.Chrome):
        WebDriverWait(driver, 20).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
        )

        # Handle cookies popup
        cookiesButtonTextList = ['accept', 'agree', 'allow']
        cookiesButtonType = ['//button', '//a', '//div']
        ignoreCaseRule = "\'ABCDEFGHIJKLMNOPQRSTUVWXYZ\', \'abcdefghijklmnopqrstuvwxyz\'"

        maxCookiesButtonReries = len(cookiesButtonType)
        cookiesButtonReries = 0
        cookiesButtonRule = []
        
        for buttonType in cookiesButtonType:
            ruleRow = f'{buttonType}['
            for buttonText in cookiesButtonTextList:
                ruleRow += f'contains(translate(., {ignoreCaseRule}), \'{buttonText} \') or translate(text(), {ignoreCaseRule})=\'{buttonText}\' or '
            ruleRow = ruleRow[:-4] + "]"
            cookiesButtonRule.append(ruleRow)
            
        while cookiesButtonReries < maxCookiesButtonReries:
            try:
                cookies_button = WebDriverWait(driver, 1).until(
                    EC.element_to_be_clickable((By.XPATH, cookiesButtonRule[cookiesButtonReries]))
                )
                cookies_button.click()
                time.sleep(1)
                break
            except Exception:
                cookiesButtonReries += 1
                print(f"Attempt {cookiesButtonReries}: Cookies button not found. Retrying...")

    
    def scrollToBottom(driver: webdriver.Chrome):
         # Scroll the page to ensure full rendering
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
