#!/usr/bin/env python
import os
import requests
import json
import sys

from pprint import pprint

EXPORT_SHAPE = 'original'

# 'ftp://username:password@ftpserver:21/path/'
FTP_LOCATION = os.environ.get("FTP_LOCATION") or raise_invalid(),

url = 'http://api.zonza.tv:8080/v0/'

def raise_invalid():
    raise RuntimeError('Environment not configured. Please set ' \
                       'env variables BORK_TOKEN and BORK_USERNAME etc.')

auth = {
    'Bork-Token': os.environ.get("BORK_TOKEN") or raise_invalid(),
    'Bork-Username': os.environ.get("BORK_USERNAME") or raise_invalid(),
}

def get_set_items(vx_id):
    headers = {'content-type': 'application/json'}
    headers.update(auth)
    response = requests.get(
        '{}collection/{}/item?__page=2'.format(url, vx_id),
        headers=headers)
    json_response = json.loads(response.content)
    return [item['id'] for item in json_response['item']]

def export(vx_id):
    headers = {'content-type': 'application/json'}
    headers.update(auth)
    body=json.dumps({
        'uri': FTP_LOCATION,
        'tag': EXPORT_SHAPE,
    })
    response = requests.post('{}item/{}/export'.format(url, vx_id),
        data=body, headers=headers)
    json_response = json.loads(response.content)
    print pprint(json_response)

set_id = sys.argv[1]
if not set_id.startswith('VX-'):
    raise Exception('No VX ID specified')

all_items = get_set_items(set_id)
print len(all_items)

#for item_id in all_items:
    #export(item_id)

