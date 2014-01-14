#-*- coding:utf-8 -*-
import json
import urllib
from html_test import ProdInfoParser

TEST_URL = r'http://www.yhd.com/ctg/s2/c33708-0/'

def app(environ, start_response):
    status = '200 OK'
    headers = [('Content-type', 'application/json')]
    start_response(status, headers)
#    body = {'x': 11, 'y': 12, 'z': 13}
    parser = ProdInfoParser()
    parser.feed(getContent(TEST_URL))
    parser.close()
    body = parser.output()
    return json.dumps(body)

def getContent(url):
    f = urllib.urlopen(url)
    c = f.read()
    f.close()
    return c



from bae.core.wsgi import WSGIApplication
application = WSGIApplication(app)
