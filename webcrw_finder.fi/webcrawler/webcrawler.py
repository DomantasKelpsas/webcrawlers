#from __future__ import unicode_literals
import requests
import csv
#import unicodecsv as csv
from bs4 import BeautifulSoup

def trade_spider(max_pages):
    page = 1
    sk=1
    #tel =''
    #em=''
   
    with open('Suunnittelu-2.csv', 'a',encoding="utf-8",newline='') as csvfile:
        fieldnames = [ 'Email']
        writer = csv.DictWriter(csvfile,fieldnames=fieldnames)
        writer.writeheader()

        while page<=354:        
            url = 'https://www.finder.fi/search?what=Suunnittelu%20Ja%20Rakennus&page=' + str(page)
            source_code= requests.get(url)
            text = source_code.text
            soup = BeautifulSoup(text)
        
            for link in soup.findAll('a',{'class':'SearchResult__ProfileLink'}):               
               
                href ='https://www.finder.fi'+link.get('href').strip()
                title =link.text.strip()
              
                source_code= requests.get(href)
                text = source_code.text
                soup_single = BeautifulSoup(text)
                                        
                #for telefon in soup.findAll('a',{'class':'SearchResult__Link'}):

                #    print(telefon.text.strip())
                #    tel = telefon.text.strip()
                
                #for email in soup.findAll('a',{'property':'email'}):
                #    #print(email.text.strip())
                #    List.append(email.text.strip())
                #    em=email.text.strip()
                #    print(em)
                #for emai in List:
                #    print(email)
                
                for info_link in soup_single.findAll('a',{'class':'SearchResult__Link'}):
                #print(email)
              
                    if '@' in info_link.text:
                        email = info_link.text
                        print(email)
                        writer.writerow({'Email': email})
                        break
                sk+=1
            page+=1                              
trade_spider(1)


