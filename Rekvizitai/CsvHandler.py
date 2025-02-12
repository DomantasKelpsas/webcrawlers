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
            
            with csvfile:
                fieldnames = ['CompanyName', 'Address', 'phoneNumber1', 'phoneNumber2', 'phoneNumber3', 'employeeCount', 'revenue', 'director', 'companyPage']
                writer = csv.DictWriter(csvfile,fieldnames=fieldnames,)
                # writer.writeheader()
                for company in rekvizitai:
                    writer.writerow({'CompanyName':company.companyName, 'Address':company.address,
                                     'phoneNumber1':company.phoneNumber1, 'phoneNumber2':company.phoneNumber2, 'phoneNumber3':company.phoneNumber3,
                                     'employeeCount':company.employeeCount,
                                     'revenue':company.revenue, 
                                     'director':company.director, 'companyPage':company.companyPage,
                                     })                                 
                        
        except Exception as e:
            print(e)
        
        finally:
            csvfile.close()