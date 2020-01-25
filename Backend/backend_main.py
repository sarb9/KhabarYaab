import re

from utils import import_utils
from models import news_model
from indexer import nindexer
from query_processing.query_handler import QueryHandler, QueryPhrase
from Server import app
# from indexer.nindexer import check_case_folding
from ling_modules.stemmer import add_similars
import copy

SCORING_MODE = 1


def get_news_content(id):
    news_model_view = mdls[id]
    result = {"thumbnail": news_model_view.thumbnail, "title": news_model_view.title,
              "content": mdls_with_tags[id].content, "publish_date": news_model_view.publish_date,
              "summary": news_model_view.summary, "url": news_model_view.url, "meta_tags": news_model_view.meta_tags}

    return result


def get_news_headers(query):
    print("your query: ", query)
    query_phrases = qh.extract_query_parts(query, without_pipeline=True)
    ans = qh.ask(query)
    results = []
    for doc_id in ans:
        news_model_view = mdls[doc_id]
        selected_part = highlight_phrases_in_content(
            news_model_view.content, query_phrases)
        results.append(
            {"selected_parts": selected_part, "id": news_model_view.id, "thumbnail": news_model_view.thumbnail,
             "title": news_model_view.title, "publish_date": news_model_view.publish_date})

    return results


def highlight_phrases_in_content(content, query_phrases):
    result = ""
    highlighted_content = content

    def get_lower_bound(index):
        if index - threshold < 0:
            return 0
        else:
            for i in range(index - threshold, len(highlighted_content)):
                if highlighted_content[i] == " ":
                    return i

    def get_upper_bound(index):
        upper_index = 0
        if index + threshold > len(highlighted_content):
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
                # case_folded = check_case_folding(integrated_term)
                # if case_folded != integrated_term:
                #     phrases.append(case_folded)

        for phrase in phrases:
            # highlighted_content = highlighted_content.replace(phrase, "<b style='color:red'>" + phrase + "</b>")
            highlighted_content = re.sub(r"\s[\u200c]?" + phrase,
                                         " <b style='color:red'>" + " " + phrase + " " + "</b> ",
                                         highlighted_content)



        return highlighted_content, phrases

    highlighted_content, phrases = bold_phrases(highlighted_content)

    threshold = 80 - 7 * len(phrases)
    if threshold < 22:
        threshold = 22

    list_of_index = []
    for phrase in phrases:
        # index = highlighted_content.find(phrase)
        index = re.search(r"\s[/u200c]?" + phrase, highlighted_content)
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


print("reading from corpus...")
corpus = import_utils.load_corpus(flag="xls")

print("indexing...")
mdls = news_model.create_models_list_from_news(corpus)
mdls_with_tags = copy.deepcopy(mdls)
for model in mdls:
    import_utils.remove_tags(model)

ind = nindexer.Indexer()
ind.feed(mdls)
print("creating dictionary...")
dct = ind.create_dictionary()
qh = QueryHandler(dct)
flask_app = app.FlaskServer(get_news_headers, get_news_content)
flask_app.run()
