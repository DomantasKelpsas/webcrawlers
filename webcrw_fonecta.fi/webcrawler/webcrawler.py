import sys
import requests
import csv
from bs4 import BeautifulSoup


def trade_spider(max_pages):
    page =1
    item_count=1
    sk=1  
   
    with open('fonecta.csv', 'w',newline='') as csvfile:
        fieldnames = ['Nr','Email','Web']
        writer = csv.DictWriter(csvfile,fieldnames=fieldnames,)
        writer.writeheader()
        print(sys.stdout.encoding)
        while item_count<=176:
            
        
            url = 'https://www.fonecta.fi/haku/rakennustelineet?page=' + str(page)
            
            source_code= requests.get(url)
            text = source_code.text
            soup = BeautifulSoup(text)

            for link in soup.findAll('div', {'class':'resultItem'}):
           
                
                href = link.find('a', {'class':'resultItemLink resultItemName'})['href']
                addr = 'https://www.fonecta.fi' + href 


                source_code_single= requests.get(addr)
                text_single = source_code_single.text
                soup_single = BeautifulSoup(text_single)

                em = soup_single.find('span',{'class':'wordBreak'})

                if em:
                    em = em.text
                    if '@' in em:
                        print(em)
                            
                        try:
                            writer.writerow({'Nr':sk,'Email': em,'Web':href})                                 
                                          
                        except Exception as e:
                            {}
                    
                        sk+=1
                  
                item_count+=1

              
               

                
                #get_single_data(href)
                #source_code_single= requests.get(href)
                #text_single = source_code_single.text
                #soup_single = BeautifulSoup(text_single)

                #print(text_single)
                                          
                #for telefon in soup.findall('span',{'data-role':'telefonnummer'}):
                #    print(telefon.text.strip())
                #    tel = telefon.text.strip()
                #    if not tel.strip(): 
                #        break

                #for email in soup.findall('a',{'property':'email'}):
                #    print(email.text.strip())
                #    em = email.text.strip()
                #    if not em.strip(): 
                #        break
                #for address in soup.findall('address'):                  
                #    adr=address.text.strip()
                #    adr=adr.replace('\n',' ').replace('\r','')
                #    print(adr)
                #    #if not adr.strip(): 
                #    break
                #try:

                #    writer.writerow({'Nr':sk,'Name':title.encode('utf-8').decode('utf-8'),'Address':adr, 'Email': em,'Telefon': tel,'Web':href})                                 
                #    sk+=1
                #except exception as e:
                #    {}

            #sk+=1  
            page+=1                              
trade_spider(1)

