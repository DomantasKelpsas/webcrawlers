import csv
import Arguments

class CsvHandler:
    def writeToCSV(competitorName: str, competitorData: str):
        csvfile = None  

        try:
            csvfile = open(Arguments.PATH_CSV, 'a',newline='')
            
            with csvfile:
                fieldnames = ['Company', 'Details']
                writer = csv.DictWriter(csvfile,fieldnames=fieldnames,)
                # writer.writeheader()
                writer.writerow({'Company':competitorName, 'Details': competitorData})                                 
                        
        except Exception as e:
            print(e)
        
        finally:
            csvfile.close()