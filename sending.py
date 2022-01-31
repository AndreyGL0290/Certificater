from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import smtplib
import os

def read_template(filename):
    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return template_file_content

def login():
    smtps = smtplib.SMTP_SSL(host="smtp.gmail.com", port=465) # Порт 587 используется для smtp, а 465 для smtps
    smtps.ehlo()
    smtps.login(os.environ["MY_ADRESS"], os.environ["MY_PASSWORD"])

    return smtps

def send_email(email, smtps, date, filename):
    if email:
        attach_file = open(f"{os.getcwd()}\\GENERATED_PDF\\{date}\\{filename}.pdf", 'rb') # Открывает файл в бинарном режиме
        payload = MIMEBase('application', 'octate-stream')
        payload.set_payload((attach_file).read())
        encoders.encode_base64(payload) # Расшифровывает добавленный файл
        # Добавляет нагрузке заголовок и имя файла
        payload.add_header('Content-Disposition', 'attachment', filename=f"{filename}.pdf")

        try:
            message = read_template("letter.txt")
        except FileNotFoundError:
            message = ''
        msg = MIMEMultipart() # Создает сообщение

        # Задаем параметры "От", "Кому" и "Тема"
        msg['From'] = os.environ["MY_ADRESS"]
        msg['To'] = email
        msg['Subject'] = 'Сертификат участника образовательного проекта ДТ "Кванториум"'

        # Добавляет текст из файла в email
        msg.attach(MIMEText(message, 'plain'))
        msg.attach(payload)
        # Отправляжет сообщние
        smtps.send_message(msg)
        
        del msg