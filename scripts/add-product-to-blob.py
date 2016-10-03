#!/usr/bin/env python

from os import path
import sys

import simplejson as json
import requests
from requests.exceptions import RequestException

if __name__ == "__main__":
    from optparse import OptionParser
    doc = "%s --u url -n username -p password" % sys.argv[0]
    parser = OptionParser(doc)
    parser.add_option("-u", "--url", dest="url", type="string", default=False,
                      action="store", help="URL to the running admin API")
    parser.add_option("-n", "--username", dest="username", type="string", default=False,
                      action="store", help="Username for the Admin interface")
    parser.add_option("-p", "--password", dest="password", type="string", default=False,
                      action="store", help="Password for the Admin interface")
    options, args = parser.parse_args()

    if not options.url or not options.username:
        print "url and auth is required"
        sys.exit(1)

    url = options.url
    client = requests.Session()
    data = client.get(url + '/api/releases', auth=(options.username,
                                                   options.password))
    releases = data.json()['releases']

    unsuccessful_releases = []
    for release in releases:
        try:
            data = client.get(url + '/api/releases/' + release['name'],
                              auth=(options.username, options.password))
            blob = data.json()
            csrf_token = data.headers['X-CSRF-Token']
            if 'product' not in blob.keys():
                print 'changing %s' % release['name']
                blob['product'] = release['product']
                data = dict(data=json.dumps(blob), product=release['product'],
                            data_version=release['data_version'])

                data['csrf_token'] = csrf_token

                r = client.post(url + '/api/releases/' + release['name'],
                                json=data, auth=(options.username,
                                                 options.password))
                r.raise_for_status()
            else:
                print "%s already has product" % release['name']
        except RequestException as re:
            if re.response.status_code == 401:
                print "auth credentials not accepted"
                sys.exit(1)
            print sys.exc_info()
            unsuccessful_releases.append(release['name'])

    if len(unsuccessful_releases) != 0:
        print "these releases could not be updated successfully:"
        for release in unsuccessful_releases:
            print release
