from hazm import word_tokenize, sent_tokenize


class Tokenizer:

    def word_tokenize(self, text):
        return word_tokenize(text)

    def sent_tokenize(self, text):
        return sent_tokenize(text)

    def __call__(self, text):
        return word_tokenize(text)
