import matplotlib.pyplot as plt
import random
from .similarity import calc_similarity


class Centroid:

    def __init__(self, weights):
        self.weights = weights

        self.next = {}
        self.n_docs = 0

        self.documents = []

    def similarity(self, document):
        return calc_similarity(self.weights, document)

    def add(self, document):
        for key, value in document.items():
            if key in self.next:
                self.next[key] += value
            else:
                self.next[key] = value
        self.n_docs += 1

    def calc(self):
        self.weights = {}
        for key, value in self.next.items():
            self.weights[key] = value / self.n_docs

        self.n_docs = 0
        self.next = {}

    def add_document(self, document):
        self.documents.append(document)


def kmeans(documents, k, iterations):
    centroids = []

    for i in range(k):
        rand = random.choice(documents).terms
        while len(rand.keys()) < 100:
            rand = random.choice(documents).terms

        centroids.append(Centroid(rand))

    def find_best_centroid(document):
        max_similarity = 0
        best_centroid = centroids[0]

        for centroid in centroids:
            sim = centroid.similarity(document)
            if sim > max_similarity:
                max_similarity = sim
                best_centroid = centroid
        return best_centroid

    # main loop of k-means
    for i in range(iterations):
        print("iteration", i, "started!")
        for document in documents:
            centroid = find_best_centroid(document.terms)
            centroid.add(document.terms)

        for centroid in centroids:
            centroid.calc()

    # assign documents to centroids
    for document in documents:
        find_best_centroid(document.terms).add_document(document)

    return centroids


def error_function(centroids, docs_no):
    error = 0

    for centroid in centroids:
        for document in centroid.documents:
            error += 1 - centroid.similarity(document.terms)

    if docs_no == 0:
        return error
    else:
        return error / docs_no


def define_best_cluster_number(documents, iterations):
    k = []
    errors = []
    for cluster_number in range(1, 20, 2):
        print("cluster_number:", cluster_number)
        centroids = kmeans(documents, cluster_number, iterations)
        error = error_function(centroids, docs_no=len(documents))
        print("cluster_number:", cluster_number, "error ->", error)
        errors.append(error)
        k.append(cluster_number)

    print("k:     ", k)
    print("error:    ", errors)

    fig = plt.figure()
    fig.suptitle('test title', fontsize=20)
    plt.xlabel('xlabel', fontsize=18)
    plt.ylabel('ylabel', fontsize=16)
    plt.plot(k, errors, "bo-")
    plt.show()

    cluster_number = int(input("it seems thr best number of clusters is: "))
    return cluster_number
