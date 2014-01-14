#-*- coding:utf-8 -*-
import json

def app(environ, start_response):
    status = '200 OK'
    headers = [('Content-type', 'application/json')]
    start_response(status, headers)
    body = {'x': 1, 'y': 2, 'z': 3}
    return json.dumps(body)

from bae.core.wsgi import WSGIApplication
application = WSGIApplication(app)
