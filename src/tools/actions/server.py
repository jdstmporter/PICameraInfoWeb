from .base import BaseAction
from tools.data import DataStore
from tools.util import Logger
from tools.wsgi import WSGIApp
from wsgiref.simple_server import make_server

class CameraServer(BaseAction):
    def __init__(self):
        super().__init__()

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