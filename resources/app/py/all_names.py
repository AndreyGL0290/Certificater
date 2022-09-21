from openpyxl import Workbook, load_workbook
import datetime
import uuid

def name_fit(name):
    arr = name.split()
    valid_name = ''
    for i in range(len(arr)):
        valid_name += arr[i]
        if i != len(arr)-1:
            valid_name += ' '
    return valid_name

def all_names(work_list, template):
    if work_list == '':
        work_list = 'list.xlsx'

    # Для работы с Excel таблицей
    try:
        wb = tuple(load_workbook(work_list, data_only=True).active.values)
    except FileNotFoundError:
        return "Excel"
    ans = list()
    for i in range(1, len(wb)):
        a = dict()
        for j in range(len(wb[i])):                
            # Это сделано чтобы указывать падеж только на одной строке, а не на каждой
            if wb[0][j] in ['case', 'Case', 'CASE']:
                a[str(wb[0][j]).lower()] = str(wb[1][j]).lower()
            else:
                # Если ячейка, в которой должно быть слово-заместитель пусто, то не записываем ее значение
                if wb[0][j] == None:
                    continue
                a[str(wb[0][j]).lower()] = wb[i][j]
        # Если в Excel файле уже указаны шаблоны, то используем их.
        # Но если они есть в Excel, а человек ввел еще и свой, то используем тот что ввел человек.
        if "template" != a.keys():
            if template != '':
                a['template'] = template
            else:
                return "Template"
        a['date'] = "{:02d}".format(datetime.date.today().day) + "." + "{:02d}".format(
            datetime.date.today().month) + "." + str(datetime.date.today().year)
        a['id'] = uuid.uuid4().hex
        # Имя файла - ФИО человека и + id в дальнейшем

        # Если в ячейке где должно быть имя пусто, то удаляем весь объект с данными об участнике
        try:
            if a['name'] != None:
                a['name'] = name_fit(a['name'])
                a['file_name'] = a['name']
                ans.append(a)
        except KeyError:
            pass
    return ans