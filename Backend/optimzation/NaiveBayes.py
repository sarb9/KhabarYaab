from optimzation.similarity import calc_similarity

categories = ["science", "culture-art", "politics", "economy", "social", "sport", "international", "multimedia"]


class NaiveBayes:
    def __init__(self, labeled_docs):
        self.class_prob = {}  # P(C)
        self.words_distribution = []  # P(X|C)

        total_docs = len(labeled_docs)
        for labeled in labeled_docs:  # calculating P(C)
            category = labeled.category
            if category in self.class_prob:
                self.class_prob[category] += 1 / total_docs
            else:
                self.class_prob[category] = 1 / total_docs

        for labeled in labeled_docs:
            terms = labeled.terms
            category = labeled.category
            for term in terms:
                if not term in self.words_distribution:
                    self.words_distribution[term] = dict()
                    self.words_distribution[term][category] = True  # Boolean Bayesian Network
                else:
                    self.words_distribution[term][category] = True  # Boolean Bayesian Network

    def ApplyNaiveBayes(self, unlabeled_data):
        for unlabeled in unlabeled_data:
            class_scores = {}  # score of belonging to each class
            for category in categories:
                class_scores[category] = 0  # Initialization for each unlabeled document belonging
            unlabeled_terms = unlabeled.terms
            for term in unlabeled_terms:
                if term in self.words_distribution:
                    for category in self.words_distribution[term]:
                        class_scores[category] += 1

            unlabeled.category = max(class_scores, key=class_scores.get)