import sys

from stemmer import Stemmer
from tokenizer import Tokenizer
from lemmatizer import Lemmatizer
from normalizer import Normalizer
from pipline import Pipeline


if __name__ == "__main__":
    inp = sys.stdin.read()

    print(inp)

    pipeline = Pipeline(Normalizer(), Stemmer(), Tokenizer(), print_res=True)
    res = pipeline.feed(inp)
    print(res)

    pipeline = Pipeline(Normalizer(), Tokenizer(), Stemmer())
    res = pipeline.feed(inp)
    print(res)
