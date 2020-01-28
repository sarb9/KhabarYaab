from utils.date_utils import get_date, date_subtractor
import os
import re

from optimzation.knn import categorize
from utils import import_utils
from models import news_model
from indexer import nindexer
from query_processing.query_handler import QueryHandler, QueryPhrase
from Server import app
# from indexer.nindexer import check_case_folding
from ling_modules.stemmer import add_similars
import copy
from optimzation.similarity import pop_best_k

SCORING_MODE = 1


def get_news_content(id):
    news_model_view = mdls[id]
    result = {"thumbnail": str(news_model_view.thumbnail), "title": news_model_view.title,
              "content": mdls_with_tags[id].content, "publish_date": str(news_model_view.publish_date),
              "summary": news_model_view.summary, "url": news_model_view.url, "meta_tags": news_model_view.meta_tags}

    return result


def get_news_headers(query):
    print("your query: ", query)
    query_phrases, _ = qh.extract_query_parts(query, without_pipeline=True)
    ans = qh.ask(query, b=min(len(dct.centroids), 5))
    results = []
    for doc_id in ans:
        news_model_view = mdls[doc_id]
        selected_part = highlight_phrases_in_content(
            news_model_view.content, query_phrases)
        results.append(
            {"selected_parts": selected_part, "id": news_model_view.id, "thumbnail": str(news_model_view.thumbnail),
             "title": news_model_view.title, "publish_date": news_model_view.publish_date,
             "news_date": get_date(news_model_view.publish_date)})
    return results


def get_similars(news_id):
    answers = qh.ask(None, doc=dct.docs[news_id], k=15, b=min(len(dct.centroids) - 2, 1))
    scores = {}
    for ans in answers:
        scores[ans] = date_subtractor(mdls[ans].publish_date, mdls[ans].publish_date)
    answers = pop_best_k(scores, 4)
    result = []
    for ans in answers:
        result.append({"title": mdls[ans].title, "url": "/results/" + str(ans)})

    return {"similar_news": result}


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


def create_models_without_tags(models):
    mdls_with_tags = copy.deepcopy(models)
    print("before:", len(models))
    # mdls = [model for model in mdls if import_utils.remove_tags(model) is not None
    temp_mdls = []
    removed_indices = []
    for i, model in enumerate(models):
        r_mdl = import_utils.remove_tags(model)
        if r_mdl is not None:
            temp_mdls.append(r_mdl)
        else:
            removed_indices.append(i)

    # mdls = temp_mdls
    mdls_with_tags = [model for i, model in enumerate(mdls_with_tags) if i not in removed_indices]
    return temp_mdls, mdls_with_tags


def index_crawler_models(crawler_models, original_dct, original_models_with_tags, original_models):
    crawler_models, models_with_tags = create_models_without_tags(crawler_models)
    ind = nindexer.Indexer()
    ind.feed(crawler_models)
    crawler_dct = ind.create_dictionary(for_crawler=True)
    for model in crawler_models:
        original_models.append(model)
    for model in models_with_tags:
        original_models_with_tags.append(model)

    for doc in crawler_dct.docs:
        original_dct.add_doc(doc)
        doc.category = categorize(doc)
    # save_new_dictionary()


labeled_docs_vector = None
if not os.path.exists('data/dictionary_obj.pkl'):
    print("reading labeled dataset corpus: ")
    corpus = import_utils.load_corpus(loc="data/labeled_dataset.xlsx", flag="xls")

    # models must be updated!!!!!
    mdls = news_model.create_models_list_from_news(corpus, labeled_data=True)
    for model in mdls:
        import_utils.remove_tags(model)
    ind = nindexer.Indexer()
    ind.feed(mdls, for_labeled_data=True)
    print("creating dictionary...")
    dct2 = ind.create_dictionary()
    print("end of reading of labeled dataset\n\n")
    labeled_docs_vector = dct2.docs
    del dct2

NUMBER_OF_FILES = 3
dataset_base_loc = "data/csv/ir-news-"

print("reading from corpus...")
mdls = []
for i in range(NUMBER_OF_FILES):
    # corpus = import_utils.load_corpus(flag="xls")
    print("reading " + "file " + str(i + 1) + " ...")
    loc = dataset_base_loc + str(2 * i) + "-" + str(2 * (i + 1)) + ".csv"
    corpus = import_utils.load_corpus(loc=loc, flag="csv")

    print("indexing...")
    for model in news_model.create_models_list_from_news(corpus):
        mdls.append(model)

# mdls_with_tags = copy.deepcopy(mdls)
#
# print("before:", len(mdls))
# # mdls = [model for model in mdls if import_utils.remove_tags(model) is not None
# temp_mdls = []
# removed_indices = []
# for i, model in enumerate(mdls):
#     r_mdl = import_utils.remove_tags(model)
#     if r_mdl is not None:
#         temp_mdls.append(r_mdl)
#     else:
#         removed_indices.append(i)
#
# mdls = temp_mdls
# mdls_with_tags = [model for i, model in enumerate(mdls_with_tags) if i not in removed_indices]

mdls, mdls_with_tags = create_models_without_tags(mdls)
print("after:", len(mdls))

ind = nindexer.Indexer()
print("feeding ...")
ind.feed(mdls)
print("creating dictionary...")
dct = ind.create_dictionary(labeled_vectors=labeled_docs_vector)
qh = QueryHandler(dct)
flask_app = app.FlaskServer(get_news_headers, get_news_content, get_similars)

flask_app.run()
