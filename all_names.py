from openpyxl import load_workbook
import datetime
import uuid


def all_names(work_list, template):
    if work_list == '':
        work_list = 'list.xlsx'
    else:
        # Меняем расширение файла на .xlsx на случай если человек выберет немного другой формат Excel таблицы
        parts = work_list.split('.')
        if len(parts) >= 3:
            work_list  = ''
            for i in range(len(parts) - 1):
                work_list += parts[i] + "."
            work_list += 'xlsx'

    # Для работы с Excel таблицей
    try:
        wb = tuple(load_workbook(work_list).active.values)
    except FileNotFoundError:
        return "Excel"

    ans = list()
    for i in range(1, len(wb)):
        a = dict()
        for j in range(len(wb[i])):
            # Это сделано чтобы указывать падеж только на одной строке, а не на каждой
            if wb[0][j] == 'case':
                a[wb[0][j]] = wb[1][j]
            else:
                a[wb[0][j]] = wb[i][j]
        # Если в Excel файле уже указаны шаблоны, то используем их.
        # Но если они есть в Excel, а человек ввел еще и свой, то используем тот что ввел человек.
        if template != '':
            a['template'] = template
        a['date'] = "{:02d}".format(datetime.date.today().day) + "." + "{:02d}".format(
            datetime.date.today().month) + "." + str(datetime.date.today().year)
        a['id'] = uuid.uuid4().hex
        # Имя файла - ФИО человека и + id в дальнейшем
        a['file_name'] = a['name']

        ans.append(a)
    return ans