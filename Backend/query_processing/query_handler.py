from collections import namedtuple
from ling_modules import lemmatizer, normalizer, pipline, stemmer, tokenizer
from dictionary.posting import Posting
from models import news_model
from indexer import nindexer
import re
from dictionary.dictionary import SCORING_MODE
from math import log
from optimzation.similarity import calc_similarity, pop_best_k

# from backend_main import SCORING_MODE

# from indexer.nindexer import check_case_folding
QueryPhrase = namedtuple('QueryPhrase', ['b', 'terms'])


class QueryHandler:

    def __init__(self, dct):
        self.dct = dct
        self.pipline = pipline.Pipeline(
            normalizer.Normalizer(), stemmer.Stemmer())

    def ask(self, query, with_clustering=False, doc=None, k=30, b=9):
        # category,  = None
        if query is not None:
            query_phrases, category = self.extract_query_parts(query)
        if with_clustering:
            nots = {}
            more_than_one = False
            necessary_docs_id = {}
            if doc is None:
                nots = {term for qp in query_phrases for term in qp.terms if not qp.b}
                necessary_docs_id = set(i for i in range(len(self.dct.docs)))

                for qp in query_phrases:
                    if qp.b and len(qp.terms) > 1:
                        more_than_one = True
                        necessary_docs_id = necessary_docs_id & self.retrive(qp)
                query_vector = self.weight_query(query_phrases)

            else:
                query_vector = doc.terms
                category = doc.category

            best_centroids = []
            for i in range(b):
                best_centroid = None
                best_similarity = -1
                for centroid in self.dct.centroids:
                    if centroid in best_centroids:
                        continue
                    sim = calc_similarity(query_vector, centroid.weights)
                    if sim > best_similarity:
                        best_similarity = sim
                        best_centroid = centroid
                best_centroids.append(best_centroid)
            scores = {}
            for centroid in best_centroids:
                for document in centroid.documents:
                    if document == doc:
                        continue
                    common_terms = set(document.terms) & set(query_vector)
                    if len(common_terms) >= min(len(query_vector), 2) and (
                            set(document.terms) & set(nots) == set()) and (
                            not more_than_one or document.id in necessary_docs_id):
                        if category is None or document.category.lower() == category.lower():
                            scores[document.id] = calc_similarity(query_vector, document.terms)

            print("mioooooo", pop_best_k(scores, k))
            return pop_best_k(scores, k)
        else:
            ans = set(i for i in range(len(self.dct.docs)))

            for qp in query_phrases:
                docs = self.retrive(qp)
                if qp.b:
                    ans = ans & docs
                else:
                    ans = ans - docs

            ans = self.sort_answers(ans, query_phrases)
            if category is not None:
                categorized_ans = []
                for answer in ans:
                    if self.dct.docs[answer].category == category:
                        categorized_ans.append(answer)
                return categorized_ans
            print("miooo ", ans)
            return ans

    def weight_query(self, query_phrases):
        query_vector = {}
        for qp in query_phrases:
            if qp.b:
                for term in qp.terms:
                    if term in query_vector:
                        query_vector[term] += 1
                    else:
                        query_vector[term] = 1

        max_tf = max(query_vector.values())
        for term, term_freq in query_vector.items():
            if SCORING_MODE == 1:
                query_vector[term] = (0.5 + 0.5 * term_freq / max_tf) * log(
                    len(self.dct.docs) / self.dct[term].df)

            elif SCORING_MODE == 2:
                query_vector[term] = log(1 + len(self.dct.docs) / self.dct[term].df)
            elif SCORING_MODE == 3:
                print("000000000000", len(self.dct.docs), len(self.dct.docs) / self.dct[term].df)
                query_vector[term] = (1 + log(term_freq)) * log(len(self.dct.docs) / self.dct[term].df)
        return query_vector

    def sort_answers(self, ans, query_phrases):
        query_vector = self.weight_query(query_phrases)

        similarities = {}
        for doc_id in ans:
            doc_vector = self.dct.docs[doc_id].terms
            similarities[doc_id] = calc_similarity(doc_vector, query_vector)

        return pop_best_k(similarities, 30)

    def retrive(self, qp):
        docs = set()

        pointer = {term: 0 for term in qp.terms}

        def get_post(term):
            if pointer[term] < len(self.dct[term]):
                return self.dct[term][pointer[term]]
            else:
                return False

        def inc_post(term):
            pointer[term] += 1
            if pointer[term] < len(self.dct[term]):
                return self.dct[term][pointer[term]]
            else:
                return False

        pos0 = get_post(qp.terms[0])
        while pos0:

            flag = True
            target = Posting(*pos0)

            for token in qp.terms[1:]:

                target = Posting(target.doc_id, target.position + 1)
                token_post = get_post(token)

                while token_post and token_post < target:
                    token_post = inc_post(token)

                if token_post and token_post == target:
                    continue
                else:
                    flag = False
                    break
            if flag:
                docs.add(target.doc_id)

            pos0 = inc_post(qp.terms[0])

        return docs

    def extract_query_parts(self, query, without_pipeline=False):
        # Todo : query and pipeline
        category = None
        query = query.strip()
        for term in re.split(' +', query):
            match = re.search("cat:", term)
            if match is not None:
                category = term[match.end():].strip().lower()
                query = query.replace(term, "")
                break

        parts = re.findall(r'!?\".*?\"', query)

        parts[:] = [QueryPhrase(True, re.split(' +', part[1:-1].strip())) if part[0] != '!'
                    else QueryPhrase(False, re.split(' +', part[2:-1])) for part in parts]

        query = re.sub(r"\".*?\"", '', query)
        query_parts = re.split(' +', query)
        query_parts[:] = [
            token for token in query_parts if token not in nindexer.STOP_WORDS]
        parts += [QueryPhrase(True, (part,)) if part[0] != '!'
                  else QueryPhrase(False, (part[1:],)) for part in query_parts if len(part) > 0]
        if not without_pipeline:
            parts[:] = [QueryPhrase(part.b, [self.pipline.feed([term])[0]
                                             for term in part.terms]) for part in parts]

        return parts, category
