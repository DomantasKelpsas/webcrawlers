import sys
import requests
import csv
import json
from bs4 import BeautifulSoup

def parse_items():
    root = 'https://www.eniro.se/'
    page =1
    item_count=1

 
    with open("C:\\Users\\Echo\\Desktop\\Marino\\rohrbau.csv", 'a',newline='') as csvfile:
        fieldnames = ['Name', 'Email','Telefon','Web']
        writer = csv.DictWriter(csvfile,fieldnames=fieldnames,)
        writer.writeheader()

        while item_count<=128:
        
            url = root + 'metal/f%C3%B6retag/' + str(page)
            
            try:
                source_code = requests.get(url)
                text = source_code.text
                soup = BeautifulSoup(text)
            except Exception as e:
                    print(e)

            for link in soup.findAll('div', {'class':'css-1shebiq'}):
                itemTag = link.select_one("a[href*=firma]")
                itemUrl = root + itemTag['href']

                if itemTag:
                    try:
                        itemSoup = BeautifulSoup(requests.get(itemUrl).text)
                        parse_contacts(writer, itemSoup, page, item_count)
                    except Exception as e:
                        print(e)
           
                item_count+=1
            page+=1

def parse_contacts(writer, itemSoup, page, item_count):
    emailIsFound = False

    companyUrl = itemSoup.select_one("a[class*=css-34vsa]")['href']

    script = json.loads(itemSoup.find('script', type='application/json', id ='__NEXT_DATA__').text)
    infoObjects = script["props"]['pageProps']['company']['products']

    print('----------- '+'psl '+str(page)+' ('+str(item_count)+')' + ' -----------')

    for info in infoObjects:
        if info['name'] == 'email':
            email = info['link']
            print(email)
            emailIsFound = True
            break
    
    if(emailIsFound != True):
        parseCompanyPage(companyUrl)

    # title = contacts.find('h3', {'class':'contains-icon-name'})
    # email = contacts.select_one("a[href*=mailto]")
    # tel = contacts.find('div', {'class':'contains-icon-telefon'})
    # web = contacts.find('div', {'class':'contains-icon-homepage'})

    # if title:
    #     title = title.text.strip()
    # else: 
    #     title = 'NERASTA'
    
    # if email:
    #     email = email.text.strip()
    # else: 
    #     script = json.loads(itemSoup.find('script', type='application/ld+json').text)
    #     root = script["@graph"]
    #     for objArray in root:
    #         if "email" in objArray:
    #             email = objArray["email"]
    #             print(email)
    #             break

    # if not email:
    #         email = 'NERASTA'        

    # if tel:
    #     tel = tel.find('span').text.strip()
    # else: 
    #     tel = 'NERASTA'

    # if web:
    #     web = web.find('a').text.strip()
    # else: 
    #     web = 'NERASTA'

    # print('----------- '+'psl '+str(page)+' ('+str(item_count)+')' + ' -----------')              
    # print(title)
    # print(web)
    # print(tel)
    # print(email)

    # write_to_csv(writer, title, web, tel, email)
   
def parseCompanyPage(companyUrl):
    
    contact_page = companyUrl + '/contact' 
    contact_us_page = companyUrl + '/contact-us' 
    kontakt_page = companyUrl + '/kontakt'
    kontak_oss_page = companyUrl + '/kontakt-oss'

    con_page_list = [contact_page,contact_us_page,kontakt_page,kontak_oss_page]

    for contactPage in con_page_list:
        try:
            companySoup = BeautifulSoup(requests.get(contactPage).text)

            for a in companySoup.findAll('a'):
                print(a)

        except Exception as e:
            print(e)


def write_to_csv(writer, title, web, tel, email):

    try:
        writer.writerow({'Name':title.encode('utf-8').decode('utf-8'), 'Email': email,'Telefon': tel,'Web':web})                                 
                    
    except Exception as e:
        print(e)

parse_items()
