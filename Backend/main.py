from query_processing import query_handler
from utils import import_utils
from models import news_model
from indexer import nindexer
from pytest import fixture
from query_handler import QueryHandler, QueryPhrase
from Server import app


def get_news_content(id):
    news_model_view = mdls[id]
    result = {"thumbnail": news_model_view.thumbnail, "title": news_model_view.title,
              "content": news_model_view.content, "id": news_model_view.id,
              "publish_date": news_model_view.publish_date, "summary": news_model_view.summary,
              "url": news_model_view.url, "meta_tags": news_model_view.meta_tags}

    return result


def get_news_headers(query):
    ans = qh.ask(query)
    results = []
    for id in ans:
        news_model_view = mdls[id]
        results.append({"thumbnail": news_model_view.thumbnail, "title": news_model_view.title,
                        "summary": news_model_view.summary, "publish_date": news_model_view.publish_date})

    return results


corpus = import_utils.load_corpus()
mdls = news_model.create_models_list_from_news(corpus)
ind = nindexer.Indexer()
ind.feed(mdls)
dct = ind.create_dictionary()
qh = QueryHandler(dct)
flask_app = app.FlaskServer(get_news_headers, get_news_content)
flask_app.run()

#
# def test_query_extractor():
#     qh = query_handler.QueryHandler(dict())
#     query = "    سرمایه گذاری میلیاردی رو پروژه ساخت \"سد خاکی\" !سابقه  "
#     query = " گزارش های مربوط به \" ساخت سد \" ۵۰ متری !خاکی "
#     query = " salam \" vali nemishe \" chera "
#     # ans = query_handler.QueryHandler.extract_query_parts(query)
#     # ans = query_handler.QueryHandler.extract_query_parts(
#     # " \"نسبت سنجی مفاد\" ")
#     query = "اسرائیل !عملیات"
#
#     query = '"خاک لبنان" "زندان دیگر" فلسطین از و برای به با'
#
#     ans = qh.extract_query_parts(query)
#     print(ans)
#
#
# @fixture(scope='module')
# def query_handler_fix():
#     print("loading corpus....")
#     corpus = import_utils.load_corpus()
#
#     print("creating models....")
#     mdls = news_model.create_models_list_from_news(corpus)
#     for model in mdls:
#         import_utils.remove_tags(model)
#
#     print("indexing....")
#     ind = nindexer.Indexer()
#     ind.feed(mdls)
#
#     print("creating dictionary....")
#     dct = ind.create_dictionary()
#
#     print("DICTIONARY CREATED!")
#     qh = QueryHandler(dct)
#     return qh
#
#
# '''
# def test_query_retrieve(query_handler_fix):
#     qp = QueryPhrase(True, ("رشت",))
#     qp = QueryPhrase(True, ("قبر", "محقر",))
#     qp = QueryPhrase(True, ("حسینقلی", "خان",))
#     qp = QueryPhrase(True, ("در", "تخت", "فولاد", "صاحب"))
#     qp = QueryPhrase(True, ("فعال", "سیاسی", "ایل"))
#     ans = query_handler_fix.retrive(qp)
#     print(ans)
# '''
#
#
# def test_query_retrieve_2(query_handler_fix):
#     print('--------------------------------------------------------------------------------')
#     # ans = query_handler.QueryHandler.extract_query_parts(
#     # "\"ناشر موظف است\"")[0]
#     # ans = query_handler.QueryHandler.extract_query_parts("\"گرماب\"")[0]
#     # ans = query_handler.QueryHandler.extract_query_parts(
#     # "\"هنوز    سنگ    قبر  \"")[0]
#     # ans = query_handler.QueryHandler.extract_query_parts(
#     # "\"آملی لاریجانی در زمان فعالیت\" ")[0]
#     # ans = query_handler.QueryHandler.extract_query_parts(
#     # "\"داخل پارکینگ\" \"انتقال جسد\" سوپ")
#     query = "اسرائیل عملیات"
#     query = '"خاک لبنان" "زندان دیگر" فلسطین'
#     query = '"مورد یمن" "تراژدی یمن" فلسطین'
#     ans = query_handler_fix.ask(query)
#     print('--------------------------------------------------------------------------------')
#
#     print(ans)
