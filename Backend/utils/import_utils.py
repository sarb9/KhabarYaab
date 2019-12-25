from models.news_model import NewsModel
from bs4 import BeautifulSoup
import xlrd

DATA_LOC = "data/news1.xlsx"


def remove_tags(news_model):
    news_model.content = BeautifulSoup(news_model.content, 'lxml').text
    return news_model


def load_corpus(loc=DATA_LOC):
    wb = xlrd.open_workbook(loc)
    sheet = wb.sheet_by_index(0)
    news = [[sheet.cell_value(r, c) for c in range(sheet.ncols)]
            for r in range(sheet.nrows)]
    del news[0]  # delete headers
    return news

