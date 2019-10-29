from normalizer import Normalizer
from lemmatizer import Lemmatizer
from tokenizer import Tokenizer
from stemmer import Stemmer


class Pipeline():

    def __init__(self, *args, print_res=False):
        self.modules = list(args)
        self.print_res = print_res

    def add(self, *args):
        self.modules.append(list(args))

    def feed(self, text):
        for module in self.modules:
            text = module(text)
            if self.print_res:
                print(text)
        return text
