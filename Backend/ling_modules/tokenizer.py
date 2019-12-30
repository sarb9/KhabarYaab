import re
from ling_modules.pipline import Pipeline


class Tokenizer:

    def tokenize(self, text):
        def remove_punctuations(text):
            """
            remove all nun alphanumercial and non space char
            """
            return re.sub(r'[^\w\s]', '', text)

        def split_by_space(text):
            """
            extract tokens from text into a list
            """
            if " " in text:
                return text.split()
            else:
                return text

        def check_fp(text):
            """
            check for frequent patterns and uniform them
            """
            frequent_patterns = load_from_file(load_path="resources/frequent_patterns")
            for row in frequent_patterns:
                if text.find(row) != -1:
                    text = text.replace(row, space_to_zwnj(row))

            return text

        def check_cf(text):
            """
            check for case folding
            """
            case_foldings = load_from_file(load_path="resources/case_foldings", delimiter=",")
            for foldings in case_foldings:
                if text.find(foldings[1]) != -1:
                    text = text.replace(foldings[1], foldings[0])

            return text

        tokenization_pipeline = Pipeline(remove_punctuations, check_fp, check_cf, split_by_space)
        return tokenization_pipeline.feed(text=text)

    def __call__(self, text):
        return self.tokenize(text)


def load_from_file(load_path, delimiter="nothing"):
    """
    load irregular nouns from .txt file
    """
    with open(load_path, "r") as file:
        nouns = []
        if delimiter == "nothing":
            for line in file:
                nouns.append(line.strip())
            return nouns

        for line in file:
            nouns.append(line.strip().split(delimiter))
    return nouns


def space_to_zwnj(text):
    """
    convert space to \u200c character
    """
    return re.sub(r'[\s]', '\u200c', text)