import csv
import Arguments
from Utils import Utils
from Models import Company

class CsvHandler:
    print()
    def writeRekvizitaiToCSV(sectionName: str, rekvizitai: list[Company]):
        csvfile = None  

        try:
            csvfile = open(f'{Arguments.PATH_CSV}Rekvizitai_{sectionName}.csv', 'a',newline='',encoding='utf-8-sig')
            fieldnames = ['CompanyName', 'phoneNumber1', 'phoneNumber2', 'phoneNumber3', 'employeeCount', 'revenue', 'profit', 'director', 'companyPage', 'companyAge', 'Address', 'Description']
            custom_headers = ['Įmonės pavadinimas', 'Mob. telefonas', 'Telefonas', 'Buh. telefonas', 'Darbuotojų skaičius', 'Pardavimo pajamos', 'Grynasis pelnas', 'Vadovas', 'Tinklalapis', 'Įmonės amžius', 'Adresas','Apie']
            
            with csvfile:
                writer = csv.DictWriter(csvfile,fieldnames=fieldnames,)
                writer.writerow(dict(zip(fieldnames, custom_headers)))
                for company in rekvizitai:
                    writer.writerow({'CompanyName':company.companyName,
                                     'phoneNumber1':company.phoneNumber1, 'phoneNumber2':company.phoneNumber2, 'phoneNumber3':company.phoneNumber3,
                                     'employeeCount':company.employeeCount,
                                     'revenue':company.revenue, 'profit':company.profit, 
                                     'director':company.director, 'companyPage':company.companyPage, 'companyAge':company.companyAge, 'Address':company.address, 'Description':company.companyDescription
                                     })                                 
                        
        except Exception as e:
            print(e)
        
        finally:
            csvfile.close()