from ling_modules import lemmatizer, normalizer, pipline, stemmer, tokenizer
import matplotlib.pyplot as plt
from models.news_model import NewsModel
import pickle
import os.path
from dictionary.posting import Posting
from collections import namedtuple
from dictionary import dictionary, posting
from dictionary.document import Document

from ling_modules import pipline, normalizer, tokenizer, stemmer

Occurance = namedtuple('Occurance', ['term', 'posting'])

STOP_WORDS = ("چه", "اگر", "همه", "نه", "آنها",
              "باید", "هر", "او", "ما", "من", "تا",
              "نیز", "اما", "یک", "خود", "بر",
              "یا", "هم", "را", "این", "با", "آن", "برای", "و", "در", "به", "که", "از")


# try:
#     case_folding.index(term)
#     termm = case_folding[1]
#     print(termm + "asdfasdfasdf")
# except:
#     termm = term
#     print(termm + "heeee")


class Indexer:

    def __init__(self):
        self.index = []
        self.dct = dictionary.Dictionary()
        self.pipline = pipline.Pipeline(
            normalizer.Normalizer(), tokenizer.Tokenizer(), stemmer.Stemmer())

    def feed(self, models, force=False):

        if not force and os.path.exists('data/dictionary_obj.pkl'):
            return

        # heaps law
        seen_words = set()
        heaps_law = []

        for model in models:
            tokens = self.pipline.feed(model.content)

            seen_words |= set(tokens)
            heaps_law.append(len(seen_words))

            doc = Document(tokens)
            self.dct.add_doc(doc)

            for i, term in enumerate(tokens):
                # termm = check_case_folding(term)
                self.index.append(Occurance(term, Posting(model.id, i)))

        fig = plt.figure()
        plt.plot(range(len(models)), heaps_law)
        fig.savefig('temp.png', dpi=fig.dpi)

        print("____+_+_+_+_+_+___________")

    def create_dictionary(self, from_scratch=False):

        def save_dictionary(dct):
            with open('data/dictionary_obj.pkl', 'wb') as output:
                pickle.dump(dct, output, pickle.HIGHEST_PROTOCOL)

        def load_dictionary():
            with open('data/dictionary_obj.pkl', 'rb') as input_file:
                return pickle.load(input_file)

        if not from_scratch and os.path.exists('data/dictionary_obj.pkl'):
            return load_dictionary()

        self.index.sort()

        prev = None
        prev_d = None
        poslist = posting.PostingList()
        for occ in self.index:

            if occ.term != prev and prev != None:
                poslist.df = poslist.df
                prev_d = None
                self.dct[prev] = poslist
                poslist = posting.PostingList()

            if prev_d != occ.posting.doc_id:
                poslist.df += 1
                prev_d = occ.posting.doc_id

            poslist.add_posting(occ.posting)
            prev = occ.term

        # add last word to the dictionary
        poslist.df = poslist.df
        self.dct[prev] = poslist

        self.dct.calc_tf_idf()

        # zips law
        print("ZIPFS:")
        word_freqs = {word: len(poss) for word, poss in self.dct.data.items()}
        word_freqs = {k: v for k, v in sorted(
            word_freqs.items(), key=lambda item: item[1])}
        for i, j in word_freqs.items():
            if j > 1000:
                print(i, j)

        for stop_word in STOP_WORDS:
            del self.dct[stop_word]

        save_dictionary(self.dct)
        return self.dct
