from ling_modules import lemmatizer, normalizer, pipline, stemmer, tokenizer
from models.news_model import NewsModel
import pickle, os.path
from dictionary.posting import Posting
from collections import namedtuple
from dictionary import dictionary, posting

from ling_modules import pipline, normalizer, tokenizer, stemmer

Occurance = namedtuple('Occurance', ['term', 'posting'])


class Indexer:

    def __init__(self):
        self.index = []
        self.pipline = pipline.Pipeline(
            normalizer.Normalizer(), tokenizer.Tokenizer(), stemmer.Stemmer())

    def feed(self, models):
        for model in models:
            tokens = self.pipline.feed(model.content)
            for i, term in enumerate(tokens):
                self.index.append(Occurance(term, Posting(model.id, i)))

    def create_dictionary(self, from_scratch):

        def save_dictionary(dct):
            with open('data/dictionary_obj.pkl', 'wb') as output:
                pickle.dump(dct, output, pickle.HIGHEST_PROTOCOL)

        def load_dictionary():
            with open('data/dictionary_obj.pkl', 'rb') as input_file:
                return pickle.load(input_file)

        if not from_scratch and os.path.exists('data/dictionary_obj.pkl'):
            return load_dictionary()
        self.index.sort()
        dct = dictionary.Dictionary()

        prev = None
        prev_d = None
        poslist = posting.PostingList()
        for occ in self.index:

            if occ.term != prev and prev != None:
                poslist.df = poslist.df
                prev_d = None
                dct[prev] = poslist
                poslist = posting.PostingList()

            if prev_d != occ.posting.doc_id:
                poslist.df += 1
                prev_d = occ.posting.doc_id

            poslist.add_posting(occ.posting)
            prev = occ.term

        # add last word to the dictionary
        poslist.df = poslist.df
        dct[prev] = poslist
        save_dictionary(dct)
        return dct
