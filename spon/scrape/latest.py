import logging
from lxml import html
from urlparse import urljoin
import requests
from thready import threaded
from spon.scrape.articles import scrape_article

log = logging.getLogger(__name__)
BASE_URL = 'http://www.spiegel.de/schlagzeilen/index-siebentage.html'


def get_latest():
    res = requests.get(BASE_URL)
    doc = html.fromstring(res.content)
    seen = set()
    for a in doc.cssselect('.schlagzeilen-content a'):
        url = urljoin(BASE_URL, a.get('href'))
        if url not in seen:
            yield url
        seen.add(url)


if __name__ == "__main__":
    get_latest()
    threaded(get_latest(), scrape_article, num_threads=10)
