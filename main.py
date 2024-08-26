#!/usr/bin/env python3
from data import MysqlStore
from picam import PiCam
from wsgi import WSGIApp
from wsgiref.simple_server import make_server
import argparse
from sys import argv

parser = argparse.ArgumentParser(
    prog='PiCamInfo',
    description='PiCam information web app'
)
parser.add_argument('-i', '--ip', action='store', default='0.0.0.0', dest='ip', nargs='?')
parser.add_argument('-p', '--port', action='store', default=8080, dest='port', type=int, nargs='?')
parser.add_argument('-s','--setup', action='store_true', dest='setup')
namespace = parser.parse_args()



''' set up camera info '''

if namespace.setup:
    try:
        print('Initialising camera info database')
        print('Getting camera info')
        cams = PiCam()
        cameras = cams.cameras
        print(f'Cameras: {cameras}')
        modes = cams.modes
        print('Camera modes:')
        for mode in modes:
         print(f'{mode}')

        print('Loading database')
        mysql = MysqlStore()
        mysql.cameras=cameras
        mysql.modes=modes
    except Exception as e:
        print(f'Error: {e}')


else:

    print('Getting camera info')
    info = PiCam()()
    print(f'Camera info is : {info}')

    print('Starting server')
    app = WSGIApp(info)

    print(f'Serving on port {namespace.ip}:{namespace.port}')
    httpd = make_server(namespace.ip, namespace.port, app)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('Interrupt')
        httpd.server_close()





