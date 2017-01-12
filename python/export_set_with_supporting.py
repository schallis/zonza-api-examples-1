#!/usr/bin/env python
import os
import requests
import json
import sys
from ftplib import FTP

from pprint import pprint

"""
Export a specified set with supporting files to an FTP location
"""

EXPORT_SHAPE = 'original'

def raise_invalid():
    raise RuntimeError('Environment not configured. Please set ' \
                       'env variables BORK_TOKEN and BORK_USERNAME etc.')

FTP_USER = os.environ.get("FTP_USER") or raise_invalid()
FTP_PASS = os.environ.get("FTP_PASS") or raise_invalid()
FTP_PATH = os.environ.get("FTP_PATH") or raise_invalid()
FTP_LOCATION = os.environ.get("FTP_LOCATION") or raise_invalid()

url = 'http://api.zonza.tv:8080/v0/'

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

def get_set_items_from_file(filepath):
    f = open(filepath, 'r')
    return [x for x in f.read().splitlines()]

def export(vx_id, subpath=''):
    headers = {'content-type': 'application/json'}
    headers.update(auth)
    uri = 'ftp://{0}:{1}@{2}:21/{3}{4}/'.format(FTP_USER, FTP_PASS,
            FTP_LOCATION, FTP_PATH, subpath)
    print "Exporting to", uri
    body=json.dumps({
        'uri': uri,
        'tag': EXPORT_SHAPE,
    })
    response = requests.post('{}item/{}/export'.format(url, vx_id),
        data=body, headers=headers)
    json_response = json.loads(response.content)
    print pprint(json_response)

def ensure_ftp_dirs(dirs=[]):
    ftp = FTP(FTP_LOCATION)
    ftp.login('stevenchallis', 'Zonza2015')

    for path in dirs:
        full_path = FTP_PATH + path
        split_path = full_path.split('/')
        parent_path, directory = '/'.join(split_path[:-1]), split_path[-1]
        parent_path = parent_path or FTP_PATH
        if full_path not in ftp.nlst(parent_path):
            print "Creating FTP path", full_path
            ftp.mkd(full_path)
        else:
            print directory, "already exists in", parent_path

    ftp.quit()

def get_supporting(vx_id):
    headers = {'content-type': 'application/json'}
    headers.update(auth)
    response = requests.get('{}item/{}/sf'.format(url, vx_id), headers=headers)
    json_response = json.loads(response.content)

    return [sf['id'] for sf in json_response['item']]

def get_filename(vx_id):
    headers = {'content-type': 'application/json'}
    headers.update(auth)
    response = requests.get(
        '{}item/{}'.format(url, vx_id),
        headers=headers)
    json_response = json.loads(response.content)
    return json_response['metadata']['mazda_filename'] or 'vx-id'

def download_original(item_id, outfile):
    from contextlib import closing

    with closing(requests.get('http://httpbin.org/get', stream=True)) as r:
        outf = open(outfile, 'wb')
        outf.write(r)
        out.close()



if __name__ == '__main__':
    """
    VX-SET/
        filename.ext
        filename.ext/
            supporting.ext
    """
    #sf_dir = 'VX-25687/VX-321678_MY16_MX5_Global_Film_Celebration_Generic_ProRes_JQGN0026000H.mov'
    #ensure_ftp_dirs([sf_dir])
    #export('VX-321678', sf_dir)
    set_id = sys.argv[1]
    if not set_id.startswith('VX-'):
        raise Exception('No VX ID specified')

    #all_items = get_set_items(set_id)
    all_items = get_set_items_from_file(set_id)
    print "Exporting", len(all_items), "to", FTP_LOCATION

    ensure_ftp_dirs([set_id])

    for item_id in all_items:
        print "starting item", item_id
        supporting_ids = get_supporting(item_id)
        print "Found", len(supporting_ids), "supporting files"
        if supporting_ids:
            filename = get_filename(item_id)
            outfile = item_id + '_' + filename
            outfile = outfile.encode('ascii', 'replace').replace(' ', '_').replace('/', '_').replace('%', '_')
            #download_original(item_id, outfile)
            sf_dir = set_id + '/' + outfile
            try:
                ensure_ftp_dirs([sf_dir])
            except Exception, err:
                import ipdb; ipdb.set_trace()

            # Export supporting
            for s_id in supporting_ids:
                print "exporting sf", s_id
                export(s_id, sf_dir)

        #export(item_id)
