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
    print("your query: ", query)
    query_phrases = qh.extract_query_parts(query, without_pipeline=True)
    print(query_phrases, " mioooo")
    ans = qh.ask(query)
    results = []
    for doc_id in ans:
        news_model_view = mdls[doc_id]
        selected_part = highlight_phrases_in_content(news_model_view.content, query_phrases)
        results.append(
            {"selected_parts": selected_part, "id": news_model_view.id, "thumbnail": news_model_view.thumbnail,
             "title": news_model_view.title,
             "summary": news_model_view.summary, "publish_date": news_model_view.publish_date})

    return results


def highlight_phrases_in_content(content, query_phrases):
    result = ""

    def get_lower_bound(index):
        if index - threshold < 0:
            return 0
        else:
            return index - threshold

    def get_upper_bound(index):
        if index + threshold > len(content):
            return len(content)
        else:
            return index + threshold

    highlighted_content = content

    def bold_phrases(highlighted_content):
        phrases = []
        for qp in query_phrases:
            if qp.b:
                for term in qp.terms:
                    phrases.append(term)
        for phrase in phrases:
            highlighted_content = highlighted_content.replace(phrase, "<b>" + phrase + "</b>")
        return highlighted_content, phrases

    highlighted_content, phrases = bold_phrases(highlighted_content)

    threshold = 40 - 4 * len(phrases)
    print(threshold, "threshold")
    if threshold < 20:
        threshold = 20

    list_of_index = []
    for phrase in phrases:
        list_of_index.append(highlighted_content.find(phrase))
    list_of_index.sort()
    upper_index = 0
    lower_index = 0
    prev_index = None
    done =False
    print(list_of_index, " list of indexxx")
    for index in list_of_index:
        done = False
        if prev_index is None:
            lower_index = get_lower_bound(index)
        elif index - prev_index > threshold:
            done= True
            result += highlighted_content[lower_index: upper_index] + " ... "
            lower_index = get_lower_bound(index)
        upper_index = get_upper_bound(index)
        prev_index = index
    if not done:
        result += highlighted_content[lower_index: upper_index]
    print("resultssss: ", result)
    return result


corpus = import_utils.load_corpus()
print("reading from corpus...")
mdls = news_model.create_models_list_from_news(corpus)
ind = nindexer.Indexer()
ind.feed(mdls)
print("indexing...")
dct = ind.create_dictionary()
print("creating dictionary...")
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
