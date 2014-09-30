#!/usr/bin/env python
import os
import requests
import json
import sys

from pprint import pprint

ITEM = 'VX-285057'

url = 'http://api.zonza.tv:8080/v0/'

def raise_invalid():
    raise RuntimeError('Credentials not configured. Please set ' \
                       'env variables BORK_TOKEN and BORK_USERNAME')

auth = {
    'Bork-Token': os.environ.get("BORK_TOKEN") or raise_invalid(),
    'Bork-Username': os.environ.get("BORK_USERNAME") or raise_invalid(),
}

#import_settings = '<fill in>'

#filename = 'VX-8888.mp4'
#fs = os.path.getsize(filename)

#def get_ticket():
    #print 'getting ticket'
    #headers = {'content-type': 'application/json'}
    #headers.update(auth)

    #result = requests.post('{}item'.format(url), data=json.dumps({
        #'file-size': fs, 'filename': filename,
    #}), headers=headers)

    #if result.status_code != 200:
        #print result.status_code
        #print result.content
        #raise Exception('Error getting ticket')

    #print 'got ticket'
    #print result.text
    #return result.json()

#def upload(data):
    #ticket = data['ticket']
    ##chunk_size = data['max_chunk_size'] / 10
    #chunk_size = 524288
    #index = 0
    #for data in read_chunks(filename, chunk_size):
        #print 'uploading chunk at index {}'.format(index)
        #result = upload_data(data, ticket, index)
        #index += chunk_size

    #print 'item', result.content

#def upload_data(data, ticket, index):
    #headers = {'index': index, 'upload-ticket': ticket}
    ## headers.update(auth)

    #result = requests.post('{}item/chunk'.format(url), data=data, headers=headers)
    #if result.status_code != 200:
        #print result.status_code
        #print result.content
        #raise Exception('Error uploading chunk')
    #return result

#def read_chunks(fn, chunk_size):
    #with open(fn, 'rb') as f:
        #while True:
            #data = f.read(chunk_size)
            #if not data:
                #break
            #yield data


print 'searching...'
headers = {'content-type': 'application/json'}
headers.update(auth)
response = requests.get(
    '{}item/{}'.format(url, ITEM),
    headers=headers)
json_response = json.loads(response.content)
print pprint(json_response)

