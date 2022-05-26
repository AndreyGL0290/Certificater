from operator import indexOf
import os
import shutil
import eel
import time
from smtplib import SMTPAuthenticationError
import concurrent.futures
from comtypes.client import CreateObject
from dotenv import load_dotenv
# Загружаем секретные переменные
load_dotenv()

path = os.getcwd()

eel.init(path + "\\Web")

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

    if send:
        try:
            os.environ["MY_ADRESS"]
        except KeyError:
            eel.raise_error("Почтовые данные не найдены, но сертификаты созданы")
            send = False

    data = all_names(input_file_name, output_file_name)
    print(data)
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

    # Устанавлиавем соединение
    if send:
        smtps = login()

    # Перебираем каждый элемент в массиве
    for loc in data:
        # file_name = PPTX_GENERATOR(loc)
        # pptx_to_pdf(file_name, loc['date'], powerpoint)
        # pptx_to_pdf(file_name[indexOf(data, loc)], powerpoint)
        pptx_to_pdf(file_name[indexOf(data, loc)], loc['date'], powerpoint)
        if send:
            try:
                send_email(loc['email'], smtps, loc['date'], file_name)
            except SMTPAuthenticationError:
                eel.raise_error("Не верно указана почта или пароль от почты\nЕсли все указано верно, то ваша почта не поддержиаватся") # Сделать ссылку
                send = False
            except KeyError:
                eel.raise_error("В Excel документе нет поля email, сертификаты не были отправлены")
                send = False

    eel.raise_error("Процесс успешно завершен")
    time2 = time.perf_counter()
    powerpoint.Quit()
    print(f"Finished in {time2-time1} second(s)")

if __name__ == "__main__":
    eel.start("HomePage.html", geometry={"size": (600, 400), "position": (400, 600)}, port=8002)
