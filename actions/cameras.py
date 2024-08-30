
from picam import PiCam
from .base import display, getInformation
from wsgi import WSGIApp
from wsgiref.simple_server import make_server




def listCameras():
    try:
        cameras, modes = getInformation()
        display(cameras, modes)
    except Exception as e:
        print(f'Error : {e}')


def runCameraServer(ip,port):
    print('Getting camera info')
    info = PiCam()()
    print(f'Camera info is : {info}')

    print('Starting server')
    app = WSGIApp(info)

    print(f'Serving on port {ip}:{port}')
    httpd = make_server(ip, port, app)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('Interrupt')
        httpd.server_close()