import logging
from lxml import html
import requests
import re
from pprint import pprint
from spon.common import engine, articles, keywords
from spon.common import article_links, topic_links, external_links
from spon.scrape.cache import cached_get
from spon.scrape.clean import clean_article

log = logging.getLogger(__name__)
EXTRACT_NUMBER = re.compile('-(\d+).html$')
SITE_URL = 'http://www.spiegel.de/'
SKIP_METAS = ['mssmarttagspreventparsing', 'email', 'author',
              'twitter_card', 'twitter_site', 'og_site_name',
              'og_type']


def path_text(doc, selector):
    els = doc.cssselect(selector)
    if not len(els):
        log.warn("Couldn't find: %s in %s", selector, doc.url)
        return
    text = els.pop()
    for tag in ['iframe', 'script', 'div']:
        for el in text.findall('.//' + tag):
            #print "DELETING", el, [el.xpath('string()').strip()]
            el.getparent().remove(el)
    return text.xpath('string()').strip()


def save_keywords(number, value):
    keywords.delete(number=number)
    for k in value.split(','):
        k = k.strip()
        if len(k):
            data = {'keyword': k, 'number': number}
            keywords.insert(data)


def save_links(number, doc):
    article_links.delete(number=number)
    topic_links.delete(number=number)
    external_links.delete(number=number)

    for link in doc.findall('.//a'):
        href = link.get('href')
        data = {
            'number': number,
            'text': link.text,
            'href': href,
            'title': link.get('title'),
        }
        if href is None or 'http://forum.spiegel.de' in href:
            continue
        if 'text-link-ext' in link.get('class', '') and SITE_URL not in href:
            external_links.insert(data)
        elif 'text-link-int' in link.get('class', '') or SITE_URL in href:
            if '/thema/' in href:
                thema_name = href.rsplit('/', 1)[-1]
                data['topic'] = thema_name
                topic_links.insert(data)
            else:
                data['href_number'] = url_to_number(href)
                article_links.insert(data)


def url_to_number(article_url):
    if '/video/' in article_url:
        return 0
    m = EXTRACT_NUMBER.search(article_url)
    if m is None:
        #return log.error("Cannot get article ID from: %s", article_url)
        return
    return int(m.groups()[0])


def scrape_article(article_url, number=None, force=True):
    if not force and articles.find_one(article_url=article_url):
        return
    #engine.begin()

    if number is None:
        number = url_to_number(article_url)

    if 'spiegel.de/spam' in article_url:
        return log.info("Won't scrape SPAM.")

    data = {'article_url': article_url, 'number': number}
    response = cached_get(article_url, force_reload=force, allow_redirects=False)
    if response.status_code >= 400 or 'location' in response.headers:
        return log.error("Cannot download article: %s (error: %s)",
                         article_url, response.status_code)

    doc = html.document_fromstring(response.content)
    doc.url = article_url
    #data['raw'] = response.content.decode('utf-8', 'ignore')
    data['headline_intro'] = path_text(doc, 'h2.article-title span.headline-intro')
    data['headline'] = path_text(doc, 'h2.article-title span.headline')
    data['date_text'] = path_text(doc, '.article-function-box .article-function-date')
    forum_el = doc.cssselect('.article-function-forum a')
    if len(forum_el):
        data['forum_url'] = forum_el.pop().get('href')
    data['teaser_text'] = path_text(doc, 'p.article-intro strong')
    data['body_text'] = path_text(doc, 'div.article-section')

    for meta in doc.findall('.//head/meta'):
        name = meta.get('name', meta.get('property', '')).lower().strip()
        name = name.replace(':', '_').replace('-', '_')
        value = meta.get('content', meta.get('value', '')).strip()
        if not len(name) or name in SKIP_METAS or not len(value):
            continue
        if name == 'keywords':
            save_keywords(number, value)
        else:
            data[name] = value

    save_links(number, doc)
    data = clean_article(data)
    articles.upsert(data, ['number'])
    #pprint(data)
    #engine.commit()
    log.info("Got: %s, %s %s", number, data['headline_intro'], data['headline'])
