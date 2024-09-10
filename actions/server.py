from data import DataStore
from util import Logger
from wsgi import WSGIApp
from wsgiref.simple_server import make_server

class CameraServer:
    def __init__(self,ip,port):
        self.ip=ip
        self.port=port
        with DataStore() as sql:
            self.info = sql.json()
        Logger.log.info(f'Camera info is : {self.info}')

    def start(self):
        Logger.log.info('Starting server')
        app = WSGIApp(self.info)

        Logger.log.info(f'Serving on port {self.ip}:{self.port}')
        httpd = make_server(self.ip, self.port, app)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            Logger.log.warning('Keyboard interrupt: terminating')
            httpd.server_close()