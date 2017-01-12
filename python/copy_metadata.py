#!/usr/bin/env python
SITE = 'demo.zonza.tv'
import os
import requests
import json
import sys
import time

from pprint import pprint

"""
Copy metadata from one field to another on an input list of VX ID's
"""

SITE = 'grey.zonza.tv'
PAGE_SIZE = 100

url = os.environ.get('BORK_URL') or 'http://api.zonza.tv:8080/v0/'

def raise_invalid():
    raise RuntimeError('Credentials not configured. Please set ' \
                       'env variables BORK_TOKEN and BORK_USERNAME')

auth = {
    'Bork-Token': os.environ.get("BORK_TOKEN") or raise_invalid(),
    'Bork-Username': os.environ.get("BORK_USERNAME") or raise_invalid(),
}

headers = {'content-type': 'application/json'}
headers.update(auth)

# Update a single item with a single new metadata value
def update_field(item, field_name, field_value):
    item_url = url + 'item/' + item + '/metadata'
    new_data = {
        field_name: field_value,
    }
    response = requests.get(
            item_url, headers=headers)
    json_response = json.loads(response.content)
    print "Old value for {} is {}".format(field_name, json_response.get(field_name))
    print 'Setting {} to {} for {}'.format(field_name, field_value, item)
    update_response = requests.post(
            item_url,
            data=json.dumps(new_data),
            headers=headers)
    print update_response, item_url
    if str(update_response.status_code).startswith('4'):
        print update_response.content


def copy_metadata(item, from_field, to_field):
    item_url = url + 'item/' + item + '/metadata'
    response = requests.get(item_url, headers=headers)
    metadata = json.loads(response.content)

    from_data = metadata.get(from_field)
    to_data = metadata.get(to_field)
    print "{} > {} - {}".format(item, from_data, to_data)
    if from_data and not to_data:
        print "moving old into new..."
        update_field(item, to_field, from_data)
        print "DONE"


# Return a list of assets matching field criteria
def search_items():
    items = []
    hits = 0
    page = 1
    pages = 1
    while page <= pages:
        response = requests.get(
            '{}item?zonza_site={}&zonza_supporting_file_master=&__page={}&__page_size={}&greys_region=NA&greys_Agency=Grey'.format(url,
                SITE, page, PAGE_SIZE),
            headers=headers)
        json_response = json.loads(response.content)
        hits = int(json_response['hits'])

        if page == 1:
            print "For site:", SITE
            print json_response
            print "# of assets:", hits
        else:
            print "...Continuing to page", page

        for item in json_response['item']:
            items.append(item['id'])

        pages = 1 + (hits // PAGE_SIZE)
        page += 1

    return items



with open('items', 'r+') as f:
    # NEW SEARCH
    #items = search_items()
    #f.writelines('\n'.join(items))

    # READ FROM FILE
    items = f.read().splitlines()

    for item in items:
        update_field(item, 'brand', 'TEST BRAND')
