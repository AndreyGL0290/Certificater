from PPTX_to_PDF import main
import datetime
import uuid
from all_names import all_names
from PPTX_GENERATOR import PPTX_GENERATOR

today_date = "{:02d}".format(datetime.date.today().day)
today_date += "-" + "{:02d}".format(datetime.date.today().month)
today_date += "-" + str(datetime.date.today().year)

names = all_names()[1:]

for name in names:
    name[3]=name[3].split('.')[0]
    UID = uuid.uuid4().hex
    file = PPTX_GENERATOR(name, UID, today_date)
    command = "python PPTX_to_PDF.py " + file + " " + today_date
    main(file, today_date)
    file = file.replace("©", " ")
