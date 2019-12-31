from query_processing import query_handler
from utils import import_utils
from models import news_model
from indexer import nindexer
from pytest import fixture
from query_handler import QueryHandler, QueryPhrase


def test_query_extractor():
    qh = query_handler.QueryHandler(dict())
    query = '"خاک لبنان" "زندان دیگر" فلسطین از و برای به با'

    ans = qh.extract_query_parts(query)


@fixture(scope='module')
def query_handler_fix():
    corpus = import_utils.load_corpus()

    mdls = news_model.create_models_list_from_news(corpus)
    for model in mdls:
        import_utils.remove_tags(model)

    ind = nindexer.Indexer()
    ind.feed(mdls, force=True)

    dct = ind.create_dictionary(force=True)

    qh = QueryHandler(dct)
    return qh


def test_query_retrieve(query_handler_fix):
    qp = QueryPhrase(True, ("فعال", "سیاس", "ایل"))

    ans = query_handler_fix.retrive(qp)
    assert 1835 in ans


def test_query_retrieve_2(query_handler_fix):
    query = "تهران ایران"
    ans = query_handler_fix.ask(query)
    check = [2028, 2996, 3290, 2255, 3078, 3112, 2740, 3172, 2589, 2909, 2001, 2801, 2875, 3281,
             2089, 1899, 2225, 2182, 2142, 2666, 3258, 3409, 2628, 2571, 2954, 2560, 2488, 2215, 2663, 2256]


    assert check == ans
