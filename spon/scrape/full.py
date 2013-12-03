import requests
from urlparse import urljoin
from thready import threaded
from spon.scrape.articles import scrape_article, url_to_number
from spon.scrape.latest import get_latest


def resolve_forward(num):
    redir_url = "http://www.spiegel.de/artikel/a-%s.html" % num
    redir_response = requests.head(redir_url)
    if redir_response.status_code >= 400:
        return
    article_url = urljoin(redir_url, redir_response.headers.get('location'))
    print [article_url]
    scrape_article(article_url, number=num, force=False)


def article_gen(num):
    while num > 0:
        yield num
        num -= 1


if __name__ == "__main__":
    max_id = max([url_to_number(u) for u in get_latest()])
    threaded(article_gen(max_id), resolve_forward, num_threads=20)
