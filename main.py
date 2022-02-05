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
Не открывать и закрывать каждый раз Power Point

Надо сделать:
Сделать чтобы галка появлялась только после ввода, а кнопка "ввести почту" менялась на "обновить почту"
Сделать поп ап с формой ввода
Сделать хэндлинг различных возникающиз проблем
Поправить дизайн
'''

@eel.expose
def create_email_info(e, p):
    # Создаем или перезаписываем файл имеющейся информацией
    with open(".env", 'w') as env:
        env.write(f"MY_ADRESS = {e}\n")
        env.write(f"MY_PASSWORD = {p}\n")
    load_dotenv()

def init_powerpoint():
    powerpoint = comtypes.client.CreateObject("Powerpoint.Application")
    powerpoint.UserControl = 0
    powerpoint.Visible = 1
    return powerpoint

@eel.expose
def start(input_file_name, output_file_name, send):    
    print(time.time())

    from PPTX_to_PDF import main
    from sending import login, send_email
    from all_names import all_names
    from PPTX_GENERATOR import PPTX_GENERATOR
    import os
    import shutil
    from smtplib import SMTPAuthenticationError
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
        eel.raise_error('Excel файл не найден')
        return

    os.makedirs(f"GENERATED_PPTX/{data[0]['date']}", exist_ok=True)
    os.makedirs(f"GENERATED_PDF/{data[0]['date']}", exist_ok=True)

    shutil.rmtree(f"GENERATED_PPTX/{data[0]['date']}")
    shutil.rmtree(f"GENERATED_PDF/{data[0]['date']}")

    os.makedirs(f"GENERATED_PPTX/{data[0]['date']}", exist_ok=True)
    os.makedirs(f"GENERATED_PDF/{data[0]['date']}", exist_ok=True)

    powerpoint = init_powerpoint()

    for loc in data:
        file_name = PPTX_GENERATOR(loc)
        if file_name == "Template":
            eel.raise_error("Файл-шаблон не найден")
            powerpoint.Quit()
            return
        # command = "python PPTX_to_PDF.py " + file_name + " " + loc['date']
        main(file_name, loc['date'], powerpoint)

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
        # file = file_name.replace("©", " ")

    powerpoint.Quit()
    eel.raise_error("Процесс успешно завершен")
    print(time.time())

if __name__ == "__main__":
    eel.start("HomePage.html", geometry={"size": (
        600, 400), "position": (400, 600)}, port=8002)
