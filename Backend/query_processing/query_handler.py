from collections import namedtuple
from ling_modules import lemmatizer, normalizer, pipline, stemmer, tokenizer
from dictionary.posting import Posting
from models import news_model
from indexer import nindexer
from math import log, sqrt
import re
import heapq
from dictionary.dictionary import SCORING_MODE

# from backend_main import SCORING_MODE

# from indexer.nindexer import check_case_folding
best_k = 30
QueryPhrase = namedtuple('QueryPhrase', ['b', 'terms'])


class QueryHandler:

    def __init__(self, dct):
        self.dct = dct
        self.pipline = pipline.Pipeline(
            normalizer.Normalizer(), stemmer.Stemmer())

    def ask(self, query):
        query_phrases = self.extract_query_parts(query)

        ans = set(i for i in range(news_model.NewsModel.gid))
        for qp in query_phrases:
            docs = self.retrive(qp)
            if qp.b:
                ans = ans & docs
            else:
                ans = ans - docs

        ans = self.sort_answers(ans, query_phrases)

        return ans

    def sort_answers(self, ans, query_phrases):
        vector = {}
        for qp in query_phrases:
            if qp.b:
                for term in qp.terms:
                    if term in vector:
                        vector[term] += 1
                    else:
                        vector[term] = 1

        max_tf = max(vector.values())
        for term, term_freq in vector.items():
            if SCORING_MODE == 1:
                vector[term] = (0.5 + 0.5 * term_freq / max_tf) * log(len(self.dct.docs) / self.dct[term].df)

            elif SCORING_MODE == 2:
                vector[term] = log(1 + len(self.dct.docs) / self.dct[term].df)
            elif SCORING_MODE == 3:
                print("000000000000", len(self.dct.docs), len(self.dct.docs) / self.dct[term].df)
                vector[term] = (1 + log(term_freq)) * log(len(self.dct.docs) / self.dct[term].df)

            # vector[term] = 1 + log(term_freq)

        answers = {}
        for doc_id in ans:
            score = 0
            doc = self.dct.docs[doc_id].vector
            for term, term_freq in vector.items():
                if term in doc:
                    score += doc[term] * term_freq


            answers[doc_id] = score / \
                (self.calc_length(doc) * self.calc_length(vector))

        return self.get_best_k_news(answers)

    def calc_length(self, vector):
        s = 0
        for tfidf in vector.values():
            s += tfidf ** 2
        return sqrt(s)

    def get_best_k_news(self, ans_dct):
        k = min(best_k, len(ans_dct))
        heap = [(-value, key) for key, value in ans_dct.items()]
        largest = heapq.nsmallest(k, heap)
        largest = [(key, -value) for value, key in largest]

        return [k[0] for k in largest]

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
        query = query.strip()

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

        return parts
