import xlrd

# news data location
loc = ("data/news1.xlsx")

def load_corpus():
    """
    read crawled data from xlsx file
    :return: list of news
    """
    wb = xlrd.open_workbook(loc)
    sheet = wb.sheet_by_index(0)
    news = [[sheet.cell_value(r, c) for c in range(sheet.ncols)] for r in range(sheet.nrows)]
    del news[0] # delete headers
    return news