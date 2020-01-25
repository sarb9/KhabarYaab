from optimzation.similarity import calc_similarity, pop_best_k


def knn(labeled_docs, all_docs_weights, K):
    """
    label whole dataset based on limited labeled docs
    :param labeled_docs: limited labeled documents, list of tuples : [(docID, Label), ...]
    :param all_docs_weights: whole dataset containing labeled ones, list of vectors
    :return:
    """

    categories = []
    for i in range(len(all_docs_weights)):
        dist_matrix = {}
        already_labeled = False  # to prevent calculating the already labeled docs
        for labeled_doc in labeled_docs:
            cosine_similarity = calc_similarity(vec1=all_docs_weights[labeled_doc[0]], vec2=all_docs_weights[i].vector)
            if cosine_similarity == 1:
                categories.append(labeled_doc[1])
                already_labeled = True
                break
            dist_matrix[labeled_doc] = cosine_similarity  # todo check for validity of tuples as dictionary key

        if already_labeled:  # to prevent calculating the already labeled docs
            continue

        k_nearest_neighbour = pop_best_k(dist_matrix, K)
        categories.append(most_frequent(
            [k_nearest_neighbour[i].label for i in range(len(k_nearest_neighbour))]))  # for knn with k = K

    return categories


def most_frequent(lst):
    return max(set(lst), key=lst.count)


print()
