import pickle
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

    def __call__(self, text):
        if isinstance(text, list):
            return [self.stem(t) for t in text]
        else:
            return self.stem(text)

    def stem(self, term):
        other_suffix = ["(.*)(ی$)", "(.*)(ای$)", "(.*)(ان$)", "(.*)(ها$)"]
        verb_stems = load_stem_pickle()
        irregular_nouns = load_irregular_noun()

        def check_verb_stem(term):
            legal_verb_affix = ["(وا)(.*)", "(اثر)(.*)", "(فرو)(.*)", "(پیش)(.*)", "(گرو)(.*)",
                                "(.*)(گار)"]  # we want to keep them
            for legal_affix in legal_verb_affix:
                if re.search(legal_affix, term):
                    for suffix in other_suffix:
                        term = re.sub(pattern=suffix, repl=r"\1", string=term)  # remove other_suffix from word
                    return True, term

            for verb in verb_stems:
                # for Mazi and Mozare Sade
                sade_pattern = verb + "([م|ی|د|یم|ید|ند])"
                # for Mazi Naghli
                naghli_pattern = verb + "ه" + "\u200c" + "([ام|ای|است|ایم|اید|اند])"
                if re.search(sade_pattern + r"|" + naghli_pattern, term):
                    return True, verb

            return False, term

        def check_noun_stem(term):
            # check for irregular nouns
            for raw in irregular_nouns:
                if term == raw[0]:
                    return raw[1]

            suffix = ["كار", "ناك", "وار", "آسا", "آگین", "بار", "بان", "دان", "زار", "سار", "سان", "لاخ", "مند", "دار",
                      "مرد", "کننده", "گرا", "وش", "نما"]
            prefix = ["بی", "با", "پیش", "غیر", "فرو", "هم", "نا", "یک"]

            noun_suffix_regex = []
            for suf in suffix:  # Create regex format from list
                noun_suffix_regex.append("(.*)(" + suf + ")")

            for suf in (other_suffix + noun_suffix_regex):
                term = re.sub(pattern=suf, repl=r"\1", string=term)

            noun_prefix_regex = []
            for pre in prefix:  # Create regex format from list
                noun_prefix_regex.append("(" + pre + ")(.*)")

            for pre in noun_prefix_regex:
                term = re.sub(pattern=pre, repl=r"\2", string=term)

            return term

        is_verb, term = check_verb_stem(term)
        if not is_verb:
            term = check_noun_stem(term)

        print("Term : " + term)
        return term.strip("\u200c")


def load_stem_pickle():
    """
    load verb stems from .pckl file
    """
    load_path = "ling_modules/resources/verb_stems.pckl"
    file = open(load_path, 'rb')
    stems = pickle.load(file)
    file.close()
    return stems


def load_irregular_noun():
    """
    load irregular nouns from .txt file
    """
    load_path = "ling_modules/resources/irregular_nouns"
    with open(load_path, "r") as file:
        nouns = []
        for line in file:
            nouns.append(line.strip().split("\t"))
    return nouns
