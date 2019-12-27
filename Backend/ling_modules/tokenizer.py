from hazm import word_tokenize, sent_tokenize
import re
from ling_modules.pipline import Pipeline


class Tokenizer:

    def word_tokenize(self, text):
        return word_tokenize(text)

    def sent_tokenize(self, text):
        return sent_tokenize(text)

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
            return text.split()

        tokenization_pipeline = Pipeline(remove_punctuations, split_by_space)
        return tokenization_pipeline.feed(text=text)

    def __call__(self, text):
        return word_tokenize(text)
