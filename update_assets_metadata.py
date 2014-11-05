#!/usr/bin/env python
import os
import requests
import json
import sys
import time

from pprint import pprint

PAGE_SIZE = 100
SITE = 'demo.zonza.tv'
FIELD = 'media_type'
OLD = 'OLD'
NEW = 'NEW'

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

# Public API requests are ratelimited to 10rps

items = []
hits = 0
page = 1
pages = 1
while page <= pages:
    response = requests.get(
        '{}item?zonza_site={}&{}={}&__page={}&__page_size={}&zonza_supporting_file_master='.format(
            url, SITE, FIELD, OLD, page, PAGE_SIZE),
        headers=headers)
    json_response = json.loads(response.content)
    hits = int(json_response['hits'])

    items.extend(json_response['item'])
    print "Page {}, {} item(s) found now".format(page, len(items))

    pages = 1 + (hits // PAGE_SIZE)
    page += 1

print "About to update", hits, "asset(s)..."
print "'{}' will be updated to '{}' for field '{}'".format(OLD, NEW, FIELD)

time.sleep(3)

# Update after retieving all items to avoid modifying the paginated results
# whilst iterating

# Multiprocessing! Warning: Vidispine facet indexes seem to lag

def update_field(item):
    item_url = item['url'] + '/metadata'
    new_data = {FIELD: NEW}
    update_response = requests.post(
            item_url,
            data=json.dumps(new_data),
            headers=headers)
    print update_response, item_url

from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool
pool = ThreadPool(10) # Sets the pool size
results = pool.map(update_field, items)
pool.close()
pool.join()

#for number, item in enumerate(items):
    #item_url = item['url'] + '/metadata'
    #new_data = {FIELD: NEW}
    #update_response = requests.post(
            #item_url,
            #data=json.dumps(new_data),
            #headers=headers)
    #print number, update_response, item_url
