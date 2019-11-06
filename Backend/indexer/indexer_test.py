from indexer import nindexer
from utils import import_utils
from models import news_model

from pytest import fixture


@fixture(scope='module')
def models():
    corpus = import_utils.load_corpus()
    mdls = news_model.create_models_list_from_news(corpus)
    for model in mdls:
        import_utils.remove_tags(model)
    return mdls


def test_index(models):
    ind = nindexer.Indexer()
    ind.feed(models)
    dct = ind.create_dictionary()

    # for term, pl in dct.items():
    # print([i.doc_id for i in pl])
    # print(term + ", tf:" + str(len(pl)) + ", df:" + str(pl.df))
