from array import array
from collections import UserDict


class Document:

    def __init__(self, tokens):
        self.terms = {}
        for token in tokens:
            self.add_token(token)

    def set_vector(self, vector):
        self.vector = vector

    def add_token(self, token):
        if token in self.terms.keys():
            self.terms[token] += 1
        else:
            self.terms[token] = 1
