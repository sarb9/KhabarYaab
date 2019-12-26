from collections.abc import Iterable

from PersianStemmer import PersianStemmer


class Stemmer:

    def __init__(self):
        self.stemmer = PersianStemmer()

    def stem(self, text):
        return self.stemmer.run(text)

    def __call__(self, text):
        if isinstance(text, list):
            return [self.stemmer.run(t) for t in text]
        else:
            return self.stemmer.run(text)
