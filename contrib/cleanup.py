#coding: utf-8
from pprint import pprint
from datetime import datetime
import sqlaload as sl

from threaded import threaded

DE_MONTHS = {
    u"Januar": "01",
    u"Februar": "02",
    u"März": "03",
    u"April": "04",
    u"Mai": "05",
    u"Juni": "06",
    u"Juli": "07",
    u"August": "08",
    u"September": "09",
    u"Oktober": "10",
    u"November": "11",
    u"Dezember": "12"
    }

def articles(engine):
    a_table = sl.get_table(engine, 'article')
    for data in sl.find(engine, a_table):
        up = {'number': data['number']}
        slug_parts = data['canonical_url'].split('/')[3:]
        if len(slug_parts) > 3:
            print slug_parts
        if len(slug_parts) == 3:
            up['ressort'], up['subressort'], _ = slug_parts
        elif len(slug_parts) == 2:
            up['ressort'], _ = slug_parts
        up['date'] = parse_date(data['date_text'])
        sl.upsert(engine, a_table, up, ['number'])


def parse_date(date_text):
    for name, num in DE_MONTHS.items():
        date_text = date_text.replace(name, num)
    date_text = date_text.replace(u"\xa0Uhr", "")
    date_text = date_text.replace("31. 09", "30. 09")
    try:
        return datetime.strptime(date_text, "%d. %m %Y, %H:%M")
    except ValueError, ve:
        return datetime.strptime(date_text, "%m/%d/%Y %H:%M %p")


    print [date_text]

if __name__ == "__main__":
    engine = sl.connect('postgresql://localhost/spon_scrape')
    articles(engine)


