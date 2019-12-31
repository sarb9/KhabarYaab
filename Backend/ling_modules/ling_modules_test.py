import sys

from ling_modules.lemmatizer import Lemmatizer
from ling_modules.normalizer import Normalizer
from ling_modules.tokenizer import Tokenizer
from ling_modules.pipline import Pipeline
from ling_modules.stemmer import Stemmer

TEXT = '''
به گزارش ورزش سه ، محافظه‌کاری اخلاق کلاسیک لیگ‌مان شده است. همه برای نباختن،حفظ
شرایط موجود، سه امتیاز حیاتی و .. به میدان می‌آیند. در روز دوم اما دو مربی جسور
می‌خواستند فوتبال هم جریان داشته باشد. جذاب‌تر و هیجان انگیزتر.
خورده بود
پرنده ها پرواز کرده بودند
'''

RES = ['به', 'گزارش', 'ورزش', 'سه', '،', 'محافظه کار',
       'اخلاق', 'کلاسیک', 'لیگ', 'شده_است', '.',
       'همه', 'برای', 'نباختن', '،', 'حفظ', 'شرط',
       'موجود', '،', 'سه', 'امتیاز', 'حیاتی', 'و',
       '.', '.', 'به', 'میدان', 'می آیند', '.', 'در',
       'روز', 'دوم', 'اما', 'دو', 'مربی', 'جسور', 'می خواستند',
       'فوتبال', 'هم', 'جریان', 'داشته_باشد', '.', 'جذاب', 'و',
       'هیجان', 'انگیز', '.', 'خورده_بود', 'پرنده', 'پرواز', 'کرده_بودند']

'''
def test_pipline():
    pipeline = Pipeline(Normalizer(), Tokenizer(), Stemmer())
    res = pipeline.feed(TEXT)
    assert res == RES
    '''
