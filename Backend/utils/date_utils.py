from datetime import datetime


def __datetime(date_str):
    return datetime.strptime(date_str, '%B %dth %Y, %H:%M:%S.000')


def get_date(string_date):
    return __datetime(string_date)


def date_subtractor(date1, date2):
    start = __datetime(date1)
    end = __datetime(date2)

    delta = end - start
    return -1 * abs(delta.total_seconds() / (24 * 3600))
