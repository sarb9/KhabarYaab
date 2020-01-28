from collections import UserDict
from math import log
from optimzation.kmeans import kmeans, define_best_cluster_number
from optimzation.knn import knn
from random import sample

# from backend_main import SCORING_MODE

SCORING_MODE = 3


class Dictionary(UserDict):
    def __init__(self):
        super().__init__()
        self.docs = []

        # self.docs_weights = []
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
            # self.docs_weights.append(vector)
            # del doc.terms
        # del self.docs

    def calc_clusters(self):
        sampled_docs = sample(self.docs, k=min(len(self.docs), 15000))
        # cluster_number = define_best_cluster_number(sampled_docs, iterations=10)
        cluster_number = 12
        self.centroids = kmeans(sampled_docs, cluster_number, iterations=10)

    def calc_categories(self, labeled_docs, K=5):
        knn(labeled_docs=labeled_docs, docs=self.docs, K=K)

    def add_doc(self, doc):
        doc.set_id(len(self.docs))
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
