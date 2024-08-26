#!/usr/bin/env python3
from data import MysqlStore
from picam import PiCam
from wsgi import WSGIApp
from wsgiref.simple_server import make_server
import argparse
from sys import argv

def getInformation():
    cams = PiCam()
    return (cams.cameras, cams.modes)

def display(cameras, modes):
    print('Cameras:')
    for n in range(len(cameras)):
        print(f'{n} : {cameras[n]}')

    print('Modes:')
    for mode in modes:
        print(str(mode))


parser = argparse.ArgumentParser(
    prog='PiCamInfo',
    description='PiCam information web app'
)
parser.add_argument('-i', '--ip', action='store', default='0.0.0.0', dest='ip', nargs='?')
parser.add_argument('-p', '--port', action='store', default=8080, dest='port', type=int, nargs='?')
parser.add_argument('-w','--write', action='store_true', dest='write')
parser.add_argument('-r','--read', action='store_true', dest='read')
parser.add_argument('-c','--cameras', action='store_true', dest='cameras')


namespace = parser.parse_args()



''' set up camera info '''
if namespace.cameras:
    try:
        cameras, modes = getInformation()
        display(cameras, modes)
    except Exception as e:
        print(f'Error : {e}')

elif namespace.read:
    try:
        mysql = MysqlStore()
        display(mysql.cameras,mysql.modes)
        mysql.close()
    except Exception as e:
        print(f'Error : {e}')
elif namespace.write:
    try:
        print('Initialising camera info database')
        print('Getting camera info')
        cameras, modes = getInformation()
        display(cameras, modes)


        print('Loading database')
        mysql = MysqlStore()
        mysql.setCameras(cameras)
        mysql.setModes(modes)
        mysql.close()
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





