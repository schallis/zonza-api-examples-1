#!/usr/bin/env python
import os
import requests
import json
import sys

from pprint import pprint

SET_ID = 'VX-123'
EXPORT_SHAPE = 'original'
FTP_LOCATION = 'ftp://username:password@ftpserver:21/path/'

url = 'http://api.zonza.tv:8080/v0/'

def raise_invalid():
    raise RuntimeError('Credentials not configured. Please set ' \
                       'env variables BORK_TOKEN and BORK_USERNAME')

auth = {
    'Bork-Token': os.environ.get("BORK_TOKEN") or raise_invalid(),
    'Bork-Username': os.environ.get("BORK_USERNAME") or raise_invalid(),
}

def get_set_items(vx_id):
    headers = {'content-type': 'application/json'}
    headers.update(auth)
    response = requests.get(
        '{}collection/{}/item'.format(url, vx_id),
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

for item_id in get_set_items(SET_ID):
    export(item_id)
