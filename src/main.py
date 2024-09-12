#!/usr/bin/env python3
from tools import BatteryDaemon, Cameras, CameraServer, Battery,Logger
import argparse

parser = argparse.ArgumentParser(
    prog='PiCamInfo',
    description='PiCam information web app'
)

subs = parser.add_subparsers(title='Modes of operation')
parserC = subs.add_parser('camera',description='Camera actions',help='camera mode help')
parserC.add_argument('action', action='store', dest='action', type=str, choices=['raw','load','store'])
parserC.set_defaults(processor=Cameras)

parserB = subs.add_parser('battery',description='Battery actions',help='battery mode help')
parserB.add_argument('action', action='store', dest='action', type=str, choices=['raw','load','store'])
parserB.set_defaults(processor=Battery)

parserD = subs.add_parser('daemon',description='Run battery daemon')
parserD.set_defaults(processor=BatteryDaemon)

parserS = subs.add_parser('service',description='Start web service')
parserS.add_argument('-i', '--ip', action='store', default='0.0.0.0', dest='ip', nargs='?',help='IP for web server')
parserS.add_argument('-p', '--port', action='store', default=8080, dest='port', type=int, nargs='?',help='Port for web server')
parserS.set_defaults(processor=CameraServer)

namespace = parser.parse_args()
try:
    proc=namespace.processor()
    proc(**vars(namespace))
except Exception as e:
    Logger.log.debug(f'Parser error: {e}')
    parser.print_help()















