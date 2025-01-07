from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from dataclasses import dataclass
import datetime
import time
import csv
import google.generativeai as genai
import base64
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@dataclass
class Competitor:
    name: str
    url: str

def main():
    # Set up Chrome options
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Run in headless mode
    # chrome_options.add_argument("--window-size=1920,1080")  # Set window size

    # Specify the path to the ChromeDriver
    driver_path = "E:\\Users\\Echo\\Documents\\Python\\chromedriver.exe"

    # Initialize the WebDriver
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        competitors = [
            Competitor(name="teltonika", url= "https://teltonika-iot-group.com"),
            # Competitor(name="revolut", url= "https://www.revolut.com/en-LT/news/")
        ]

        geminiModel = initGeminiModel()
        
        # Open the target website
        for competitor in competitors:
            driver.get(competitor.url)

            save_webpage_as_pdf(driver, competitor)
            # captureWebScreen2(driver, competitor)
            # competitorData = scrapeText(driver)
            # foramttedompetitorData = getGeminiQuery(model = geminiModel, competitorData = competitorData)
            # writeToCSV(competitor.name, foramttedompetitorData)


    finally:
        # Close the browser
        driver.quit()

def scrapeText(driver: webdriver):
    pageText = driver.find_element("tag name", "body").text.replace('\n', ' ').replace('\r', ' ')
    print(pageText)

    return pageText

def writeToCSV(competitorName, competitorData):
    csvfile = None  

    try:
        csvfile = open("E:\\Users\\Echo\\Documents\\Python\\Competitors\\competitors.csv", 'a',newline='')
        
        with csvfile:
            fieldnames = ['Company', 'Details']
            writer = csv.DictWriter(csvfile,fieldnames=fieldnames,)
            # writer.writeheader()
            writer.writerow({'Company':competitorName, 'Details': competitorData})                                 
                    
    except Exception as e:
        print(e)
    
    finally:
        csvfile.close()


def initGeminiModel():
    genai.configure(api_key="AIzaSyCKhoUdsFUWxA0UrjTzMgE7ALbQQakSC1g")
    return genai.GenerativeModel("gemini-1.5-flash")
    
def getGeminiQuery(model: genai.GenerativeModel, competitorData: str):

    query = (
    f'Details about company are provided in quatation marks. The text is not clean. Clean the text and make a summary from the provided text.' 
    f'If there are any news about the company, list them with exact headlines or if they dont have headlines summarize the news into headline making a list of them.'
    f'"{competitorData}"'
    )

    response = model.generate_content(query)
    print(response.text)
    return response.text

def save_webpage_as_pdf(driver: webdriver.Chrome,  competitor: Competitor):

    try:
        # Wait for the page to load (optional, adjust as needed)

        currentDate = datetime.datetime.now().strftime('%Y%m%dT%H%M%S')
        pdf_path = f"E:\\Users\\Echo\\Documents\\Python\\Competitors\\screenshots\\{competitor.name}_screenshot_{currentDate}.pdf"

        # Wait for the page to load completely
        # WebDriverWait(driver, 20).until(
        #     EC.presence_of_element_located((By.TAG_NAME, "body"))
        # )
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
    

main()

