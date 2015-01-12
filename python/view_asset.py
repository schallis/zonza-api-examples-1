#!/usr/bin/env python
import os
import requests
import json
import sys

from pprint import pprint

ITEM = 'VX-336639'

url = 'http://api.zonza.tv:8080/v0/'

def raise_invalid():
    raise RuntimeError('Credentials not configured. Please set ' \
                       'env variables BORK_TOKEN and BORK_USERNAME')

auth = {
    'Bork-Token': os.environ.get("BORK_TOKEN") or raise_invalid(),
    'Bork-Username': os.environ.get("BORK_USERNAME") or raise_invalid(),
}

print 'searching...'
headers = {'content-type': 'application/json'}
headers.update(auth)
response = requests.get(
    '{}item/{}'.format(url, ITEM),
    headers=headers)
json_response = json.loads(response.content)
print pprint(json_response)

