from selenium import webdriver
from selenium.webdriver.common.by import By
import datetime
import time
import base64
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Competitor import Competitor
import Arguments

class PdfHandler: 
    def save_webpage_as_pdf(driver: webdriver.Chrome,  competitor: Competitor):

        try:
            # Wait for the page to load (optional, adjust as needed)

            currentDate = datetime.datetime.now().strftime('%Y%m%dT%H%M%S')
            pdf_path = f"{Arguments.PATH_SCREENSHOT}{competitor.name}_screenshot_{currentDate}.pdf"

            WebDriverWait(driver, 20).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )

        # Handle cookies popup
            maxCookiesButtonReries = 3
            cookiesButtonReries = 0

            cookiesButtonRule = [
                    "//button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'accept') or "
                    "contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'agree')]",
                    "//a[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'accept') or "
                    "contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'agree')]",
                    "//div[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'accept') or "
                    "contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'agree')]"
                    ]
            
            while cookiesButtonReries < maxCookiesButtonReries:
                try:
                    cookies_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, cookiesButtonRule[cookiesButtonReries]))
                    )
                    cookies_button.click()
                    time.sleep(1)
                    break
                except Exception as e:
                    cookiesButtonReries += 1
                    print(f"Attempt {cookiesButtonReries}: Cookies button not found. Retrying... ({str(e)})")

            # Scroll the page to ensure full rendering
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            pdf_base64 = driver.print_page()

            # Decode the Base64 content into binary data
            pdf_binary = base64.b64decode(pdf_base64)

            # Save the binary data to a PDF file
            with open(pdf_path, 'wb') as f:
                f.write(pdf_binary)

            print(f"Saved webpage to PDF: {pdf_path}")
        except Exception as e:
            print(e)