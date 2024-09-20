#!/usr/bin/env python3
import actions
from util import Logger
import argparse



parser = argparse.ArgumentParser(
    prog='PiCamInfo',
    description='PiCam information web app'
)

subs = parser.add_subparsers(title='Modes of operation')

# TODO: Test camera raw
# TODO: Test camera load (DONE)
# TODO: Test camera store
parserC = subs.add_parser('camera',description='Camera actions',help='camera mode help')
parserC.add_argument('action', action='store', type=str, choices=['raw','load','store'])
parserC.set_defaults(processor=actions.CameraTool)

# TODO: Test camera raw (DONE)
# TODO: Test camera load (DONE)
# TODO: Test camera store (DONE)
# TODO: Test battery clean (DONE)
parserB = subs.add_parser('battery',description='Battery actions',help='battery mode help')
parserB.add_argument('action', action='store', type=str, choices=['raw','load','store','clean'])
parserB.set_defaults(processor=actions.BatteryTool)

#  TODO: Test daemon (DONE)
parserD = subs.add_parser('daemon',description='Run battery daemon')
parserD.set_defaults(processor=actions.BatteryDaemon)

# TODO Test service
#      URLS to test:
#      / : currently camera, should be api
#      /cam : camera
#      /batt : battery
#      /batt?ts=nnnnnn : battery CSV since specified unix timestamp
parserS = subs.add_parser('service',description='Start web service')
parserS.add_argument('-i', '--ip', action='store', default='0.0.0.0', dest='ip', nargs='?',help='IP for web server')
parserS.add_argument('-p', '--port', action='store', default=8080, dest='port', type=int, nargs='?',help='Port for web server')
parserS.set_defaults(processor=actions.CameraServer)

namespace = parser.parse_args()

ns = vars(namespace)
for k,v in ns.items():
    print(f"Key [{k}] Value [{v}]")
try:
    proc=namespace.processor()
    proc(**vars(namespace))
except Exception as e:
    Logger.log.debug(f'Parser error: {e}')
    parser.print_help()















