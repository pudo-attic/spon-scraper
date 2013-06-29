from spon.extract.normalize import normalize
import os

STOPFILE = os.path.join(os.path.dirname(__file__), 'stopwords.de.txt')
STOPWORDS = normalize(open(STOPFILE).read().decode('utf-8')).split()


def tokens_to_bigrams(tokens):
    last_token = None
    for token in tokens:
        if last_token is not None:
            yield '%s_%s' % (last_token, token)
        last_token = token


def tokenize(text):
    for token in normalize(text).split(' '):
        if not len(token) or token in STOPWORDS:
            continue
        yield token


def make_bigrams(text):
    tokens = tokenize(text)
    bigrams = tokens_to_bigrams(tokens)
    return bigrams


if __name__ == '__main__':
    print make_bigrams('Ich bin also eine Banane!')
