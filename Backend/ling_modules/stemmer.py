import pickle
import re
from ling_modules.tokenizer import load_from_file

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
        self.verb_stems = load_stem_pickle()
        self.irregular_nouns = load_from_file(load_path="ling_modules/resources/irregular_nouns", delimiter="\t")
        self.other_suffix = ["(.*)(ی$)", "(.*)(ای$)", "(.*)(ان$)", "(.*)(ها$)"]
    def stem(self, term):
        def check_verb_stem(term):
            legal_verb_affix = ["(وا)(.*)", "(اثر)(.*)", "(فرو)(.*)", "(پیش)(.*)", "(گرو)(.*)",
                                "(.*)(گار)", "(.*)(چه)"]  # we want to keep them
            for legal_affix in legal_verb_affix:
                if re.search(legal_affix, term):
                    for suffix in self.other_suffix:
                        term = re.sub(pattern=suffix, repl=r"\1", string=term)  # remove other_suffix from word
                    return True, term

            # for Mazi and Mozare Sade
            sade_pattern = "([م$|ی$|د$|یم$|ید$|ند$])"
            # for Mazi Naghli
            naghli_pattern = "ه" + "\u200c" + "([ام$|ای$|است$|ایم$|اید$|اند$])"

            # prefix
            prefix_pattern = "^می|^ب"
            if re.search(sade_pattern + r"|" + naghli_pattern + r"|" + prefix_pattern, term):
                for verb in self.verb_stems:
                    if verb in term:
                        return True, verb

            return False, term

        def check_noun_stem(term):

            suffix = ["كار", "ناك", "وار", "آسا", "آگین", "بار", "بان", "دان", "زار", "سار", "سان", "لاخ", "مند", "دار",
                      "مرد", "کننده", "گرا", "وش", "نما"]
            prefix = ["بی", "با", "پیش", "غیر", "فرو", "هم", "نا", "یک"]

            flag = False

            noun_suffix_regex = []
            for suf in suffix:  # Create regex format from list
                noun_suffix_regex.append("(.*)(" + suf + ")")

            for suf in (self.other_suffix + noun_suffix_regex):
                if re.search(suf, term):
                    term = re.sub(pattern=suf, repl=r"\1", string=term)
                    flag = True

            noun_prefix_regex = []
            for pre in prefix:  # Create regex format from list
                noun_prefix_regex.append("(" + pre + ")(.*)")

            for pre in noun_prefix_regex:
                if re.search(pre, term):
                    term = re.sub(pattern=pre, repl=r"\2", string=term)
                    flag = True

            # check for irregular nouns
            if not flag and len(term) >= 5:
                for raw in self.irregular_nouns:
                    if term == raw[0]:
                        return raw[1]

            return term

        is_verb, term = check_verb_stem(term)
        if not is_verb:
            term = check_noun_stem(term)

        # print("Term : " + term)
        return term.strip("\u200c")

    def __call__(self, text):
        if isinstance(text, list):
            return [self.stem(t) for t in text]
        else:
            return self.stem(text)



def load_stem_pickle():
    """
    load verb stems from .pckl file
    """
    load_path = "ling_modules/resources/verb_stems.pckl"
    file = open(load_path, 'rb')
    stems = pickle.load(file)
    file.close()
    return stems

# stemmer = Stemmer()
# stemmer.stem("می‌روم")
# def load_from_text():
#     load_path = "ling_modules/resources/Verb_stemss.txt"
#     verbs = load_from_file(load_path, "\t")
#     vvv=[]
#     for row in verbs:
#         vvv.append(row[0])
#         vvv.append(row[1])
#
#     with open('ling_modules/resources/verb_stems.pckl', 'wb') as fp:
#         pickle.dump(vvv, fp)
#
#     print()
#
# load_from_text()
