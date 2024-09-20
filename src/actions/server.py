from data import DataStore
from util import Logger
from .wsgi import WSGIApp
from tools import UPSDevice
from wsgiref.simple_server import make_server
from time import sleep

class CameraServer:
    def __init__(self):
        with DataStore() as sql:
            self.info = sql.json()
        Logger.log.info(f'Camera info is : {self.info}')

    def __call__(self,**kwargs):
        Logger.log.info('Starting server')
        ip = kwargs.get('ip','0.0.0.0')
        port = kwargs.get('port',8080)
        app = WSGIApp(self.info)

        Logger.log.info(f'Serving on port {ip}:{port}')
        httpd = make_server(ip, port, app)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            Logger.log.warning('Keyboard interrupt: terminating')
            httpd.server_close()

class BatteryDaemon:
    def __init__(self,interval=10):
        self.interval=interval
        self.sql = DataStore()
        self.ups = UPSDevice()
        self.ups.connect()

    def __del__(self):
        self.ups.close()
        self.sql.close()

    def __call__(self,**kwargs):
        run = True
        while run:
            try:
                Logger.log.debug('Logging battery level...')
                info = self.ups()
                self.sql.battery=info
                sleep(self.interval)
            except KeyboardInterrupt:
                Logger.log.warning('Keyboard interrupt: terminating')
                run = False
            except Exception as e:
                Logger.log.error(f'Error : {e}')