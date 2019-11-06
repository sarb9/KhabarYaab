from collections import namedtuple
from dictionary.posting import Posting
import re

QueryPhrase = namedtuple('QueryPhrase', ['b', 'terms'])


class QueryHandler:

    def __init__(self, dct):
        self.dct = dct

    def ask(self, query):
        query_phrases = self.extract_query_parts(query)

        ans = set(self.dct.keys())
        for qp in query_phrases:
            self.retrive(qp)

    def retrive(self, qp):
        docs = []
        print("----------------------------------------------------------------------")
        print(qp)

        for term in qp.terms:
            print(term, ": ---------------------------------------------------------")
            print(self.dct[term])
            print()
            print()
        print("************************************************************")

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
            print("-------->", pos0)

            flag = True
            target = Posting(*pos0)
            print(target)

            for token in qp.terms[1:]:

                target = Posting(target.doc_id, target.position + 1)
                token_post = get_post(token)

                while token_post and token_post < target:
                    token_post = inc_post(token)

                if token_post and token_post == target:
                    print("OK")
                    continue
                else:
                    print("FALSE on", token, target)
                    flag = False
                    break
            if flag:
                print(target)
                docs.append(target.doc_id)

            pos0 = inc_post(qp.terms[0])

        return docs

    @classmethod
    def extract_query_parts(cls, query):
        query = query.strip()

        parts = re.findall(r'!?\".*\"', query)
        parts[:] = [part[1:-1].strip() for part in parts]
        parts[:] = [QueryPhrase(True, re.split(' +', part)) if part[0] != '!'
                    else QueryPhrase(False, re.split(' +', part)) for part in parts]

        query = re.sub(r"\".*\"", '', query)
        query_parts = re.split(' +', query)
        parts += [QueryPhrase(True, (part,)) if part[0] != '!'
                  else QueryPhrase(False, (part, )) for part in query_parts if len(part) > 0]

        return parts
