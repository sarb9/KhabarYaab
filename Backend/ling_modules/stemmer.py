import pickle
from PersianStemmer import PersianStemmer
import re
from ling_modules.pipline import Pipeline

# CASE_FOLDING = (["تهران", "طهران"], ["زغال", "ذغال"], ["بلیت", "بلیط"])
CASE_FOLDING = (["تهران", "طهران"], ["زغال", "ذغال"],
                ["بلیت", "بلیط"], ["طوفان", "توفان"])


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
                return case_folding[0]

        return term

    def __init__(self):
        self.stemmer = PersianStemmer()
        # print()

    def stem(self, text):
        return self.stemmer.run(text)

    def __call__(self, text):
        if isinstance(text, list):
            return [self.stemmer.stem(self.check_case_folding(t)) for t in text]
        else:
            return self.stemmer.stem(text)


def stemmer(term):
    other_prefix = ["(.*)(ی)", "(.*)(ای)", "(.*)(ان)", "(.*)(ها)"]
    verb_stems = load_stem_pickle()
    irregular_nouns = load_irregular_noun()

    def check_verb_stem(term):
        legal_verb_affix = ["(وا)(.*)", "(اثر)(.*)", "(فرو)(.*)", "(پیش)(.*)", "(گرو)(.*)",
                            "(.*)(گار)"]  # we want to keep them
        for legal_affix in legal_verb_affix:
            if re.search(legal_affix, term):
                for prefix in other_prefix:
                    term = re.sub(pattern=prefix, repl=r"\1", string=term)  # remove other_prefix from word
                return True, term

        #Todo: Verb Stemming need to be handled --->

        # for verb in verb_stems:
        #     if verb in term:
        #         return True, verb
        return False, term

    def check_noun_stem(term):
        # check for irregular nouns
        for raw in irregular_nouns:
            if term == raw[0]:
                return raw[1]

        suffix = ["كار", "ناك", "وار", "آسا", "آگین", "بار", "بان", "دان", "زار", "سار", "سان", "لاخ", "مند", "دار",
                  "مرد", "کننده", "گرا", "وش", "نما", "متر"]
        prefix = ["بی", "با", "پیش", "غیر", "فرو", "هم", "نا", "یک"]

        suffix_regex = []
        for suf in suffix:
            suffix_regex.append("(.*)(" + suf + ")")

        for suf in suffix_regex:
            term = re.sub(pattern=suf, repl=r"\1", string=term)

        prefix_regex = []
        for pre in prefix:
            prefix_regex.append("(" + pre + ")(.*)")

        for pre in prefix_regex:
            term = re.sub(pattern=pre, repl=r"\2", string=term)

        return term

    check_pos, term = check_verb_stem(term)
    if not check_pos:
        term = check_noun_stem(term)

    return term


def load_stem_pickle():
    """
    load verb stems from .pckl file
    """
    load_path = "resources/verb_stems.pckl"
    file = open(load_path, 'rb')
    stems = pickle.load(file)
    file.close()
    return stems


def load_irregular_noun():
    """
    load irregular nouns from .txt file
    """
    load_path = "resources/irregular_nouns"
    with open(load_path, "r") as file:
        nouns = []
        for line in file:
            nouns.append(line.strip().split("\t"))
    return nouns


stemmer("گندمزار")
