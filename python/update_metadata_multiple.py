#!/usr/bin/env python
import os
import requests
import json
import sys
import time
import urllib

from pprint import pprint

"""
Update multiple metadata fields for multiple assets
"""

SITE = 'zonza.tv'
#CONVENTION = '{brand} {year} {campaign} {language} {media_type} {agency}'
PAGE_SIZE = 100

url = os.environ.get('BORK_URL') or 'http://api.zonza.tv:8080/v0/'

criteria = (
    # Field ID, Old Value,  New Value
    ('brand', 'TST', 'TEST'),
    ('agency', 'TST', 'TEST'),
)

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
    print "Old value is", json_response.get(field_name)
    print 'Setting {} to {} for {}'.format(field_name, field_value, item)
    update_response = requests.post(
            item_url,
            data=json.dumps(new_data),
            headers=headers)
    print update_response, item_url
    if str(update_response.status_code).startswith('4'):
        print update_response.content


def recalculate_title(item):
    field_name = 'title'
    item_url = url + 'item/' + item + '/metadata'

    # Get existing values
    response = requests.get(
            item_url, headers=headers)
    metadata= json.loads(response.content)
    #print "Old value is", metadata.get(field_name)  # title is not returned

    # Compute new title
    field_value = CONVENTION.format(**metadata)
    new_data = {
        field_name: field_value,
    }

    # Set title
    print 'Setting {} to {} for {}'.format(field_name, field_value, item)
    update_response = requests.post(
            item_url,
            data=json.dumps(new_data),
            headers=headers)
    print update_response, item_url
    if str(update_response.status_code).startswith('4'):
        print update_response.content

# Return a list of assets matching field criteria
def search_items(field_name, field_value):
    items = []
    hits = 0
    page = 1
    pages = 1
    while page <= pages:
        response = requests.get(
            '{}item?zonza_site={}&{}={}&zonza_supporting_file_master=&__page={}&__page_size={}'.format(url,
                SITE, field_name, field_value, page, PAGE_SIZE),
            headers=headers)
        json_response = json.loads(response.content)
        hits = int(json_response['hits'])

        if page == 1:
            print "For site:", SITE
            print "Criteria: {}={}".format(field_name, field_value)
            print json_response
            print "# of assets:", hits
        else:
            print "...Continuing to page", page

        for item in json_response['item']:
            items.append(item['id'])

        pages = 1 + (hits // PAGE_SIZE)
        page += 1

    return items

for row in criteria:
    to_update_vxids = search_items(row[0], urllib.quote(row[1], safe=''))
    for to_update in to_update_vxids:
        update_field(to_update, row[0], row[2])

        #if row[0] in CONVENTION:
            #print "'{}' is in naming convention, updating title".format(row[0])
            #recalculate_title(to_update)
