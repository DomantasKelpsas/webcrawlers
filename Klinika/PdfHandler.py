from selenium import webdriver
from selenium.webdriver.common.by import By
import datetime
import time
import base64
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Section import Section
import Arguments

class PdfHandler: 
    def save_webpage_as_pdf(driver: webdriver.Chrome,  competitor: Section):

        try:
            # Wait for the page to load (optional, adjust as needed)

            currentDate = datetime.datetime.now().strftime('%Y%m%dT%H%M%S')
            pdf_path = f"{Arguments.PATH_SCREENSHOT}{competitor.name}_screenshot_{currentDate}.pdf"

            pdf_base64 = driver.print_page()

            # Decode the Base64 content into binary data
            pdf_binary = base64.b64decode(pdf_base64)

            # Save the binary data to a PDF file
            with open(pdf_path, 'wb') as f:
                f.write(pdf_binary)

            print(f"Saved webpage to PDF: {pdf_path}")
        except Exception as e:
            print(e)