from operator import indexOf
import os
import shutil
import subprocess
import eel
import sys
import time
from smtplib import SMTPAuthenticationError
import concurrent.futures
# from comtypes.client import CreateObject
from dotenv import load_dotenv

# from PPTX_to_PDF import pptx_to_pdf
from sending import login, send_email
from all_names import all_names
from PPTX_GENERATOR import PPTX_GENERATOR

# Loading Secret Variables
load_dotenv()

path = os.getcwd()

eel.init(path + "\\Web")

# def create_email_info(e, p):
#     # Creating or rewriting file with information given in gui
#     with open(".env", 'w') as env:
#         env.write(f"MY_ADRESS = {e}\n")
#         env.write(f"MY_PASSWORD = {p}\n")
#     load_dotenv()

# def init_powerpoint():
#     powerpoint = CreateObject('PowerPoint.Application')
#     powerpoint.UserControl = 0
#     powerpoint.Visible = 1
#     return powerpoint

def start(input_file_name, output_file_name, send=False):    
    time1 = time.perf_counter()

    if send:
        try:
            os.environ["MY_ADDRESS"]

            # Establishing smtps connection
            smtps = login()
        except KeyError:
            send = False
            print('Email data wasn\'t found, but certificates were created')
        except:
            send = False

    data = all_names(input_file_name, output_file_name)
    # if Excel file wasn't found
    if data == 'Excel':
        raise 'Excel file wasn\'t found'
    # if Powerpoint file wasn't found
    elif data == 'Template':
        raise 'Template file wasn\'t found'

    os.makedirs(f"GENERATED_PPTX/{data[0]['date']}", exist_ok=True)
    os.makedirs(f"GENERATED_PDF/{data[0]['date']}", exist_ok=True)

    shutil.rmtree(f"GENERATED_PPTX/{data[0]['date']}")
    shutil.rmtree(f"GENERATED_PDF/{data[0]['date']}")

    os.makedirs(f"GENERATED_PPTX/{data[0]['date']}", exist_ok=True)
    os.makedirs(f"GENERATED_PDF/{data[0]['date']}", exist_ok=True)

    # Starting asynchronous pptx rewriting
    with concurrent.futures.ThreadPoolExecutor() as executor:
        file_name = list(executor.map(PPTX_GENERATOR, data))

    # Starting bash script with libreoffice
    process = subprocess.Popen(['libreoffice.sh'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return_code = process.wait()
    print(return_code)

    # Iterating through every element of 'data' array and trying to send them
    for loc in data:
        # powerpoint = init_powerpoint()
        # pptx_to_pdf(file_name[indexOf(data, loc)], loc['date'], powerpoint)
        
        if not send:
            continue
            
        try:
            send_email(loc['email'], smtps, loc['date'], file_name)
        except SMTPAuthenticationError:
            send = False
            print('Email or password missmatch\nIf everything is correct your email is not supported') # Create a link
        except KeyError:
            send = False
            print('No email field in Excel document, certificates weren\'t sent')

    print('Process was successfully completed')
    # powerpoint.Quit()
    
    time2 = time.perf_counter()
    print(f"Finished in {time2-time1} second(s)")

if __name__ == "__main__":
    print(sys.argv)
    start(sys.argv[1], sys.argv[2], sys.argv[3])
    # eel.start("HomePage.html", geometry={"size": (600, 400), "position": (400, 600)}, port=8002)
