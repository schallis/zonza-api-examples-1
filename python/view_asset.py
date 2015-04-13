#!/usr/bin/env python
import os
import requests
import json
import sys

from pprint import pprint

url = 'http://api.zonza.tv:8080/v0/'

def raise_invalid():
    raise RuntimeError('Credentials not configured. Please set ' \
                       'env variables BORK_TOKEN and BORK_USERNAME')

auth = {
    'Bork-Token': os.environ.get("BORK_TOKEN") or raise_invalid(),
    'Bork-Username': os.environ.get("BORK_USERNAME") or raise_invalid(),
}

item = sys.argv[1]
if not item.startswith('VX-'):
    raise Exception('No VX ID specified')
print 'searching...'
headers = {'content-type': 'application/json'}
headers.update(auth)
response = requests.get(
    '{}item/{}'.format(url, item),
    headers=headers)
json_response = json.loads(response.content)
print pprint(json_response)

