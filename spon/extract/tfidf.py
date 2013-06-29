import math
import json
from spon.common import articles, data_path
from collections import defaultdict
from spon.extract.tokenize import make_bigrams, tokenize
from pprint import pprint


def load_articles(limit):
    for article in articles.find(_limit=limit):
        if 'spiegel.de/international' in article['article_url']:
            continue
        yield {
            'url': article['article_url'],
            'text': article['body_text'],
            'bigrams': list(make_bigrams(article['body_text'])),
            'tokens': list(tokenize(article['body_text']))
        }


def parse_articles(field):
    model = load_idf_model(field)
    print "Extracting..."
    #articles = 0
    for article in articles.find(_limit=400):
        print "\n\nDOCUMENT", article['article_url']
        most = article_terms(model, article)
        pprint(most[:5])
        #if i % 100 == 0:
        #    print "Done: %s" % i
        #articles += 1


def article_terms(model, article):
    terms = defaultdict(int)
    for token in tokenize(article['body_text']):
        terms[token] += 1

    total = float(sum(terms.values()))
    if total == 0:
        return []
    max_f = max(terms.values())/total
    #print "MAX", max_f, max(terms.values()), terms.values()
    tf_idfs = {}
    for term, count in terms.items():
        tf = 0.5 + ((0.5*(count/total))/max_f)
        tf_idfs[term] = tf * model['terms'].get(term, 0)

    return sorted(tf_idfs.items(), key=lambda (a, b): b, reverse=True)


def generate_idf_model():
    tokens_global = defaultdict(int)
    bigrams_global = defaultdict(int)
    print "Extracting..."
    articles = 0
    for i, article in enumerate(load_articles(50000)):
        for token in set(article['tokens']):
            tokens_global[token] += 1
        for bigram in set(article['bigrams']):
            bigrams_global[bigram] += 1
        if i % 100 == 0:
            print "Done: %s" % i
        articles += 1

    print "Calculating IDF..."
    for file_name, terms in (('tokens', tokens_global), ('bigrams', bigrams_global)):
        data = {'articles': articles}
        data['terms'] = dict()
        for term, count in terms.items():
            idf = math.log((articles/(1+count)))
            data['terms'][term] = idf

        with open(data_path('idf_%s.json' % file_name), 'wb') as fh:
            json.dump(data, fh)


def load_idf_model(type_):
    with open(data_path('idf_%s.json' % type_), 'rb') as fh:
        return json.load(fh)


if __name__ == '__main__':
    parse_articles('tokens')
