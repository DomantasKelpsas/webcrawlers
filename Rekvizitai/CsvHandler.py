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
                fieldnames = ['CompanyName', 'phoneNumber', 'employeeCount', 'revenue']
                writer = csv.DictWriter(csvfile,fieldnames=fieldnames,)
                # writer.writeheader()
                for company in rekvizitai:
                    writer.writerow({'CompanyName':company.name, 'phoneNumber':company.phoneNumber, 'employeeCount':company.employeeCount, 'revenue':company.revenue})                                 
                        
        except Exception as e:
            print(e)
        
        finally:
            csvfile.close()