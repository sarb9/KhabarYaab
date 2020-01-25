from math import sqrt
import heapq


def calc_similarity(vec1, vec2):
    if len(vec1) == 0 or len(vec2) == 0:
        return 0

    score = 0
    common_keys = list(set(vec1) & set(vec2))

    for term in common_keys:
        score += vec1[term] * vec2[term]

    return score / (calc_length(vec1) * calc_length(vec2))


def calc_length(vector):
    s = 0
    for tfidf in vector.values():
        s += tfidf ** 2
    return sqrt(s)


def pop_best_k(dct, k):
    k = min(k, len(dct))
    heap = [(-value, key) for key, value in dct.items()]
    largest = heapq.nsmallest(k, heap)
    largest = [(key, -value) for value, key in largest]

    return [i[0] for i in largest]
