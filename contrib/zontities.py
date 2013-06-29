import requests
from pprint import pprint
import os
from itertools import count

PAGE_SIZE = 100
BASE_URL = "http://api.zeit.de/keyword"
API_KEY = os.environ.get('ZON_KEY')

def get_entities():
    for i in count(0):
        p = {'limit': PAGE_SIZE, 'offset': i*PAGE_SIZE, 'api_key': API_KEY}
        res = requests.get(BASE_URL, params=p)
        for match in res.json().get('matches'):
            print [match.get('value')]
            #pprint(match)
        if i*PAGE_SIZE > res.json().get('found'):
            break

if __name__ == "__main__":
    get_entities()



