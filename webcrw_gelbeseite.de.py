import sys
import requests
import csv
import json
import time
import math
from selenium import webdriver
from bs4 import BeautifulSoup

def parse_items():
    url = 'https://www.gelbeseiten.de/suche/industrie%20lackieren/bundesweit'
    soup = BeautifulSoup(url)

    page =1
    item_count=1
    max_item_count=85
    max_load_more_click_count = math.ceil((max_item_count - 50) / 10)

    python_button = None

    driver = webdriver.Chrome("C:\\Users\\Echo\\Downloads\\chromedriver")
    driver.implicitly_wait(30)
    driver.get(url)

    try:
        python_button = driver.find_element_by_id("mod-LoadMore--button")
    except Exception as e:
        print(e)

    with open("C:\\Users\\Echo\\Desktop\\Marino\\industrie-lackieren.csv", 'a',newline='') as csvfile:
        fieldnames = ['Name', 'Email','Telefon','Web']
        writer = csv.DictWriter(csvfile,fieldnames=fieldnames,)
        writer.writeheader()

        if(python_button):
            for load_more_click_count in range(max_load_more_click_count):
                try:
                    python_button.click()
                    print("load more clicked ("+ str(load_more_click_count) +" out of "+ str(max_load_more_click_count) +")")
                    time.sleep(5)
                except Exception as e:
                    print(e) 
                

        print(sys.stdout.encoding)
        
        try:
            # source_code = requests.get(driver.page_source)
            # text = source_code.text
            soup = BeautifulSoup(driver.page_source)
        except Exception as e:
                print(e)

        searchListItemLinks = soup.findAll('article', {'class':'mod-Treffer'})
        print("Articles found: " + str(len(searchListItemLinks)))

        for link in searchListItemLinks:
            itemTag = link.select_one("a[href*=https]")

            if itemTag:
                try:
                    itemSoup = BeautifulSoup(requests.get(itemTag['href']).text)
                    parse_contacts(writer, itemSoup, page, item_count)
                except Exception as e:
                    print(e)
        
            item_count+=1

def parse_contacts(writer, itemSoup, page, item_count):
    contacts = itemSoup.find('section', {'id':'kontaktdaten'})

    if contacts:
        title = contacts.find('div', {'class':'contains-icon-name'})
        email = contacts.select_one("a[href*=mailto]")
        tel = contacts.find('div', {'class':'contains-icon-telefon'})
        web = contacts.find('div', {'class':'contains-icon-homepage'})

        if title:
            title = title.text.strip()
        else: 
            title = 'NERASTA'
        
        if email:
            email = email.text.strip()
        else: 
            script = json.loads(itemSoup.find('script', type='application/ld+json').text)
            root = script["@graph"]
            for objArray in root:
                if "email" in objArray:
                    email = objArray["email"]
                    print(email)
                    break

        if not email:
             email = 'NERASTA'        

        if tel:
            tel = tel.find('span').text.strip()
        else: 
            tel = 'NERASTA'

        if web:
            web = web.find('a').text.strip()
        else: 
            web = 'NERASTA'

        print('----------- '+'psl '+str(page)+' ('+str(item_count)+')' + ' -----------')              
        print(title)
        print(web)
        print(tel)
        print(email)

        write_to_csv(writer, title, web, tel, email)
   

def write_to_csv(writer, title, web, tel, email):

    try:
        writer.writerow({'Name':title.encode('utf-8').decode('utf-8'), 'Email': email,'Telefon': tel,'Web':web})                                 
                    
    except Exception as e:
        print(e)


parse_items()
