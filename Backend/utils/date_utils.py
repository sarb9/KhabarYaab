from datetime import datetime
import re


def __datetime(date_str):
    date_str = date_str.replace("rd", "")
    date_str = date_str.replace("th", "")
    date_str = re.sub(r"st|rd|th|nd", "", date_str)
    return datetime.strptime(date_str, '%B %d %Y, %H:%M:%S.000')


def get_date(string_date):
    return str(__datetime(string_date))


def date_subtractor(date1, date2):
    start = __datetime(date1)
    end = __datetime(date2)

    delta = end - start
    return -1 * abs(delta.total_seconds() / (24 * 3600))
