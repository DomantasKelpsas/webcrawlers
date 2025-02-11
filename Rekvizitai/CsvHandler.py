import csv
import Arguments
from Utils import Utils

class CsvHandler:
    print()
    # def writeDoctorsToCSV(sectionName: str, doctors: list[Doctor]):
    #     csvfile = None  

    #     try:
    #         csvfile = open(f'{Arguments.PATH_CSV}klinika_{sectionName}.csv', 'a',newline='',encoding='utf-8-sig')
            
    #         with csvfile:
    #             fieldnames = ['Name', 'Position', 'Url']
    #             writer = csv.DictWriter(csvfile,fieldnames=fieldnames,)
    #             # writer.writeheader()
    #             for doctor in doctors:
    #                 writer.writerow({'Name':doctor.name, 'Position':doctor.position, 'Url':doctor.url})                                 
                        
    #     except Exception as e:
    #         print(e)
        
    #     finally:
    #         csvfile.close()

    # def formatProcedureCSVRow(fieldnames: list[str], ProcedureName: str, ServiceName: str, Value1: str, additionaValues: list[str] = []):
    #     additionaFieldNames = fieldnames[3:]
    #     procedureCSVRow = {'ProcedureName': ProcedureName, 'ServiceName':ServiceName, 'Value1':Value1}

    #     additionalValueIndex = 0
    #     for fieldname in additionaFieldNames:
    #         procedureCSVRow[fieldname] = Utils.safe_get(additionaValues,additionalValueIndex)
    #         additionalValueIndex+=1
    #     return procedureCSVRow

    # def writePricesToCSV(sectionName: str, procedures: list[Procedure]):
    #     csvfile = None

    #     max_additional_values = max(
    #     (len(service.additionalValues) for procedure in procedures for service in procedure.services),
    #     default=0   
    #     )  

    #     fieldnames = ['ProcedureName', 'ServiceName', 'Value1']
    #     for i in range(0, max_additional_values):
    #         fieldnames.append(f'Value{i+2}')

    #     try:
    #         csvfile = open(f'{Arguments.PATH_CSV}klinika_{sectionName}.csv', 'a',newline='',encoding='utf-8-sig')
            
    #         with csvfile:
    #             writer = csv.DictWriter(csvfile,fieldnames=fieldnames,)
    #             for procedure in procedures:
                    
    #                 writer.writerow(CsvHandler.formatProcedureCSVRow(fieldnames, procedure.name,"", ""))
    #                 writer.writerow(CsvHandler.formatProcedureCSVRow(fieldnames, "", procedure.serviceTitleFields[0],procedure.serviceTitleFields[1],procedure.serviceTitleFields[2:]))
                    
    #                 for service in procedure.services:
    #                      writer.writerow(CsvHandler.formatProcedureCSVRow(fieldnames,"", service.name, service.value, service.additionalValues))
    #                 writer.writerow(CsvHandler.formatProcedureCSVRow(fieldnames, "", "", ""))
    #     except Exception as e:
    #         print(e)
        
    #     finally:
    #         csvfile.close()