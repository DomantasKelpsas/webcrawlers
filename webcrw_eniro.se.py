import sys
import requests
import csv
from bs4 import BeautifulSoup


def trade_spider(max_pages):
    page = 1
    item_count = 1
    sk = 1  
   
    with open('metallbearbetning.csv', 'w',newline='') as csvfile:
        fieldnames = ['Email']
        writer = csv.DictWriter(csvfile,fieldnames=fieldnames,)
        writer.writeheader()
        print(sys.stdout.encoding)
        while page<=53:
        
            url = 'https://www.eniro.se/metallbearbetning/f%C3%B6retag/' + str(page)
            
            source_code= requests.get(url)
            text = source_code.text
            soup = BeautifulSoup(text)

            for link in soup.findAll('a', {'class':'homePage'}):
           
                
                addr = link['href']
                #print(addr)


                contact_page = addr + '/contact' 
                kontakt_page = addr + '/kontakt'
                kontak_oss_page = addr + '/kontakt-oss'

                con_page_list = [contact_page,kontakt_page,kontak_oss_page]

                for con_page in con_page_list:
                    try:
                        source_code_single= requests.get(con_page)
                        text_single = source_code_single.text
                        soup_single = BeautifulSoup(text_single)

                        for a in soup_single.findAll('a'):

                            #print(a.text)

                            if '@'in a.text:
                                em = a.text.strip()
                                print(em)

                                try:
                                    writer.writerow({'Email': em})                                 
                                           
                                except Exception as ex:
                                    {}



                        #if em:
                        #    em = em.text
                        #    if '@' in em:
                        #        print(em)
                            
                        #        try:
                        #            writer.writerow({'Nr':sk,'Email': em,'Web':href})                                 
                                           
                        #        except Exception as e:
                        #            {}
                    
                        #        sk+=1
                  
                        item_count+=1
                    except Exception as e:
                        {}
              
               

            page+=1                              
trade_spider(1)

