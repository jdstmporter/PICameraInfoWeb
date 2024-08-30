#!/usr/bin/env python3
from actions import listCameras, dumpDB, initialiseDB, readBattery, runCameraServer
import argparse




parser = argparse.ArgumentParser(
    prog='PiCamInfo',
    description='PiCam information web app'
)

groupU=parser.add_argument_group('utilities')
groupU.add_argument('-w','--write', action='store_true', dest='write',help='Initialise camera information DB')
groupU.add_argument('-r','--read', action='store_true', dest='read',help='dump camera information DB')
groupU.add_argument('-c','--cameras', action='store_true', dest='cameras',help='List available cameras and modes')
groupU.add_argument('-b','--battery',action='store_true',dest='battery',help='Print battery status')

groupS=parser.add_argument_group('services')
groupS.add_argument('-d','--daemon',action='store_true',dest='daemon',help='Start battery daemon')
groupS.add_argument('-s','--server',action='store_true',dest='webserver',help='Start web server')
groupS.add_argument('-i', '--ip', action='store', default='0.0.0.0', dest='ip', nargs='?',help='IP for web server')
groupS.add_argument('-p', '--port', action='store', default=8080, dest='port', type=int, nargs='?',help='Port for web server')

namespace = parser.parse_args()



''' set up camera info '''
if namespace.cameras:
    listCameras()

elif namespace.read:
    dumpDB()
elif namespace.write:
    initialiseDB()

elif namespace.battery:
    readBattery()

elif namespace.daemon:
    print('Starting battery daemon')
    # runBatteryDaemon()
    pass

elif namespace.webserver:
    runCameraServer(namespace.ip,namespace.port)

else:
    parser.print_help()









