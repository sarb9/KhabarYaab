from models.news_model import NewsModel
from bs4 import BeautifulSoup
import xlrd
import csv
import sys

import pandas as pd

DATA_LOC = "data/news.xlsx"


# DATA_LOC = "data/news_14.csv"

def remove_tags(news_model):
    if not news_model.content:
        return None
    news_model.content = BeautifulSoup(news_model.content, 'lxml').text
    if not news_model.content:
        return None
    return news_model


def load_corpus(loc=DATA_LOC, flag="xls"):
    if flag == "xls":
        wb = xlrd.open_workbook(loc)
        sheet = wb.sheet_by_index(0)
        news = [[sheet.cell_value(r, c) for c in range(sheet.ncols)]
                for r in range(sheet.nrows)]
        del news[0]  # delete headers
        return news

    # elif flag == "csv":
    #     csv.field_size_limit(sys.maxsize)
    #     with open(loc) as csv_file:
    #         csv_reader = csv.reader(csv_file, delimiter=',')
    #         news = list(csv_reader)
    #         for item in news:
    #             del item[8]
    #             del item[7]
    #             del item[4]
    #     return news

    elif flag == "csv":
        df = pd.read_csv(loc, error_bad_lines=False, engine="python", encoding="utf-8")

        del df['source_url']
        del df['category']
        del df['subcategory']

        return df
