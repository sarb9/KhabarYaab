from array import array
from collections import UserDict


class Document:

    def __init__(self, tokens):
        self.terms = {}
        self.cluster = None
        self.id = None
        # self.vector= {}
        self.category = None
        for token in tokens:
            self.add_token(token)

    def set_vector(self, vector):
        # self.vector = vector
        self.terms = vector

    def add_token(self, token):
        if token in self.terms.keys():
            self.terms[token] += 1
        else:
            self.terms[token] = 1

    def set_id(self, id):
        self.id = id
