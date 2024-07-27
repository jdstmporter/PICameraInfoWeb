#!/usr/bin/env python3
import argparse
from picam import PiCam
from wsgi import WSGIApp
from wsgiref.simple_server import make_server
from sys import argv

parser = argparse.ArgumentParser(
    prog='PiCamInfo',
    description='PiCam information web app'
)
parser.add_argument('-i', '--ip', action='store', default='0.0.0.0', dest='ip', nargs='?')
parser.add_argument('-p', '--port', action='store', default=8080, dest='port', type=int, nargs='?')
namespace = parser.parse_args()




''' set up camera info '''

print('Getting camera info')
info = PiCam()()
print(f'Camera info is : {info}')

print('Starting server')
app = WSGIApp(info)

httpd = make_server(namespace.ip, namespace.port, app)
print(f'Serving on port {namespace.ip}:{namespace.port}')
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    print('Interrupt')
    httpd.server_close()





