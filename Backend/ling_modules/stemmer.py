from collections.abc import Iterable

import hazm
from PersianStemmer import PersianStemmer


class Stemmer:

    def __init__(self):
        self.stemmer = PersianStemmer()

    def stem(self, text):
        return self.stemmer.stem(text)

    def __call__(self, text):
        if isinstance(text, list):
            return [self.stemmer.stem(t) for t in text]
        else:
            return self.stemmer.stem(text)
