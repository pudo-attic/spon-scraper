#coding: utf-8
import logging
from dateutil.parser import parse

log = logging.getLogger(__name__)


def clean_article(data):

    try:
        slug_parts = data['article_url'].split('/')[3:]
        if len(slug_parts) > 3:
            print slug_parts
        if len(slug_parts) == 3:
            data['ressort'], data['subressort'], _ = slug_parts
        elif len(slug_parts) == 2:
            data['ressort'], _ = slug_parts
    except Exception, e:
        log.exception(e)

    data['last_modified'] = parse(data['last_modified'])
    data['date'] = parse(data['date'])
    return data
