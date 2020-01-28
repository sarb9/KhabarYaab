import pickle
import os.path
from collections import namedtuple

import matplotlib.pyplot as plt

from ling_modules import lemmatizer, normalizer, pipline, stemmer, tokenizer
from models.news_model import NewsModel
from dictionary import dictionary, posting
from dictionary.document import Document

from ling_modules import pipline, normalizer, tokenizer, stemmer

Occurance = namedtuple('Occurance', ['term', 'posting'])

STOP_WORDS = ("چه", "اگر", "همه", "نه", "آنها",
              "باید", "هر", "او", "ما", "من", "تا",
              "نیز", "اما", "یک", "خود", "بر",
              "یا", "هم", "را", "این", "با", "آن", "برای", "و", "در", "به", "که", "از")


class Indexer:

    def __init__(self):
        self.index = []
        self.dct = dictionary.Dictionary()
        self.pipline = pipline.Pipeline(
            normalizer.Normalizer(), tokenizer.Tokenizer(), stemmer.Stemmer())

    def feed(self, models, force=False, for_labeled_data=False):

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
            if for_labeled_data:
                doc.category = model.category
            self.dct.add_doc(doc)

            for i, term in enumerate(tokens):
                self.index.append(
                    Occurance(term, posting.Posting(model.id, i)))

        fig = plt.figure()
        plt.plot(range(len(models)), heaps_law)
        fig.savefig('statistics/heaps.png', dpi=fig.dpi)

    def create_dictionary(self, force=False, labeled_vectors=None, for_crawler=False):

        def save_dictionary(dct):
            with open('data/dictionary_obj.pkl', 'wb') as output:
                pickle.dump(dct, output, pickle.HIGHEST_PROTOCOL)

        def load_dictionary():
            with open('data/dictionary_obj.pkl', 'rb') as input_file:
                return pickle.load(input_file)

        if not force and os.path.exists('data/dictionary_obj.pkl'):
            return load_dictionary()

        # sort documents
        self.index.sort()

        # calculate document frequencies
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

        # calculate tf-idf then cluster and categorize documents
        self.dct.calc_doc_tf_idf()
        if labeled_vectors is None or for_crawler:
            return self.dct

        print("clustering ...")
        self.dct.calc_clusters()

        print("classification ...")
        self.dct.calc_categories(labeled_docs=labeled_vectors)

        # zipfs law
        word_freqs = {len(posting_list): None
                      for word, posting_list in self.dct.data.items()}

        zipfs = list(word_freqs.keys())
        zipfs.sort(reverse=True)
        fig = plt.figure()
        plt.plot(range(len(zipfs)), zipfs)
        fig.savefig('statistics/zipfs.png', dpi=fig.dpi)

        # delete stop words after zipfs law
        for stop_word in STOP_WORDS:
            if stop_word in self.dct:
                del self.dct[stop_word]

        # save and return at the end
        if save_dictionary:
            save_dictionary(self.dct)
        return self.dct
