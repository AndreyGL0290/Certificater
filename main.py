from time import time_ns
import tkinter as tk
from tkinter import Image, Place, filedialog as fd


def start():
    global input_file_name
    global output_file_name
    from PPTX_to_PDF import main
    from all_names import all_names
    from PPTX_GENERATOR import PPTX_GENERATOR
    import os
    import shutil
    import time
    if output_file_name == '' or input_file_name == '':
        log.config(text='Chose 2 files')
    data = all_names(input_file_name, output_file_name)

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

    for loc in data:
        file_name = PPTX_GENERATOR(loc)
        command = "python PPTX_to_PDF.py " + file_name + " " + loc['date']
        main(file_name, loc['date'])
        file = file_name.replace("©", " ")
    log.config(text=f'Succesfull at {time.monotonic()}')


input_file_name = ''
output_file_name = ''


def input_file():
    global input_file_name
    input_file_name = fd.askopenfilename(filetypes=(
        ('Exel files', '*.xls;*.xlsx'), ("All files", "*.*"))).split('/')[-1]
    input_txt.config(text=input_file_name)


def output_file():
    global output_file_name
    output_file_name = fd.askopenfilename(filetypes=(
        ('PowerPoint files', '*.ppt;*.pptx'), ("All files", "*.*"))).split('/')[-1]
    output_txt.config(text=output_file_name)


root = tk.Tk()
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(),
              root.winfo_screenheight()))
root.title('Sertificater')

start_btn = tk.Button(text='Start', command=start)
input_btn = tk.Button(text='Enter input file', command=input_file)
output_btn = tk.Button(text='Enter output file', command=output_file)
input_txt = tk.Label()
output_txt = tk.Label()
log = tk.Label()
input_btn.pack()
input_txt.pack()
output_btn.pack()
output_txt.pack()
start_btn.pack()
log.pack()
root.mainloop()
