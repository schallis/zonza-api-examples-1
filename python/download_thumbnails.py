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

print 'searching...'
headers = {'content-type': 'application/json'}
headers.update(auth)
with open('/Users/stevenchallis/common-mapped', 'r') as common:
    for item in common:
        ITEM = item.split(' ', 1)[0]
        path = 'http://api.zonza.tv:8080/v0/item/{}/thumbnail/0'.format(ITEM)
        print path
        response = requests.get(path,
            headers=headers)
        with open('thumbs/{0}.png'.format(ITEM), 'wb') as f:
            f.write(response.content)
