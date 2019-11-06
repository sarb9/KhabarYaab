from query_processing import query_handler
from utils import import_utils
from models import news_model
from indexer import nindexer
from pytest import fixture
from query_handler import QueryHandler, QueryPhrase


def test_query_extractor():
    qh = query_handler.QueryHandler(dict())
    query = "    سرمایه گذاری میلیاردی رو پروژه ساخت \"سد خاکی\" !سابقه  "
    query = " گزارش های مربوط به \" ساخت سد \" ۵۰ متری !خاکی "
    query = " salam \" vali nemishe \" chera "
    # ans = query_handler.QueryHandler.extract_query_parts(query)
    # ans = query_handler.QueryHandler.extract_query_parts(
    # " \"نسبت سنجی مفاد\" ")
    query = "اسرائیل !عملیات"

    query = '"خاک لبنان" "زندان دیگر" فلسطین از و برای به با'

    ans = qh.extract_query_parts(query)
    print(ans)


@fixture(scope='module')
def query_handler_fix():

    print("loading corpus....")
    corpus = import_utils.load_corpus()

    print("creating models....")
    mdls = news_model.create_models_list_from_news(corpus)
    for model in mdls:
        import_utils.remove_tags(model)

    print("indexing....")
    ind = nindexer.Indexer()
    ind.feed(mdls)

    print("creating dictionary....")
    dct = ind.create_dictionary()

    print("DICTIONARY CREATED!")
    qh = QueryHandler(dct)
    return qh


'''
def test_query_retrieve(query_handler_fix):
    qp = QueryPhrase(True, ("رشت",))
    qp = QueryPhrase(True, ("قبر", "محقر",))
    qp = QueryPhrase(True, ("حسینقلی", "خان",))
    qp = QueryPhrase(True, ("در", "تخت", "فولاد", "صاحب"))
    qp = QueryPhrase(True, ("فعال", "سیاسی", "ایل"))
    ans = query_handler_fix.retrive(qp)
    print(ans)
'''


def test_query_retrieve_2(query_handler_fix):
    print('--------------------------------------------------------------------------------')
    # ans = query_handler.QueryHandler.extract_query_parts(
    # "\"ناشر موظف است\"")[0]
    # ans = query_handler.QueryHandler.extract_query_parts("\"گرماب\"")[0]
    # ans = query_handler.QueryHandler.extract_query_parts(
    # "\"هنوز    سنگ    قبر  \"")[0]
    # ans = query_handler.QueryHandler.extract_query_parts(
    # "\"آملی لاریجانی در زمان فعالیت\" ")[0]
    # ans = query_handler.QueryHandler.extract_query_parts(
    # "\"داخل پارکینگ\" \"انتقال جسد\" سوپ")
    query = "اسرائیل عملیات"
    query = '"خاک لبنان" "زندان دیگر" فلسطین'
    query = '"مورد یمن" "تراژدی یمن" فلسطین'
    ans = query_handler_fix.ask(query)
    print('--------------------------------------------------------------------------------')

    print(ans)
