from openpyxl import load_workbook
import datetime
import uuid


def all_names(name, template):
    if name == '':
        name = 'list.xlsx'
    else:
        name = name.split('.')[0]+'.xlsx'
    wb = tuple(load_workbook(name).active.values)
    ans = list()
    for i in range(1, len(wb)):
        a = dict()
        for j in range(len(wb[i])):
            a[wb[0][j]] = wb[i][j]
        a['template'] = template
        a['date'] = "{:02d}".format(datetime.date.today().day) + "." + "{:02d}".format(
            datetime.date.today().month) + "." + str(datetime.date.today().year)
        a['id'] = uuid.uuid4().hex
        a['file_name'] = wb[i][0]

        ans.append(a)
    return ans