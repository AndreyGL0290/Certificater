from openpyxl import load_workbook


def all_names(name):
    if name == '':
        name = 'list.xlsx'
    wb = load_workbook(name)
    wb = wb.active
    ans = [[j if j != None else '' for j in i] for i in wb.values]
    print(*ans[1:])
    return ans
