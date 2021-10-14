from PPTX_to_PDF import main
from all_names import all_names
from PPTX_GENERATOR import PPTX_GENERATOR

data = all_names(input('print input file name: '))

for loc in data:
    file_name = PPTX_GENERATOR(loc)
    command = "python PPTX_to_PDF.py " + file_name + " " + loc['date']
    main(file_name, loc['date'])
    file = file_name.replace("©", " ")
input('Process finished successfully. Press any key to exit.\n')