#!/usr/bin/env python
import os
import requests
import json
import sys

from pprint import pprint

"""
Trigger an export to an FTP location for an item with specified VX ID
"""

EXPORT_SHAPE = 'original'


FTP_LOCATION = 'ftp://username:password@ftpserver:21/path/'

url = 'http://api.zonza.tv:8080/v0/'

def raise_invalid():
    raise RuntimeError('Environment not configured. Please set ' \
                       'env variables BORK_TOKEN and BORK_USERNAME etc.')

auth = {
    'Bork-Token': os.environ.get("BORK_TOKEN") or raise_invalid(),
    'Bork-Username': os.environ.get("BORK_USERNAME") or raise_invalid(),
}

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

item_id = sys.argv[1]
if not item_id.startswith('VX-'):
    raise Exception('No VX ID specified')

export(item_id)

