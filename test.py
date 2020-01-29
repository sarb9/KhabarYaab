import math
import re
from collections import namedtuple
from datetime import datetime

# start_date = 'Sun Sep 16 16:05:15 +0000 2012'
# end_date = 'Sun Sep 17 23:55:20 +0000 2012'
from ling_modules.stemmer import add_similars
from utils import import_utils

start_date = "October 20rd 2019, 15:56:00.000"
end_date = "October 18th 2019, 23:11:00.000"
end_date4 = "October 18st 2019, 23:11:00.000"


def __datetime(date_str):
    date_str = re.sub(r"st|rd|th", "", date_str)
    return datetime.strptime(date_str, '%B %d %Y, %H:%M:%S.000')


start = __datetime(start_date)
end = __datetime(end_date)
end34 = __datetime(end_date4)

print(end)
print(start)
print(end34)


# delta = end - start
# print(delta)  # prints: 1 day, 7:50:05
# print(abs(delta.total_seconds() / (24 * 3600)))  # prints: 114605.0
#
#
# # print("/news/"+ str3)
#
#
# print(type([11]) is list)


def highlight_phrases_in_content(content, query_phrases):
    print(query_phrases)
    result = ""
    highlighted_content = import_utils.remove_tag_from_content(content)
    print(highlighted_content)

    def get_lower_bound(index):
        if index - threshold < 0:
            return 0
        else:
            for i in range(index - threshold, len(highlighted_content)):
                if highlighted_content[i] == " ":
                    return i

    def get_upper_bound(index):
        upper_index = 0
        if index + threshold > len(highlighted_content) - 1:
            return len(highlighted_content)
        else:
            for i in range(index + threshold, 0, -1):
                if highlighted_content[i] == " ":
                    upper_index = i
                    break
        findex = highlighted_content[index: upper_index].find("<b")
        if findex == -1:
            return upper_index
        else:
            return index + findex

    def bold_phrases(highlighted_content):
        phrases = []
        for qp in query_phrases:
            if qp.b:
                integrated_term = ""
                for term in qp.terms:
                    integrated_term += term + " "
                integrated_term = integrated_term.strip()
                phrases.append(integrated_term)
                for s_term in add_similars(integrated_term):
                    if integrated_term != s_term:
                        phrases.append(s_term)

        for phrase in phrases:
            highlighted_content = re.sub(r"[\s\":;»«][\u200c]?" + phrase,
                                         " <b style='color:red'>" + " " + phrase + " " + "</b> ",
                                         highlighted_content)

        return highlighted_content, phrases

    highlighted_content, phrases = bold_phrases(highlighted_content)
    print(phrases)

    threshold = 80 - 7 * len(phrases)
    if threshold < 22:
        threshold = 22

    list_of_index = []
    for phrase in phrases:
        # index = highlighted_content.find(phrase)
        index = re.search(r"[\s\":;»«][\u200c]?" + phrase, highlighted_content)
        if index is not None:
            list_of_index.append(index.start())
        # if index != -1:
        #     list_of_index.append(index)

    list_of_index.sort()
    upper_index = 0
    lower_index = 0
    prev_index = None
    for index in list_of_index:
        if prev_index is None:
            lower_index = get_lower_bound(index)
        elif index - prev_index > threshold:
            result += highlighted_content[lower_index: upper_index] + "..."
            lower_index = get_lower_bound(index)
        upper_index = get_upper_bound(index)
        prev_index = index

    result += highlighted_content[lower_index: upper_index] + "..."
    return result


str = """
به گزارش خبرنگار پارلمانی <strong><a href="http://shabestan.ir">خبرگزاری شبستان</a>، &laquo;شادمهر کاظم زاده&raquo;</strong> شب گذشته (دوشنبه 29 مهرماه) در برنامه گفتگوی ویژه خبری شبکه دو سیما درباره لزوم توسعه حمل و نقل ریلی کشور مباحثی را بازگو کرد و یکی از علل اصلی توسعه نیافتن حمل و نقل ریلی را جایگزینی اعتبارات عنوان کرد و گفت: برای انجام نشدن برنامه‌های پیش بینی شده توسعه ریلی کشور، محدودیت‌های مالی را مطرح می‌کنند در حالی که در ماده ۷۰ قانون الحاق تنظیم بخشی از مقررات مالی دولت، به صراحت آمده است که ۲۰ درصد فروش نفت و گاز، اختصاصا برای تثبیت تعرفه، حق دسترسی و توسعه و نگهداری شبکه ریلی کشور باید منظور شود.
&nbsp;
<strong>رئیس کمیته حمل و نقل کمیسیون عمران مجلس شورای اسلامی</strong> با بیان اینکه اکنون ۸۹ درصد ارتباطات و حمل بار و مسافر، زمینی و یک درصد، هوایی و حدود ۱۰ درصد، ریلی است، گفت: در بند الف ماده ۵۲ قانون برنامه ششم توسعه به صراحت امده که دولت مکلف است نسبت به تضمین سرمایه گذاری اشخاص غیردولتی اقدامات لازم را انجام دهد.
&nbsp;مهر کاظم
وی اضافه کرد: همچنین یک درصد درآمد فروش سالانه سهم نفتی دولت باید به وزارت راه و شهرسازی تخصیص داده شود، اما این کار انجام نمی‌شود.از نگاه قانونی، توان داخلی برای اجرای طرح های توسعه ای ریلی وجود دارد.
&nbsp;
رئیس کمیته حمل و نقل کمیسیون عمران مجلس شورای اسلامی گفت: اگر شبکه ریلی کشورمان را سریعتر به مرز‌ها وصل نکنیم، از لحاظ حمل و نقل به نسبت رقبا و کشور‌های همسایه و مسیر‌های جایگزین، عقب می‌مانیم و مزیت رقابتی را از دست می‌دهیم./

"""
