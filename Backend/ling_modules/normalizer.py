import hazm


class Normalizer:

    def __init__(self):
        self.normalizer = hazm.Normalizer()

    def normalize(self, text):
        return self.normalizer.normalize(text)

    def __call__(self, text):
        if isinstance(text, list):
            print("here")
            return [self.normalizer.normalize(t) for t in text]
        else:
            return self.normalizer.normalize(text)
