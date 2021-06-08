import sys
import requests
import csv
from bs4 import BeautifulSoup


def trade_spider(max_pages):
    page =0
    item_count=1
    sk=1  
   
    with open('svetsning.csv', 'w',newline='') as csvfile:
        fieldnames = ['Email','Web']
        writer = csv.DictWriter(csvfile,fieldnames=fieldnames,)
        writer.writeheader()
        print(sys.stdout.encoding)
        while page<=10:
        
            url = 'https://www.riksdelen.se/sok/?q=svetsning&loc=&p=' + str(page)
            
            source_code= requests.get(url)
            text = source_code.text
            soup = BeautifulSoup(text)

            for link in soup.findAll('div', {'class':'Item'}):
           
                
                href = link.find('a')['href']
                addr = 'https://www.riksdelen.se' + href
                print(item_count)

                source_code_single= requests.get(addr)
                text_single = source_code_single.text
                soup_single = BeautifulSoup(text_single)

                em = soup_single.find('a',{'class':'solid Email'})

                if em:
                    em = em.text
                    if '@' in em:
                        print(em)
                            
                        try:
                            writer.writerow({'Email': em,'Web':addr})                                 
                                           
                        except Exception as e:
                            {}
                    
                        sk+=1
                  
                item_count+=1

              
               

              
            page+=1                              
trade_spider(1)

