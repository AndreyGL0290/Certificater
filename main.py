from PPTX_to_PDF import main
from all_names import all_names
from PPTX_GENERATOR import PPTX_GENERATOR
import os, shutil

data = all_names(input('print input file name: '))

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
input('Process finished successfully. Press enter to exit.\n')
