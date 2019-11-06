from models.news_model import NewsModel

from utils.import_utils import load_corpus, remove_tags

from pytest import fixture


@fixture(scope="class")
def corpus():
    corpus = load_corpus(loc="data/news1.xlsx")
    test_model = NewsModel(*corpus[0])

    return (corpus, test_model)


class TestImporter:

    def test_load_corpus(self, corpus):
        assert len(corpus[0]) == 1729
        assert corpus[1].url == "khabaronline.ir"

    def test_remove_tags(self, corpus):
        assert "<" not in remove_tags(corpus[1]).content
        assert ">" not in remove_tags(corpus[1]).content
