from dotenv import load_dotenv
from sys import argv, stdout

def create_email_info(e, p):
    # Создаем или перезаписываем файл имеющейся информацией
    with open(".env", 'w') as env:
        env.write(f"MY_ADRESS = {e}\n")
        env.write(f"MY_PASSWORD = {p}\n")
    load_dotenv()

if __name__ == '__main__':
    # ВАЖНО: нужно для правильной передачи кириллицы на фронт
    stdout.reconfigure(encoding='utf-8')

    create_email_info(argv[1], argv[2])