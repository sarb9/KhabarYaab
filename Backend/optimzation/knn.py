from optimzation.similarity import calc_similarity, pop_best_k

labeled_data = None


def knn(labeled_docs, docs, K):
    """
    label whole dataset based on limited labeled docs
    :param labeled_docs: limited labeled documents, list of tuples : [(docID, Label), ...]
    :param all_docs_weights: whole dataset containing labeled ones, list of vectors
    :return:
    """
    global labeled_data
    labeled_data = labeled_docs
    for document in docs:
        categorize(document, labeled_docs=labeled_docs, k=K)


def categorize(doc, k=5):
    dist_matrix = {}
    for i, labeled_doc in enumerate(labeled_docs):
        cosine_similarity = calc_similarity(vec1=labeled_doc.terms, vec2=doc.terms)
        if cosine_similarity == 1:
            doc.category = labeled_doc.category
            return
        dist_matrix[i] = cosine_similarity  # todo check for validity of tuples as dictionary key

    k_n_neighbour = pop_best_k(dist_matrix, K)
    doc.category = most_frequent(
        [labeled_docs[k_n_neighbour[i]].category for i in range(len(k_n_neighbour))])  # for knn with k = K


def most_frequent(lst):
    return max(set(lst), key=lst.count)
