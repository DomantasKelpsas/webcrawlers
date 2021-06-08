import sys
import requests
import csv
import json
from bs4 import BeautifulSoup


def trade_spider(max_pages):
    page =1
    item_count=1
    sk=1  
   
    with open('tlf.csv', 'w',newline='') as csvfile:
        fieldnames = ['Email']
        writer = csv.DictWriter(csvfile,fieldnames=fieldnames,)
        writer.writeheader()
        print(sys.stdout.encoding)
        while page<=10:
        
            url = 'https://www.detelefoongids.nl/bouw/4-1/?page=' + str(page)
            
            source_code= requests.get(url)
            text = source_code.text
            soup = BeautifulSoup(text)

            for link in soup.findAll('div', {'class':'business-card__metadata--header'}):
           
                
                addr = link.find('a')['href']
                #print(addr)


                source_code_single= requests.get(addr)
                text_single = source_code_single.text
                soup_single = BeautifulSoup(text_single)

                for em in soup_single.find('script', {'data-reactid':'26'}).text.split('"'):
                    if '@' in em:
                        em = em.strip()
                        if len(em)<40:
                            print(em)
                            try:
                                writer.writerow({'Email': em})                                 
                                           
                            except Exception as e:
                                {}
                    
                            sk+=1
                  
                    item_count+=1      


                #script = soup_single.find('script', {'data-reactid':'26'}).text.split('data=')[1]
                #script = script[:-1]
                #js = json.loads(script)
                #print([d.get('email') for d in js['window.__data=']['reduxAsyncConnect']['detailApi']['details']['email'] if d.get('email')])

                #em = soup_single.find('span',{'class':'wordBreak'})

                #if em:
                #    em = em.text
                #    if '@' in em:
                #        print(em)
                            
                #        try:
                #            writer.writerow({'Nr':sk,'Email': em,'Web':href})                                 
                                           
                #        except Exception as e:
                #            {}
                    
                #        sk+=1
                  
                #item_count+=1                                             
               
            page+=1                              
trade_spider(1)

