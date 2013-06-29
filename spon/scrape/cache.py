import requests
from requests.structures import CaseInsensitiveDict
import hashlib
import os
import json


class FakeResponse(object):

    def __init__(self, data):
        self.data = data
        self.headers = CaseInsensitiveDict(data.get('headers'))
        self.status_code = data.get('status_code')
        self.content = data.get('content')


def cache_path(url):
    cache_dir = os.environ.get('CACHE_PATH', 'articles')
    if not os.path.isdir(cache_dir):
        os.makedirs(cache_dir)
    fname = hashlib.sha1(url).hexdigest()
    return os.path.join(cache_dir, fname)


def cached_get(url, force_reload=False, *a, **kw):
    path = cache_path(url)
    data = None
    if not os.path.isfile(path) or force_reload:
        res = requests.get(url, *a, **kw)
        data = {
            'content': res.content.decode('latin-1'),
            'status_code': res.status_code,
            'headers': res.headers.items()
        }
        with file(path, 'wb') as fh:
            json.dump(data, fh)
    if data is None:
        with file(path, 'rb') as fh:
            data = json.load(fh)
    return FakeResponse(data)
