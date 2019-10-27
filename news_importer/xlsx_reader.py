import xlrd

loc = ("data/news1.xlsx")

wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)

print(sheet.cell_value(0, 0))
print(sheet.nrows)
print(sheet.ncols)

for i in range(sheet.ncols):
    print(sheet.cell_value(0, i))

for i in range(sheet.nrows):
    print(sheet.cell_value(i, 0))

print(sheet.row_values(1))

print()
for i in range(sheet.ncols):
    print(sheet.cell_value(1, i))
    print()

print(sheet.cell_value(1, 1))
