from collections.abc import Iterable

from PersianStemmer import PersianStemmer

# CASE_FOLDING = (["تهران", "طهران"], ["زغال", "ذغال"], ["بلیت", "بلیط"])
CASE_FOLDING = (["تهران", "طهران"], ["زغال", "ذغال"], ["بلیت", "بلیط"], ["طوفان", "توفان"])


# CASE_FOLDING = (["تهران", "طهران"], ["زغال", "ذغال"])


def add_similars(phrase):
    for case in CASE_FOLDING:
        if phrase in case:
            return case
    return []


class Stemmer:

    def check_case_folding(self, term):
        for case_folding in CASE_FOLDING:
            if term in case_folding:
                print(case_folding[0], "yum yummyy, boood")
                return case_folding[0]

        return term

    def __init__(self):
        self.stemmer = PersianStemmer()

    def stem(self, text):
        return self.stemmer.run(text)

    def __call__(self, text):
        if isinstance(text, list):

            print("hereeeeeeeeeeeee")
            return [self.stemmer.stem(self.check_case_folding(t)) for t in text]
        else:
            print("oonjaii ke nabaud")
            return self.stemmer.stem(text)
