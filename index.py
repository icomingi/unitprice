#-*- coding:utf-8 -*-
import json
import urllib
from html_test import ProdInfoParser
import re

from cgi import parse_qs, escape

TEST_URL = r'http://www.yhd.com/ctg/s2/c33708-0/'
SCRIPT_TAG = re.compile(r'<!%.*%!>', re.IGNORECASE)

def app(environ, start_response):
    parameters = parse_qs(environ.get('QUERY_STRING', ''))
    if 'url' in parameters:
        url = escape(parameters['url'][0])
    else:
        url = TEST_URL
    status = '200 OK'
    headers = [('Content-type', 'application/json')]
    start_response(status, headers)
#    body = {'x': 11, 'y': 12, 'z': 13}
    parser = ProdInfoParser()
    parser.feed(rmScript(getContent(url)))
    parser.close()
    body = parser.output()
    return json.dumps(body)

def getContent(url):
    f = urllib.urlopen(url)
    c = f.read()
    f.close()
    return c

def rmScript(c):
    m = SCRIPT_TAG.findall(c)
    if m:
        for e in m:
            c = re.sub(SCRIPT_TAG, '', c)
    return c

from bae.core.wsgi import WSGIApplication
application = WSGIApplication(app)
