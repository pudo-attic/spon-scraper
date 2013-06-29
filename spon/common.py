import dataset
import os
import logging

requests_log = logging.getLogger("requests")
requests_log.setLevel(logging.WARNING)

assert 'DATABASE_URI' in os.environ, 'No DATABASE_URI is set!'
engine = dataset.connect(os.environ['DATABASE_URI'])
articles = engine.get_table('articles')
keywords = engine.get_table('keywords')
