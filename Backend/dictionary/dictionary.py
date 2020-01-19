from collections import UserDict
from math import log
from array import array

# from backend_main import SCORING_MODE

SCORING_MODE = 3


class Dictionary(UserDict):
    def __init__(self):
        super().__init__()
        self.docs = []
    # docs = []

    def calc_tf_idf(self):
        keys = self.data.keys()
        keys = list(keys)
        n_docs = len(self.docs)

        for i, doc in enumerate(self.docs):
            vector = {}
            for term, tf in doc.terms.items():
                if SCORING_MODE == 1:
                    vector[term] = tf * log(n_docs / self.data[term].df)

                elif SCORING_MODE == 2:
                    vector[term] = (1 + log(tf))

                elif SCORING_MODE == 3:
                    vector[term] = (1 + log(tf)) * \
                                   log(n_docs / self.data[term].df)

            doc.set_vector(vector)

    def add_doc(self, doc):
        self.docs.append(doc)

    def __missing__(self, key):
        if isinstance(key, str):
            raise (Exception("MISS: ##############################" +
                             key + "##############################"))
        else:
            return self.data[str(key)]

    def __contains__(self, key):
        return str(key) in self.data

    def __setitem__(self, key, item):
        self.data[str(key)] = item
