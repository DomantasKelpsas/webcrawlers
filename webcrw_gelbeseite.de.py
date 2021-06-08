import sys
import requests
import csv
from bs4 import BeautifulSoup


def trade_spider(max_pages):
    page =1
    item_count=1
 
   
    with open("C:\\Users\\Echo\\Desktop\\Marino\\schiffbau.csv", 'w',newline='') as csvfile:
        fieldnames = ['Name', 'Email','Telefon','Web']
        writer = csv.DictWriter(csvfile,fieldnames=fieldnames,)
        writer.writeheader()
        print(sys.stdout.encoding)
        while item_count<=242:
        
            url = 'https://www.gelbeseiten.de/Suche/schiffbau%20lackieren/Bundesweit/Seite-' + str(page)
            
            source_code= requests.get(url)
            text = source_code.text
            soup = BeautifulSoup(text)

            for link in soup.findAll('article', {'class':'mod-Treffer'}):
                                                                                        
                em = link.select_one("a[href*=mailto]")
                                      
                if em:

                    em = em['href'].split(':')[1].split('?')[0]

                    tel = link.find('p', {'class':'mod-AdresseKompakt__phoneNumber'})
                    web = link.find('a', {'class':'contains-icon-homepage gs-btn'})
                    if tel:
                        tel = tel.text
                    else:
                        tel = 'none'
                    if web:
                        web = web['href']
                    else:
                        web = 'none'

                    title =link.find('h2').text
                    href =link.find('a')['href']


                    print('----------- '+'psl '+str(page)+' ('+str(item_count)+')' + ' -----------')              
                    print(title)
                    print(web)
                    print(tel)
                    print(em)                   

                    try:
                        writer.writerow({'Name':title.encode('utf-8').decode('utf-8'), 'Email': em,'Telefon': tel,'Web':web})                                 
                                           
                    except Exception as e:
                        print(e)
                                      
                item_count+=1

                
             
            page+=1                              
trade_spider(1)

