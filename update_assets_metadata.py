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

PAGE_SIZE = 100
SITE = 'fox.zonza.tv'
FIELD = 'fox_brand'
OLD = '4094'
NEW = 'LETS BE COPS'

items = []
hits = 0
page = 1
pages = 2
while page < pages:
    print "Updating", page
    response = requests.get(
        '{}item?zonza_site={}&{}={}&__page={}&__page_size={}'.format(
            url, SITE, FIELD, OLD, page, PAGE_SIZE),
        headers=headers)
    json_response = json.loads(response.content)
    print pprint(json_response)
    hits = int(json_response['hits'])
    pages = 1 + (hits // PAGE_SIZE)
    items.extend(json_response['item'])

print hits


# Update after retieving all items to avoid modifying the paginated results
# whilst iterating

for item in items:
    item_url = item['url'] + '/metadata'
    print item_url
    new_data = {FIELD: NEW}
    update_response = requests.post(
            item_url,
            data=json.dumps(new_data),
            headers=headers)
    print update_response
