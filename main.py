import os
import eel
import time
import comtypes.client
from dotenv import load_dotenv

# Загружаем секретные переменные
load_dotenv()

path = os.getcwd()

eel.init(path + "\\Web")

'''
Сделано:
Русские символы в названии файлов
Возможность не склонять ФИО
Модификация склонения (по отчеству, если его нет, то morphy)
НЕ СКЛОНЯТЬ другие текстовые поля
При наличии не используемых полей возникает ошибка

Надо сделать:
Не открывать и закрывать каждый раз Power Point
Callback - делать pdf после полного создания 
'''

def init_powerpoint():
    powerpoint = comtypes.client.CreateObject("Powerpoint.Application")
    powerpoint.UserControl = 0
    powerpoint.Visible = 1
    return powerpoint

@eel.expose
def start(input_file_name, output_file_name, send):
    print(time.time())
    print(send)
    from PPTX_to_PDF import main
    from sending import login, send_email
    from all_names import all_names
    from PPTX_GENERATOR import PPTX_GENERATOR
    import os
    import shutil
    # data = all_names(input_file_name, output_file_name)
    # То что ниже нужно для тестинга
    data = all_names('data_copy_small.xlsx', 'tmplt1.pptx')

    os.makedirs(f"GENERATED_PPTX/{data[0]['date']}",
                exist_ok=True)
    os.makedirs(f"GENERATED_PDF/{data[0]['date']}",
                exist_ok=True)

    shutil.rmtree(f"GENERATED_PPTX/{data[0]['date']}")
    shutil.rmtree(f"GENERATED_PDF/{data[0]['date']}")

    os.makedirs(f"GENERATED_PPTX/{data[0]['date']}",
                exist_ok=True)
    os.makedirs(f"GENERATED_PDF/{data[0]['date']}",
                exist_ok=True)

    powerpoint = init_powerpoint()

    for loc in data:
        file_name = PPTX_GENERATOR(loc)
        # command = "python PPTX_to_PDF.py " + file_name + " " + loc['date']
        main(file_name, loc['date'], powerpoint)
        
        if send:
            try:
                send_email(loc['email'], login(), loc['date'], file_name)
            except KeyError:
                print("В Excel файле нет поля email, файлы не были отправлены")
        # file = file_name.replace("©", " ")

    powerpoint.Quit()
    print(time.time())

if __name__ == "__main__":
    eel.start("HomePage.html", geometry={"size": (600, 400), "position": (400, 600)}, port=8002)
