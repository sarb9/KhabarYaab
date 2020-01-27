from optimzation.similarity import calc_similarity, pop_best_k


def knn(labeled_docs, docs, K):
    """
    label whole dataset based on limited labeled docs
    :param labeled_docs: limited labeled documents, list of tuples : [(docID, Label), ...]
    :param all_docs_weights: whole dataset containing labeled ones, list of vectors
    :return:
    """

    for document in docs:
        dist_matrix = {}
        already_labeled = False  # to prevent calculating the already labeled docs
        for labeled_doc in labeled_docs:
            cosine_similarity = calc_similarity(vec1=labeled_doc.terms, vec2=document.terms)
            if cosine_similarity == 1:
                document.category = labeled_doc.category
                already_labeled = True
                break
            dist_matrix[labeled_doc] = cosine_similarity  # todo check for validity of tuples as dictionary key

        if already_labeled:  # to prevent calculating the already labeled docs
            continue

        k_nearest_neighbour = pop_best_k(dist_matrix, K)
        document.category = most_frequent(
            [k_nearest_neighbour.category for i in range(len(k_nearest_neighbour))])  # for knn with k = K


def most_frequent(lst):
    return max(set(lst), key=lst.count)
