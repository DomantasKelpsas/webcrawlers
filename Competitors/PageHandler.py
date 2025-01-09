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

        maxCookiesButtonReries = len(cookiesButtonType)
        cookiesButtonReries = 0
        cookiesButtonRule2 = []

       

        cookiesButtonRule = [
                "//button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'accept ') or "
                "contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'agree ') or "
                "contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'allow ')]",
                "//a[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'accept ') or "
                "contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'agree ') or "
                "contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'allow ')]",
                "//div[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'accept ') or "
                "contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'agree ') or "
                "contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'allow ')]"
                ]
        
        for buttonType in cookiesButtonType:
            ruleRow = f'{buttonType}['
            for buttonText in cookiesButtonTextList:
                ruleRow += f'contains(translate(., \'ABCDEFGHIJKLMNOPQRSTUVWXYZ\', \'abcdefghijklmnopqrstuvwxyz\'), \'{buttonText} \') or '
            ruleRow = ruleRow[:-4] + "]"
            cookiesButtonRule2.append(ruleRow)
            
        while cookiesButtonReries < maxCookiesButtonReries:
            try:
                cookies_button = WebDriverWait(driver, 10).until(
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
