#!/usr/bin/env python
SITE = 'demo.zonza.tv'
import os
import requests
import json
import sys
import time

"""
Update the ZONZA domain for an VX item specified as the input param
"""

from pprint import pprint

url = 'http://api.zonza.tv:8080/v0/'

def raise_invalid():
    raise RuntimeError('Credentials not configured. Please set ' \
                       'env variables BORK_TOKEN and BORK_USERNAME')

auth = {
    'Bork-Token': os.environ.get("BORK_TOKEN") or raise_invalid(),
    'Bork-Username': os.environ.get("BORK_USERNAME") or raise_invalid(),
}

print 'replacing...'
headers = {'content-type': 'application/json'}
headers.update(auth)

def update_field(item):
    item_url = url + 'item/' + item + '/metadata'
    new_data = {
            'zonza_site': 'zonza.tv'
    }
    update_response = requests.post(
            item_url,
            data=json.dumps(new_data),
            headers=headers)
    print update_response, item_url


vx_id = sys.argv[1]
update_field(vx_id)
