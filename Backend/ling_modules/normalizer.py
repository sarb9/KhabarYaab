import hazm


class Normalizer:
    def __init__(self):
        self.normalizer = hazm.Normalizer()

    def normalize(self, text):
        return self.normalizer.normalize(text)

    def __call__(self, text):
        return self.normalizer.normalize(text)