from collections import UserDict
from math import log
from array import array
from optimzation.kmeans import kmeans, define_best_cluster_number
from optimzation.knn import knn

# from backend_main import SCORING_MODE

SCORING_MODE = 3


class Dictionary(UserDict):
    def __init__(self):
        super().__init__()
        # this will be vanished..
        self.docs = []

        self.docs_weights = []
        self.categories = []
        self.centroids = []

    def calc_doc_tf_idf(self):
        n_docs = len(self.docs)

        for doc in self.docs:
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
            self.docs_weights.append(vector)
            # del doc.terms
        # del self.docs

    def calc_clusters(self):
        cluster_number = define_best_cluster_number(self.docs, 4)
        self.centroids = kmeans(self.docs, cluster_number, 4)

    def calc_categories(self, labeled_doc ,K=5):
        self.categories = knn(labeled_doc=labeled_doc, all_docs_weights=self.docs_weights, K=K)

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
