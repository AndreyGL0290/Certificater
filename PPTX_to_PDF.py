import comtypes.client
import os

def init_powerpoint():
    powerpoint = comtypes.client.CreateObject("Powerpoint.Application")
    powerpoint.UserControl = 0
    
    return powerpoint
 
def ppt_to_pdf(powerpoint, inputFileName, outputFileName, formatType = 32):
    if outputFileName[-3:] != 'pdf':
        outputFileName = outputFileName.replace(".pptx","").replace(".ppt","").replace("GENERATED_PPTX","GENERATED_PDF") + ".pdf"
    deck = powerpoint.Presentations.Open(inputFileName)
    deck.SaveAs(outputFileName, formatType) # formatType = 32 for ppt to pdf
    deck.Close()
    #print('convert %s file complete '%outputFileName)

def main(file, today_date):
    # file = sys.argv[1]  # из аргументов командной строки получаем имя файла
    # today_date = sys.argv[2]  # и дату
    file = file.replace("©", " ")  # возвращаем обратно пробелы 
    powerpoint = init_powerpoint()  # инициализируем процесс PowerPoint (работает ТОЛЬКО в Windows)
    cwd = os.getcwd() + "\GENERATED_PPTX\\"+ today_date +"\\"+ file + ".pptx"  # создаём полный путь до файла 
    ppt_to_pdf(powerpoint, cwd, cwd)  # запуск конвертации 
    powerpoint.Quit()