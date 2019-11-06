import hazm


class Lemmatizer:

    def __init__(self):
        self.lemmatizer = hazm.Lemmatizer()

    def lemmatize(self, text):
        return self.lemmatizer.lemmatize(text)

    def __call__(self, text):
        return self.lemmatizer.lemmatize(text)
