#!/usr/bin/env python3

from picam import PiCam
from wsgi import WSGIApp
from wsgiref.simple_server import make_server
from sys import argv

try:
    port = int(argv[1])
except:
    port = 8000



''' set up camera info '''

print('Getting camera info')
info = PiCam()()
print(f'Camera info is : {info}')

print('Starting server')
app = WSGIApp(info)

httpd = make_server('', port, app)
print(f'Serving on port {port}')
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    print('Interrupt')
    httpd.server_close()





