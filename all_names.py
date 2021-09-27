from openpyxl import load_workbook


def all_names():
    wb = load_workbook('list.xlsx')
    wb = wb.active
    ans = [[j if j != None else '' for j in i] for i in wb.values]
    return ans

print (all_names())