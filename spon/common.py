import dataset
import os
import logging

requests_log = logging.getLogger("requests")
requests_log.setLevel(logging.WARNING)

assert 'DATABASE_URI' in os.environ, 'No DATABASE_URI is set!'
engine = dataset.connect(os.environ['DATABASE_URI'])
articles = engine.get_table('articles')
keywords = engine.get_table('keywords')

WORK_DATA = os.environ.get('WORK_PATH', 'data')
if not os.path.isdir(WORK_DATA):
    os.makedirs(WORK_DATA)


def data_path(file_name):
    return os.path.join(WORK_DATA, file_name)
