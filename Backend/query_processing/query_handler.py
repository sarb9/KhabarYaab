from collections import namedtuple
from ling_modules import lemmatizer, normalizer, pipline, stemmer, tokenizer
from dictionary.posting import Posting
from models import news_model
from indexer import nindexer
import re

QueryPhrase = namedtuple('QueryPhrase', ['b', 'terms'])


class QueryHandler:

    def __init__(self, dct):
        self.dct = dct
        self.pipline = pipline.Pipeline(
            normalizer.Normalizer(), stemmer.Stemmer())

    def ask(self, query):
        query_phrases = self.extract_query_parts(query)
        # print(query_phrases, " ()))() query phrases")

        ans = set(i for i in range(news_model.NewsModel.gid))
        for qp in query_phrases:
            docs = self.retrive(qp)
            print(docs)
            if qp.b:
                ans = ans & docs
                print(ans)
            else:
                ans = ans - docs

        return ans

    def retrive(self, qp):
        docs = set()
        # print("----------------------------------------------------------------------")
        # print(qp)

        # for term in qp.terms:
        ##print(term, ": ---------------------------------------------------------")
        # print(self.dct[term])
        # print()
        # print()
        # print("************************************************************")

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
            ##print("-------->", pos0)

            flag = True
            target = Posting(*pos0)
            # print(target)

            for token in qp.terms[1:]:

                target = Posting(target.doc_id, target.position + 1)
                token_post = get_post(token)

                while token_post and token_post < target:
                    token_post = inc_post(token)

                if token_post and token_post == target:
                    # print("OK")
                    continue
                else:
                    ##print("FALSE on", token, target)
                    flag = False
                    break
            if flag:
                docs.add(target.doc_id)

            pos0 = inc_post(qp.terms[0])

        return docs

    def extract_query_parts(self, query, without_pipeline=False):
        query = query.strip()

        parts = re.findall(r'!?\".*?\"', query)

        parts[:] = [QueryPhrase(True, re.split(' +', part[1:-1].strip())) if part[0] != '!'
                    else QueryPhrase(False, re.split(' +', part[2:-1])) for part in parts]

        query = re.sub(r"\".*?\"", '', query)
        query_parts = re.split(' +', query)
        query_parts[:] = [
            token for token in query_parts if token not in nindexer.STOP_WORDS]
        parts += [QueryPhrase(True, (part,)) if part[0] != '!'
                  else QueryPhrase(False, (part[1:], )) for part in query_parts if len(part) > 0]
        if not without_pipeline:
            parts[:] = [QueryPhrase(part.b, [self.pipline.feed(term)
                                             for term in part.terms]) for part in parts]

        return parts
