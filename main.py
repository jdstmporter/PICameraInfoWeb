#!/usr/bin/env python3
from actions import BatteryDaemon, Cameras, SQL, CameraServer
import argparse

from actions.power import Battery

parser = argparse.ArgumentParser(
    prog='PiCamInfo',
    description='PiCam information web app'
)

subs = parser.add_subparsers(title='Modes of operation')
parserC = subs.add_parser('camera',description='Camera actions',help='camera mode help')
parserC.add_argument('action', action='store', dest='action', type=str, choices=['raw','load','store'])
parserC.set_defaults(actor='camera')

parserB = subs.add_parser('battery',description='Battery actions',help='battery mode help')
parserB.add_argument('action', action='store', dest='action', type=str, choices=['raw','load','store'])
parserB.set_defaults(actor='battery')

parserD = subs.add_parser('daemon',description='Run battery daemon')
parserD.set_defaults(actor='daemon')

parserS = subs.add_parser('service',description='Start web service')
parserS.add_argument('-i', '--ip', action='store', default='0.0.0.0', dest='ip', nargs='?',help='IP for web server')
parserS.add_argument('-p', '--port', action='store', default=8080, dest='port', type=int, nargs='?',help='Port for web server')
parserS.set_defaults(actor='service')

namespace = parser.parse_args()
actor = namespace.actor

if actor=='camera':
    action=namespace.action
    c = Cameras()
    if action=='raw':
        c.list()
    elif action=='load':
        c.read()
    elif action=='store':
        c.write()
    else:
        parser.print_help()

elif actor=='battery':
    action = namespace.action
    b = Battery()
    if action == 'raw':
        b.list()
    elif action == 'load':
        b.read()
    elif action == 'store':
        b.write()
    else:
        parser.print_help()

elif actor=='daemon':
    print('Starting battery daemon')
    batteryDaemon = BatteryDaemon()
    batteryDaemon.start()

elif actor=='service':
    c=CameraServer(namespace.ip,namespace.port)
    c.start()

else:
    parser.print_help()









