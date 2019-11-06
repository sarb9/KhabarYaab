from ling_modules.normalizer import Normalizer
from ling_modules.lemmatizer import Lemmatizer
from ling_modules.tokenizer import Tokenizer
from ling_modules.stemmer import Stemmer


class Pipeline():

    def __init__(self, *args):
        self.modules = list(args)

    def add(self, *args):
        self.modules.append(list(args))

    def feed(self, text):
        for module in self.modules:
            text = module(text)
        return text
