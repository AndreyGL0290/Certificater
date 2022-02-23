from math import ceil
from operator import index, indexOf
import os
import eel
import time
from smtplib import SMTPAuthenticationError
import concurrent.futures
from comtypes.client import CreateObject
from comtypes import CoInitializeEx, CoUninitialize
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
Не открывать и закрывать каждый раз Power Point
Сделать поп ап с формой ввода email
Сделать хэндлинг различных возникающих проблем
Поправить дизайн

Надо сделать:
Сделать чтобы галка появлялась только после ввода, а кнопка "ввести почту" менялась на "обновить почту"
'''

@eel.expose
def create_email_info(e, p):
    # Создаем или перезаписываем файл имеющейся информацией
    with open(".env", 'w') as env:
        env.write(f"MY_ADRESS = {e}\n")
        env.write(f"MY_PASSWORD = {p}\n")
    load_dotenv()

def init_powerpoint():
    powerpoint = CreateObject('PowerPoint.Application')
    powerpoint.UserControl = 0
    powerpoint.Visible = 1
    return powerpoint

@eel.expose
def start(input_file_name, output_file_name, send):    
    time1 = time.perf_counter()

    from PPTX_to_PDF import pptx_to_pdf
    from sending import login, send_email
    from all_names import all_names
    from PPTX_GENERATOR import PPTX_GENERATOR
    import os
    import shutil
    import os

    if send:
        try:
            os.environ["MY_ADRESS"]
        except KeyError:
            eel.raise_error("Почтовые данные не найдены, но сертификаты созданы")
            send = False

    data = all_names(input_file_name, output_file_name)

    # Если Excel файл не найден
    if data == 'Excel':
        eel.raise_error('Excel файл не найден или не указан')
        return
    elif data == 'Template':
        eel.raise_error('Шаблон не найден или не указан')
        return

    os.makedirs(f"GENERATED_PPTX/{data[0]['date']}", exist_ok=True)
    os.makedirs(f"GENERATED_PDF/{data[0]['date']}", exist_ok=True)

    shutil.rmtree(f"GENERATED_PPTX/{data[0]['date']}")
    shutil.rmtree(f"GENERATED_PDF/{data[0]['date']}")

    os.makedirs(f"GENERATED_PPTX/{data[0]['date']}", exist_ok=True)
    os.makedirs(f"GENERATED_PDF/{data[0]['date']}", exist_ok=True)

    # Запускаем асинхронное редактирование pptx
    with concurrent.futures.ThreadPoolExecutor() as executor:
        file_name = list(executor.map(PPTX_GENERATOR, data))

    powerpoint = init_powerpoint()

    # with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
    #     print(list(executor.map(pptx_to_pdf, [{"file_name": file_name[:ceil(len(file_name)/2):], 'powerpoint': powerpoint}, {"file_name": file_name[ceil(len(file_name)/2)::], "powerpoint": powerpoint}])))

    # Перебираем каждый элемент в массиве
    for loc in data:
        # file_name = PPTX_GENERATOR(loc)
        # if file_name == 'empty':
        #     powerpoint.Quit()
        #     t2 = time.perf_counter()
        #     print(f"Finished in {t2-t1} second(s)")
        #     return
        # pptx_to_pdf(file_name[indexOf(data, loc)], powerpoint)
        pptx_to_pdf(file_name[indexOf(data, loc)], loc['date'], powerpoint)
        if send:
            try:
                smtps = login()
                send_email(loc['email'], smtps, loc['date'], file_name)
            except SMTPAuthenticationError:
                eel.raise_error("Не верно указан пароль от почты.\n Статья о других возможных проблемах по ссылке")
                send = False
            except KeyError:
                eel.raise_error("В Excel документе нет поля email, сертификаты не были отправлены")
                send = False

    eel.raise_error("Процесс успешно завершен")
    time2 = time.perf_counter()
    # powerpoint.Quit()
    print(f"Finished in {time2-time1} second(s)")

if __name__ == "__main__":
    eel.start("HomePage.html", geometry={"size": (600, 400), "position": (400, 600)}, port=8002)
