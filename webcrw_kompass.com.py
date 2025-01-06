import sys
import requests
import csv
import json
from bs4 import BeautifulSoup

def parse_items():
    page =1
    item_count=1
 
   
    with open("C:\\Users\\Echo\\Desktop\\Marino\\metals_fr.csv", 'a',newline='') as csvfile:
        fieldnames = ['Name', 'Email','Telefon','Web']
        writer = csv.DictWriter(csvfile,fieldnames=fieldnames,)
        writer.writeheader()
        
        print(sys.stdout.encoding)
        while item_count<=2397:
        
            url = 'https://fr.kompass.com/en/a/boilerwork-services/65180/page-' + str(page)
            
            try:
                source_code = requests.get(url)
                text = source_code.text
                soup = BeautifulSoup(text)
            except Exception as e:
                    print(e)

            for link in soup.findAll('article', {'class':'mod-Treffer'}):
                itemTag = link.select_one("a[href*=https]")

                if itemTag:
                    try:
                        itemSoup = BeautifulSoup(requests.get(itemTag['href']).text)
                        parse_contacts(writer, itemSoup, page, item_count)
                    except Exception as e:
                        print(e)
           
                item_count+=1
            page+=1

def parse_contacts(writer, itemSoup, page, item_count):
    contacts = itemSoup.find('section', {'id':'kontaktdaten'})

    if contacts:
        title = contacts.find('h3', {'class':'contains-icon-name'})
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
