import sys
import requests
import csv
from bs4 import BeautifulSoup


def trade_spider(max_pages):
    page =1
    item_count=1
    sk=1  
   
    with open('mettalbau.csv', 'a',newline='') as csvfile:
        fieldnames = ['Email','Web']
        writer = csv.DictWriter(csvfile,fieldnames=fieldnames,)
        writer.writeheader()
        print(sys.stdout.encoding)
      
        
        url = 'https://www.foretagsfakta.se/sok/welding%20works'
            
        source_code= requests.get(url)
        text = source_code.text
        soup = BeautifulSoup(text)

        for link in soup.findAll('div', {'class':'company-details'}):
           
                
            addr = link.find('a')['href']
            

           
            source_code_single= requests.get(addr)
            text_single = source_code_single.text
            soup_single = BeautifulSoup(text_single)

            em_div = soup_single.find('div',{'class':'company-email'})

            if em_div:
                
                em = em_div.find('a').text.strip()
               
                print(em)
                            
                try:
                    writer.writerow({'Email': em,'Web':addr})                                 
                                           
                except Exception as e:
                    {}
                    
                sk+=1
                  
            item_count+=1
              
                          
                                     
trade_spider(1)

