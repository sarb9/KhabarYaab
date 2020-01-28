import math
from datetime import datetime

# start_date = 'Sun Sep 16 16:05:15 +0000 2012'
# end_date = 'Sun Sep 17 23:55:20 +0000 2012'

start_date = "October 20th 2019, 15:56:00.000"
end_date = "October 18th 2019, 23:11:00.000"


def __datetime(date_str):
    return datetime.strptime(date_str, '%B %dth %Y, %H:%M:%S.000')


start = __datetime(start_date)
end = __datetime(end_date)

print(end)

# delta = end - start
# print(delta)  # prints: 1 day, 7:50:05
# print(abs(delta.total_seconds() / (24 * 3600)))  # prints: 114605.0
#
#
# # print("/news/"+ str3)
#
#
# print(type([11]) is list)