#!/usr/bin/env python
import requests
import json
import os

from pprint import pprint

"""
Prints out the number of hits for a site and the first 10
"""
SITE = 'demo.zonza.tv'


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
    '{}item?zonza_site={}'.format(url, SITE),
    headers=headers)
json_response = json.loads(response.content)
print "For site:", SITE
print "# of assets:", json_response['hits']
print "First 10..."
for item in json_response['item'][:10]:
    item_url = item['url']
    print item_url

