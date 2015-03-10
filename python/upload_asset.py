#!/usr/bin/env python
import base64
import hashlib
import os
import random
import requests
import json
from datetime import datetime
import sys

"""
Usage: python upload_asset.py <filename>
"""

def raise_invalid():
    raise RuntimeError('Credentials not configured. Please set ' \
                       'env variables BORK_TOKEN and BORK_USERNAME')

fs = 1024 * 1024
url = 'http://api.zonza.tv:8080/v0/'
auth = {
    'Bork-Token': os.environ.get("BORK_TOKEN") or raise_invalid(),
    'Bork-Username': os.environ.get("BORK_USERNAME") or raise_invalid(),
}

filename = sys.argv[1]
fs = os.path.getsize(filename)
upload_fn = filename

def get_ticket():
    print 'getting ticket'
    headers = {'content-type': 'application/json'}
    headers.update(auth)

    result = requests.post('{}item'.format(url), data=json.dumps({'file-size':
        fs, 'filename': upload_fn, 'import-settings': 'VX-6',
        'transcode-groups': []}), headers=headers)
    if result.status_code != 200:
        print result.status_code
        open('error.html', 'wb').write(result.content)
        raise Exception()

    print 'got ticket'
    return result.json()

def upload(data):
    ticket = data['ticket']
    chunk_size = data['max_chunk_size']

    fhash = hashlib.new('sha1')
    index = 0
    start = datetime.now()
    iterator = read_chunks(filename, chunk_size)
    for data in iterator:
        print len(data)
        print 'upload {}-{}/{}'.format(index, index+chunk_size, fs)
        result = upload_data(data, ticket, index)
        fhash.update(data)
        index += chunk_size
    print datetime.now() - start
    print 'item', result.content
    return fhash.hexdigest()

def upload_data(data, ticket, index):
    result = requests.post('{}item/chunk'.format(url), data=data, headers={'index': index, 'upload-ticket': ticket})
    if result.status_code != 200:
        print result.status_code
        open('error.html', 'wb').write(result.content)
        raise Exception()
    return result

def read_chunks(fn, chunk_size):
    with open(fn, 'rb') as f:
        while True:
            data = f.read(chunk_size)
            if not data:
                break
            yield data

data = get_ticket()
print data
fhash = upload(data)
print fhash
