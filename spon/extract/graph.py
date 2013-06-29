import math
import json
import networkx as nx
from spon.common import articles, data_path
from collections import defaultdict
from itertools import combinations
from spon.extract.tfidf import load_idf_model, article_terms
from pprint import pprint


def topic_graph():
    print "Loading IDF model..."
    model = load_idf_model('tokens')
    print "Making a graph..."
    #articles = 0
    edges = defaultdict(int)
    for article in articles.find(_limit=10000):
        if 'spiegel.de/international' in article['article_url']:
            continue
        terms = article_terms(model, article)[:15]
        for (term1, score1), (term2, score2) in combinations(terms, 2):
            key = max(term1, term2), min(term1, term2)
            edges[key] += score1 * score2

    G = nx.Graph()
    #for (s, d), w in edges.items():
    for (s, d), w in sorted(edges.items(), key=lambda (a, b): b, reverse=True)[:20000]:
        G.add_edge(s, d, weight=w)
    nx.write_gexf(G, data_path('topic_graph_abridged.gexf'))
    #print "Sorting..."
    #ranked = sorted(edges.items(), key=lambda (a, b): b, reverse=True)
    #pprint(ranked[:10])


if __name__ == '__main__':
    topic_graph()
