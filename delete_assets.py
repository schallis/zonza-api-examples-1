#!/usr/bin/env python
import os
import requests
import json
import sys

from pprint import pprint

SITE = 'deluxe.zonza.tv'
USER = 'deluxeuser@deluxe.com'

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
for page in xrange(1, 10):
    print "Deleting page", page
    response = requests.get(
        '{}item?zonza_site={}&user={}&__page={}'.format(url,
            SITE, USER, page),
        headers=headers)
    json_response = json.loads(response.content)
    print pprint(json_response)
    print json_response['hits']
    for item in json_response['item']:
        item_url = item['url']
        print item_url
        delete_response = requests.delete(item_url, headers=headers)
        print delete_response

