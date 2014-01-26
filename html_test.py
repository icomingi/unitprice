#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sgmllib import SGMLParser
from re_test import extract_data

from urllib import urlopen
import json

import re

JD_ITEM = re.compile(r'http://item\.jd\.com/([0-9]{3,12})\.html', re.IGNORECASE)

JD_PRICE_SERVER = r'http://p.3.cn/prices/mgets?skuIds=J_'

class ProdInfoParser(SGMLParser):
    def reset(self):
        SGMLParser.reset(self)
        self.products = {}

    def output(self):
        return self.products

class YhdInfoParser(ProdInfoParser):        
    def start_span(self, attrs):
        attrs = dict(attrs)
        #print attrs
        if attrs.get('productid') and attrs.get('yhdprice'):
            #print attrs
            productId = attrs.get('productid')
            if not self.products.get(productId):
                self.products[productId] = {}
            self.products[productId]['yhdprice'] = attrs.get('yhdprice')
            #print self.products
            
    def start_a(self, attrs):
        attrs = dict(attrs)
        #print attrs
        if attrs.get('id') and attrs.get('pmid') and attrs.get('title'):
            #print attrs
            productId = attrs.get('id').split('_')[1]
            if not self.products.get(productId):
                self.products[productId] = {}
#            self.products[productId]['title'] = attrs.get('title')
            result = extract_data(attrs.get('title'))
            if result:
#                net, unit = result
                self.products[productId]['net'] = tuple(result)

class JdInfoParser(ProdInfoParser):
    def reset(self):
        ProdInfoParser.reset(self)
        self.atag_title_stack = []
    
    def start_a(self, attrs):
        attrs = dict(attrs)       
        if attrs.get('target') and attrs.get('href'):
            m = JD_ITEM.match(attrs.get('href'))
            if m:
                productId = m.groups()[0]
                if not self.products.get(productId):
                    self.products[productId] = {}
                self.atag_title_stack.append(productId)

    def handle_data(self, text):
        if self.atag_title_stack:
            productId = self.atag_title_stack.pop()
            result = extract_data(text)
            if result:
                self.products[productId]['net'] = tuple(result)

    def output(self):
        skus = self.products.keys()
        jd_price_url = JD_PRICE_SERVER + ',J_'.join(skus)
        try:
            f = urlopen(jd_price_url)
            prices = json.loads(f.read())
        except:
            pass
        finally:
            f.close()
        if prices:
            for p in prices:
                productId = p['id'][2:]
                self.products[productId]['jdprice'] = p['p']
        return self.products
        
#    def parse_declaration(self, i):
#        SGMLParser.parse_declaration(self, i)
#        return -1
    
def test_run():
    parser = ProdInfoParser()
    f = open('yhd.html')
    c = f.read()
 #   print c[:100]
    parser.feed(c)
    f.close()
    d = parser.output()
    print d
    for k, v in d.items():
        result = extract_data(v['title'])
        if result:
            net, unit = extract_data(v['title'])
            unit_price = float(v['yhdprice']) / net * 500
            print k
            print v['title']
            print "Unit price: ￥%.2f/500%s" % (unit_price, unit)
    #print data[:1000]

def jd_test_run():
    parser = JdInfoParser()
    f = urlopen(r'http://list.jd.com/1320-5019-5020-0-0-0-0-0-0-0-3-1-1-1-2-2824-2889-0.html')
    c = f.read()
    parser.feed(c)
    f.close()
    d = parser.output()
    print '\n'.join(["product: %s, price: %s, weight: %.1f%s" % (key, item['jd_price'], item['net'][0], item['net'][1]) for key, item in d.items() if item.get('net')])

    
if __name__ == "__main__":
    jd_test_run()
#    print '中文'
