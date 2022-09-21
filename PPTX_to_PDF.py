from comtypes.client import CreateObject
import comtypes
import os

def init_powerpoint():
    powerpoint = CreateObject('PowerPoint.Application')
    powerpoint.UserControl = 0
    powerpoint.Visible = 1
    return powerpoint

def convertation(powerpoint, inputFileName, outputFileName, formatType = 32):
    if outputFileName[-3:] != 'pdf':
        outputFileName = outputFileName.replace(".pptx","").replace(".ppt","").replace("GENERATED_PPTX","GENERATED_PDF") + ".pdf"
    try:
        deck = powerpoint.Presentations.Open(inputFileName)
        deck.SaveAs(outputFileName, formatType) # formatType = 32 для ppt в pdf
        deck.Close()
    except comtypes.COMError:
        # Если случилась ошибка и сертификат не создается
        with open("logs.txt", 'a', encoding="utf-8") as log_file:
            log_file.writelines(["При создании сертификата из файла\n~", inputFileName, "~\nСлучилась ошибка и этот файл был пропущен\nКогда все сертификаты будут созданы программа пересоздаст их автоматически\n"])
        log_file.close()
        powerpoint = init_powerpoint()
        convertation(powerpoint, inputFileName, outputFileName)

def pptx_to_pdf(file_name, today_date, powerpoint):
    cwd = f"{os.getcwd()}\\GENERATED_PPTX\\{today_date}\\{file_name}.pptx"  # Создаём полный путь до файла
    convertation(powerpoint, cwd, cwd)  # Запуск конвертации