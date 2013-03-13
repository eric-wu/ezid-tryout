#!/usr/bin/python

import datetime
import random
import string
import time
import urllib2

def login(user, password):
    auth_handler = urllib2.HTTPBasicAuthHandler()
    auth_handler.add_password(realm='EZID',
                              uri='https://n2t.net/ezid/',
                              user=user,
                              passwd=password)
    opener = urllib2.build_opener(auth_handler)
    urllib2.install_opener(opener)
    response = urllib2.urlopen('https://n2t.net/ezid/login')
    cookie = response.headers["Set-Cookie"].split(";")[0]
    return cookie

def random_string(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for c in range(size))

def create_metadata(creator, title, target):
    metadata = 'datacite.creator: ' + creator
    metadata = metadata + '\r\n'
    metadata = metadata + 'datacite.title: ' + title
    metadata = metadata + '\r\n'
    metadata = metadata + 'datacite.publisher: ' + 'Sage Bionetworks'
    metadata = metadata + '\r\n'
    metadata = metadata + 'datacite.publicationyear: ' + str(datetime.date.today().year)
    metadata = metadata + '\r\n'
    metadata = metadata + '_target: ' + target
    return metadata

def create_doi(cookie):
    random_str = random_string()
    request = urllib2.Request('http://n2t.net/ezid/id/doi:10.5072/FK2.' + random_str)
    request.get_method = lambda: 'PUT'
    request.add_header("Cookie", cookie)
    request.add_header("Content-Type", "text/plain; charset=UTF-8")
    request.add_data(create_metadata('Wu, Eric', random_str, 'http://synapse.sagebase.com'))
    try:
        start = time.time()
        response = urllib2.urlopen(request)
        end = time.time()
        output = response.read()
        print output
        print str(end - start)
    except urllib2.HTTPError as e:
        print e.code, e.msg
        print e.fp.read()

cookie = login('apitest', 'apitest')
create_doi(cookie)

