#-*- coding:utf-8 -*-
import json
import urllib
from html_test import JdInfoParser, YhdInfoParser, ProdInfoParser
import re
import web
import urlparse

from flask import Flask, request, make_response

from cgi import parse_qs, escape

from selenium import webdriver

TEST_URL = r'http://www.yhd.com/ctg/s2/c33708-0/'
SCRIPT_TAG = re.compile(r'<!%.*%!>', re.IGNORECASE)

app = Flask(__name__)
app.debug  = True


@app.route('/')
#def app(environ, start_response):
def unit_price():
#    parameters = parse_qs(environ.get('QUERY_STRING', ''))
#    if 'url' in parameters:
#        url = escape(parameters['url'][0])
#    else:
#        url = TEST_URL
#    status = '200 OK'
#    headers = [('Content-type', 'application/json')]
#    start_response(status, headers)
    url_parse_result = urlparse.urlparse(url)
    if 'jd.com' in url_parse_result.netloc:
        parser = JdInfoParser()
        page_source = getContent(url)
    elif 'yhd.com' in url_parse_result.netloc:
        parser = YhdInfoParser()
#        page_source = rmScript(getContent(url))
#        page_source = page_source.decode('utf-8')
        url = url.replace('ctg/s2', 'ctg/searchPage')
        products = rmScript(getContent(url))
        extra_products = rmScript(getContent(url+'/?isGetMoreProducts=1'))
        products = json.loads(products)
        extra_products = json.loads(extra_products)
        products = isinstance(products, unicode) and products.encode('utf-8') or products
        extra_products = isinstance(extra_products, unicode) and extra_products.encode('utf-8') or extra_products
        page_source = products.get('value') + extra_products.get('value')
    else:
        parser = ProdInfoParser()
        page_source = rmScript(getContent(url))
    parser.feed(page_source)
    parser.close()
    body = parser.output()
#    body['web'] = web.__version__
#    ff = webdriver.Firefox()
#    ff.get('http://www.baidu.com/')
#    dom = ff.execute_script('document.documentElement.innerHTML')
#    body['dom'] = dom
#    return json.dumps(body)
    return (make_response(json.dumps(body)), '200 OK', {'Content-type': 'application/json'})


def getContent(url):
    f = urllib.urlopen(url)
    c = f.read()
    f.close()
    return c

def rmScript(c):
#    m = SCRIPT_TAG.findall(c)
#    if m:
#        for e in m:
#            c = re.sub(SCRIPT_TAG, '', c)
    c = c.replace('<!%', '')
    c = c.replace('%!>', '')
    return c

from bae.core.wsgi import WSGIApplication
application = WSGIApplication(app)
