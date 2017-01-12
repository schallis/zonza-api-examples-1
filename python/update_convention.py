#!/usr/bin/env python
from __future__ import unicode_literals
import os
import requests
import json
import sys
import time
import urllib

from pprint import pprint

"""
Update the title of a list of assets according to a naming convention
specified in this file
"""


# Search for assets matching a filter criteria and replace with new metadata
# values

SITE = 'zonza.tv'
CONVENTION = '{brand} {year} {campaign} {language} {media_type} {_agency}'

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

def get_items_from_file(filepath):
    f = open(filepath, 'r')
    return [x for x in f.read().splitlines()]

to_update_vxids = get_items_from_file('input_ids')
for to_update in to_update_vxids:
    print "updating", to_update
    recalculate_title(to_update)
