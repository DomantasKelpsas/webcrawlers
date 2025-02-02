import csv
import Arguments
from Models import Doctor
from Models import Service
from Models import Procedure
from Utils import Utils

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

    def writePricesToCSV(sectionName: str, procedures: list[Procedure]):
        csvfile = None  

        try:
            csvfile = open(f'{Arguments.PATH_CSV}klinika_{sectionName}.csv', 'a',newline='',encoding='utf-8-sig')
            
            with csvfile:
                fieldnames = ['ProcedureName', 'ServiceName', 'Value1', 'Value2']
                writer = csv.DictWriter(csvfile,fieldnames=fieldnames,)
                for procedure in procedures:
                    writer.writerow({'ProcedureName':procedure.name, 'ServiceName':"", 'Value1':"", 'Value2':""})
                    writer.writerow({'ProcedureName':"", 'ServiceName':Utils.safe_get(procedure.serviceTitleFields,0), 'Value1':Utils.safe_get(procedure.serviceTitleFields,1), 'Value2':Utils.safe_get(procedure.serviceTitleFields,2)})                                 

                    for service in procedure.services:
                            writer.writerow({'ProcedureName':"", 'ServiceName':service.name, 'Value1':service.value1, 'Value2':service.value2})
                    writer.writerow({'ProcedureName':"", 'ServiceName':"", 'Value1':"", 'Value2':""})       
        except Exception as e:
            print(e)
        
        finally:
            csvfile.close()