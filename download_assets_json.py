#!/usr/bin/env python
import os
import requests
import json
import sys
import csv
"""
Retrieves all metadata information for all files specified in a input CSV
file, specified here as a download report
"""

from pprint import pprint

FILE = '/Users/stevenchallis/Desktop/downloads.csv'
OUTFILE = '/Users/stevenchallis/Desktop/fileinfo.json'

url = 'http://api.zonza.tv:8080/v0/'

def raise_invalid():
    raise RuntimeError('Credentials not configured. Please set ' \
                       'env variables BORK_TOKEN and BORK_USERNAME')

auth = {
    'Bork-Token': os.environ.get("BORK_TOKEN") or raise_invalid(),
    'Bork-Username': os.environ.get("BORK_USERNAME") or raise_invalid(),
}

print 'searching...'
headers = {'content-type': 'application/json'}
headers.update(auth)


def get_json(vxid, sfile):
    response = requests.get(
        '{}item/{}'.format(url, vxid),
        headers=headers)
    if response.status_code == 200:
        content = json.loads(response.content)
        metadata = content['metadata']
        metadata['Supporting File'] = sfile
        return metadata
    else:
        print 'did not find', vxid
        return {'Deleted': '1'}

def write_to_file(fileinfo):
    outfile = open(OUTFILE, 'w')
    outfile.write(json.dumps(fileinfo.items()))
    outfile.close()

# VXId -> metadata
fileinfo = {}

with open(FILE, 'rb') as download_report:
    reader = csv.reader(download_report)
    FIRST = True
    for row in reader:
        if FIRST:
            FIRST = False
            continue
        datetime, user, vxid, supporting_id, revision, site, filesize, size_in_gb = row
        if vxid.startswith('VX'):
            identifier = vxid
            sfile = 0
        else:
            identifier = supporting_id[3:-2]
            sfile = 1
        if identifier not in fileinfo.keys():
            fileinfo[vxid] = get_json(identifier, sfile)

write_to_file(fileinfo)
