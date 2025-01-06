from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from dataclasses import dataclass
import datetime
import csv
from PIL import Image
import google.generativeai as genai

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
            Competitor(name="revolut", url= "https://www.revolut.com/en-LT/news/")
        ]

        geminiModel = initGeminiModel()
        
        # Open the target website
        for competitor in competitors:
            driver.get(competitor.url)

            # captureWebScreen(driver, competitor)
            competitorData = scrapeText(driver)
            foramttedompetitorData = getGeminiQuery(model = geminiModel, competitorData = competitorData)
            writeToCSV(competitor.name, foramttedompetitorData)


    finally:
        # Close the browser
        driver.quit()

def captureWebScreen(driver: webdriver, competitor: Competitor):
    # Set the window size to the total height of the page
    total_height = driver.execute_script("return document.body.scrollHeight")
    driver.set_window_size(1920, total_height)
    currentDate = datetime.datetime.now().strftime('%Y%m%dT%H%M%S')

    # Take a screenshot of the full page
    screenshot_path = f"E:\\Users\\Echo\\Documents\\Python\\Competitors\\screenshots\\{competitor.name}_screenshot_{currentDate}.png"
    driver.save_screenshot(screenshot_path)
    print(f"Screenshot saved at {screenshot_path}")

def scrapeText(driver: webdriver):
    pageText = driver.find_element("tag name", "body").text.replace('\n', ' ').replace('\r', ' ')
    print(pageText)

    return pageText

def captureWebScreen2(driver: webdriver, competitor: Competitor):
    viewport_height = driver.execute_script("return window.innerHeight")
    scroll_height = driver.execute_script("return document.body.scrollHeight")
    driver.set_window_size(1920, viewport_height)

    # Take screenshots while scrolling
    screenshots = []
    for offset in range(0, scroll_height, viewport_height):
        driver.execute_script(f"window.scrollTo(0, {offset})")
        screenshot_path = f"screenshot_{offset}.png"
        driver.save_screenshot(screenshot_path)
        screenshots.append(screenshot_path)

    # Stitch screenshots together
    images = [Image.open(s) for s in screenshots]
    total_height = sum(img.height for img in images)
    stitched_image = Image.new("RGB", (images[0].width, total_height))

    y_offset = 0
    for img in images:
        stitched_image.paste(img, (0, y_offset))
        y_offset += img.height

    currentDate = datetime.datetime.now().strftime('%Y%m%dT%H%M%S')

    # Take a screenshot of the full page
    screenshot_path = f"E:\\Users\\Echo\\Documents\\Python\\screenshots\\{competitor.name}_screenshot_{currentDate}.png"
    print(f"Screenshot saved at {screenshot_path}")
    stitched_image.save(screenshot_path)

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
    

main()

