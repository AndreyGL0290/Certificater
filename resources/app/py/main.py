# LIBS FROM OTHER FILES FOR COMPILATION 
from pytrovich.enums import NamePart, Gender, Case
from pytrovich.maker import PetrovichDeclinationMaker
import pymorphy2 as pmr
from pptx import Presentation
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from smtplib import SMTP_SSL
from openpyxl import load_workbook
from datetime import date
from uuid import uuid4
from os import getcwd

# ONLY MAIN.PY LIBS
from operator import indexOf
from os import environ, makedirs
from sys import argv, stdout
from shutil import rmtree
from time import perf_counter
from smtplib import SMTPAuthenticationError
from concurrent.futures import ThreadPoolExecutor
from comtypes.client import CreateObject
from dotenv import load_dotenv

def init_powerpoint():
    powerpoint = CreateObject('PowerPoint.Application')
    powerpoint.UserControl = 0
    powerpoint.Visible = 1
    return powerpoint

def start(input_file_name, output_file_name, send):    
    time1 = perf_counter()

    from PPTX_to_PDF import pptx_to_pdf
    from sending import login, send_email
    from all_names import all_names
    from PPTX_GENERATOR import PPTX_GENERATOR

    if bool(int(send)):
        try:
            environ["MY_ADRESS"]
        except KeyError:
            send = False

    data = all_names(input_file_name, output_file_name)

    # Если Excel файл не найден
    if data == 'Excel':
        print('Excel файл не найден или не указан')
        return
    elif data == 'Template':
        print('Шаблон не найден или не указан')
        return

    # Не спраашивай зачем так много, просто надо
    makedirs(f"GENERATED_PPTX/{data[0]['date']}", exist_ok=True)
    makedirs(f"GENERATED_PDF/{data[0]['date']}", exist_ok=True)

    rmtree(f"GENERATED_PPTX/{data[0]['date']}")
    rmtree(f"GENERATED_PDF/{data[0]['date']}")

    makedirs(f"GENERATED_PPTX/{data[0]['date']}", exist_ok=True)
    makedirs(f"GENERATED_PDF/{data[0]['date']}", exist_ok=True)

    # Запускаем асинхронное редактирование pptx
    with ThreadPoolExecutor() as executor:
        file_name = list(executor.map(PPTX_GENERATOR, data))

    # with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
    #     print(list(executor.map(pptx_to_pdf, [{"file_name": file_name[:ceil(len(file_name)/2):], 'powerpoint': powerpoint}, {"file_name": file_name[ceil(len(file_name)/2)::], "powerpoint": powerpoint}])))
    if bool(int(send)):
        smtps = login()
    
    # Перебираем каждый элемент в массиве
    for loc in data:
        powerpoint = init_powerpoint()

        # file_name = PPTX_GENERATOR(loc)
        # pptx_to_pdf(file_name, loc['date'], powerpoint)
        # pptx_to_pdf(file_name[indexOf(data, loc)], powerpoint)

        pptx_to_pdf(file_name[indexOf(data, loc)], loc['date'], powerpoint)
        if bool(int(send)):
            try:
                send_email(loc['email'], smtps, loc['date'], file_name[indexOf(data, loc)])
            except SMTPAuthenticationError:
                print('Не верно указан пароль от почты.\n Статья о других возможных проблемах по ссылке')
                send = False
            except KeyError:
                print('В Excel документе нет поля email, сертификаты не были отправлены')
                send = False

    time2 = perf_counter()
    print(f'Процесс завершен за {time2-time1} секунд(ы)')
    powerpoint.Quit()

if __name__ == "__main__":
    # ВАЖНО: нужно для правильной передачи кириллицы на фронт
    stdout.reconfigure(encoding='utf-8')

    # Загружаем секретные переменные
    load_dotenv()

    # Начинаем
    start(argv[1], argv[2], argv[3])
