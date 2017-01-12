#!/usr/bin/env python
import os
import requests
import json
import sys
import time
import urllib

from pprint import pprint

"""
Update multiple metadata fields where those fields cascade
"""

SITE = 'zonza.tv'
CONVENTION = '{brand} {year} {campaign} {language} {media_type} {agency}'
PAGE_SIZE = 100

url = os.environ.get('BORK_URL') or 'http://api.zonza.tv:8080/v0/'

criteria = (
    # Old Fields->values, New Field->Value
    # e.g. where Sudafed and Sophie, update to Andrew
    ((
        ('jnj_brand', 'Sudafed'),
        ('jnj_uscn', 'Sophie Christiansen'),
    ), ('jnj_uscn', 'Andrew Vincent')),
    ((
        ('jnj_brand', 'Calcough'),
        ('jnj_uscn', 'Sophie Christiansen'),
    ), ('jnj_uscn', 'Antonia Wood')),
    ((
        ('jnj_brand', 'Calpol'),
        ('jnj_uscn', 'Sophie Christiansen'),
    ), ('jnj_uscn', 'Antonia Wood')),
    ((
        ('jnj_brand', 'Benylin'),
        ('jnj_uscn', 'Sophie Christiansen'),
    ), ('jnj_uscn', 'Ellie Harper')),
    ((
        ('jnj_brand', 'Imodium'),
        ('jnj_uscn', 'Sophie Christiansen'),
    ), ('jnj_uscn', 'Ellie Harper')),
    ((
        ('jnj_brand', 'Listerine'),
        ('jnj_uscn', 'Sophie Christiansen'),
    ), ('jnj_uscn', 'Julia LePla')),
    ((
        ('jnj_brand', 'ImoFlora'),
        ('jnj_uscn', 'Sophie Christiansen'),
    ), ('jnj_uscn', 'Lizzie Alleyne')),
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
def search_items(fieldvalues):
    items = []
    hits = 0
    page = 1
    pages = 1
    query = ''.join(['&{}={}'.format(field, urllib.quote(val, ''))
        for field, val in fieldvalues])
    while page <= pages:
        response = requests.get(
            '{}item?zonza_site={}{}&zonza_supporting_file_master=&__page={}&__page_size={}'.format(url,
                SITE, query, page, PAGE_SIZE),
            headers=headers)
        json_response = json.loads(response.content)
        hits = int(json_response['hits'])

        if page == 1:
            print "For site:", SITE
            print "Criteria: {}".format(query)
            #print json_response
            print "# of assets:", hits
        else:
            print "...Continuing to page", page

        for item in json_response['item']:
            items.append(item['id'])

        pages = 1 + (hits // PAGE_SIZE)
        page += 1

    return items

for fieldvalues, newfieldvalue in criteria:
    to_update_vxids = search_items(fieldvalues)
    for to_update in to_update_vxids:
        update_field(to_update, *newfieldvalue)
        #if newfieldvalue[0] in CONVENTION:
            #print "'{}' is in naming convention, updating title".format(newfieldvalue[0])
            #recalculate_title(to_update)
