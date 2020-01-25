import matplotlib.pyplot as plt
import random
from .similarity import calc_similarity


def kmeans(docs_weights, k):
    clusters_centers = []
    clusters_values = []

    for _i in range(4):
        if _i == 0:
            # choose centers randomly
            for i in range(k):
                clusters_centers.append(random.choice(docs_weights))
                clusters_values.append([])
        else:
            # calc new centers
            new_clusters_centers = []
            new_clusters_values = []
            for one_cluster in clusters_values:
                avg = {}
                for vector in one_cluster:
                    for term in vector:
                        added_value = vector[term] / len(one_cluster)
                        if term not in avg:
                            avg[term] = added_value
                        else:
                            avg[term] = avg[term] + added_value

                new_clusters_centers.append(avg)
                new_clusters_values.append([])

            clusters_centers = new_clusters_centers
            clusters_values = new_clusters_values

        # assgin vectors to members
        for vector in docs_weights:
            max_similarity = 0
            best_center_index = 0
            for center_index in range(len(clusters_centers)):
                sim = calc_similarity(clusters_centers[center_index], vector)
                if sim > max_similarity:
                    best_center_index = center_index
                    max_similarity = sim
            clusters_values[best_center_index].append(vector)

    return clusters_centers, clusters_values


def error_function(clusters_centers, clusters_values, docs_no=0):
    error = 0
    for i in range(len(clusters_centers)):
        for j in range(len(clusters_values[i])):
            error += 1 - calc_similarity(clusters_values[i][j], clusters_centers[i])
    if docs_no == 0:
        return error
    else:
        return error / docs_no

    # error += calc_similarity(member, center)
    # return error


def plot_k_errors(k, errors):
    plt.plot(k, errors, "bo")
    plt.show()


def define_best_cluster_number(docs_weights):
    k = []
    errors = []
    for cluster_number in range(9, 13, 2):
        cluster_centers, cluster_values = kmeans(docs_weights, cluster_number)
        errors.append(error_function(cluster_centers, cluster_values, docs_no=len(docs_weights)))
        k.append(cluster_number)
    print("k:     ", k)
    print("errorrrr:    ", errors)
    plot_k_errors(k, errors)
    cluster_number = int(input("it seems thr best number of clusters is: "))
    return cluster_number
