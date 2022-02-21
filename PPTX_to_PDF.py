from comtypes.client import CreateObject
from comtypes import CoInitializeEx, CoUninitialize, COINIT_MULTITHREADED
import datetime
import os

def init_powerpoint():
    CoInitializeEx(COINIT_MULTITHREADED)
    powerpoint = CreateObject('PowerPoint.Application')
    powerpoint.UserControl = 0
    powerpoint.Visible = 1
    return powerpoint

def convertation(powerpoint, inputFileName, outputFileName, formatType = 32):
    if outputFileName[-3:] != 'pdf':
        outputFileName = outputFileName.replace(".pptx","").replace(".ppt","").replace("GENERATED_PPTX","GENERATED_PDF") + ".pdf"

    deck = powerpoint.Presentations.Open(inputFileName)
    deck.SaveAs(outputFileName, formatType) # formatType = 32 для ppt в pdf
    deck.Close()

def pptx_to_pdf(file_names):
    powerpoint = init_powerpoint()
    today_date = "{:02d}".format(datetime.date.today().day) + "." + "{:02d}".format(datetime.date.today().month) + "." + str(datetime.date.today().year)
    for file_name in file_names:
        # powerpoint = init_powerpoint()
        cwd = f"{os.getcwd()}\\GENERATED_PPTX\\{today_date}\\{file_name}.pptx"  # Создаём полный путь до файла 
        convertation(powerpoint, cwd, cwd)  # Запуск конвертации
    