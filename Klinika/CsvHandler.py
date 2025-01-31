import csv
import Arguments
from Models import Doctor
from Models import Price

class CsvHandler:
    def writeDoctorsToCSV(sectionName: str, doctors: list[Doctor]):
        csvfile = None  

        try:
            csvfile = open(f'{Arguments.PATH_CSV}klinika_{sectionName}.csv', 'a',newline='',encoding='utf-8-sig')
            
            with csvfile:
                fieldnames = ['Name', 'Position', 'Url']
                writer = csv.DictWriter(csvfile,fieldnames=fieldnames,)
                # writer.writeheader()
                for doctor in doctors:
                    writer.writerow({'Name':doctor.name, 'Position':doctor.position, 'Url':doctor.url})                                 
                        
        except Exception as e:
            print(e)
        
        finally:
            csvfile.close()

    def writePricesToCSV(sectionName: str, prices: list[Price]):
        csvfile = None  

        try:
            csvfile = open(f'{Arguments.PATH_CSV}klinika_{sectionName}.csv', 'a',newline='',encoding='utf-8-sig')
            
            with csvfile:
                fieldnames = ['Name', 'Price']
                writer = csv.DictWriter(csvfile,fieldnames=fieldnames,)
                # writer.writeheader()
                for price in prices:
                    writer.writerow({'Name':price.name, 'Price':price.value})                                 
                        
        except Exception as e:
            print(e)
        
        finally:
            csvfile.close()